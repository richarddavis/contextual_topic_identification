
import model
import utils
import pandas as pd
import pickle
import dill
import matplotlib.pyplot as plt
import os
import pathlib

import warnings
warnings.filterwarnings('ignore', category=Warning)

import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--fpath', default='/contextual_topic_identification/data/steam_reviews.csv')
    parser.add_argument('--colname', default='review')
    parser.add_argument('--ntopic', default=10)
    parser.add_argument('--method', default='TFIDF')
    parser.add_argument('--samp_size', default=10000)
    args = parser.parse_args()

    data = pd.read_csv(str(args.fpath))
    data = data.fillna('')  # only the comments has NaN's
    rws = data[args.colname]
    sentences, token_lists, idx_in = model.preprocess(rws, samp_size=int(args.samp_size))
    # Define the topic model object
    tm = model.Topic_Model(k = int(args.ntopic), method = str(args.method))
    # Fit the topic model by chosen method
    tm.fit(sentences, token_lists)
    # Evaluate using metrics

    model_path = pathlib.Path(__file__).parent.parent.absolute()
    model_path = os.path.join(model_path, 'docs/saved_models')

    with open(os.path.join(model_path, f'{tm.id}.file'), 'wb') as f:
        dill.dump(tm, f, pickle.HIGHEST_PROTOCOL)

    print('Coherence:', utils.get_coherence(tm, token_lists, 'c_v'))
    print('Silhouette Score:', utils.get_silhouette(tm))
    # visualize and save img
    utils.visualize(tm)
    for i in range(tm.k):
        utils.get_wordcloud(tm, token_lists, i)
