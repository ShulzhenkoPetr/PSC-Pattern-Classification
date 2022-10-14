import sys

sys.path.append('./functions')

from run import *
from pdf import *

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--index_type', type=str, required=True, help='Type of index: FOREX / NONFOREX')
parser.add_argument('--index', type=str, required=True, help='index to use')
parser.add_argument('--nb_clusters', type=int)
parser.add_argument('--date_start', type=str, help='Y-M-D H:M:S')
parser.add_argument('--date_end_train', type=str, help='Y-M-D H:M:S')
parser.add_argument('--date_end_test', type=str, help='Y-M-D H:M:S')
args = parser.parse_args()

path = "/Users/petrshulzhenko/psc/Code-2/"
index0 = args.index_type
index = args.index
date_start = args.date_start or '2012-01-06 07:00:00'
date_end_train = args.date_end_train or '2016-01-06 07:00:00'
date_end_test = args.date_end_test or '2017-01-06 07:00:00'
nb_clusters = args.nb_clusters or 100
# 100 meilleur choix
longueur = 8
echantillon = 8

n_in = echantillon
latent_dim = 3
input_dim = 1

seuil = 0.4
nb_iter = 25

t_tracking = 20
min_pip = 0.05
min_element = 45
spread = 0.01
int_rate = 0.1
trade_init = 10

output = run(path, index0, index, date_start, date_end_train, date_end_test, nb_clusters, longueur, echantillon, n_in=8,
             latent_dim=3, input_dim=1,
             seuil=seuil, nb_iter=nb_iter, t_tracking=t_tracking, min_pip=min_pip, min_element=min_element, spread=0.01,
             int_rate=0.1, trade_init=10)

#output = {'third': random.randint(0,10), 'forth': args.nb_clusters or nb_clusters}
#import pandas as pd
#df = pd.DataFrame.from_dict(output)
#df.to_csv(f'{args.index}.csv', header=output[0].keys())

import csv

with open(f'/content/gdrive/My Drive/Data/{args.index}.csv', 'a', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=output.keys())
    writer.writerow(output)

#BACKTEST_REPORT(output)
