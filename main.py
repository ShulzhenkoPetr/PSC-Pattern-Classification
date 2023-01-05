import sys

sys.path.append('./functions')

from run import *
from pdf import *
from gen_check import *
import csv
import argparse


def generalization_check(run_args: list) -> None:
    output_list = gen_check(*run_args)

    if output_list[1]:
        output = {"First part Return": output_list[0], "Second part Return": output_list[1]}

        with open(f'/content/gdrive/My Drive/Data/FRA40_Gen_check.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=output.keys())
            writer.writerow(output)

    #return output_list[1] is not None
    with open('/content/PSC-Pattern-Classification/gen_chek_bool.txt', 'w') as f:
        f.write(str(output_list[1] is not None))

def result(run_args: list) -> None:
    output = run(*run_args)

    with open(f'/content/gdrive/My Drive/Data/{run_args[2]}.csv', 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=output.keys())
        writer.writerow(output)


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

run_args = [path, index0, index, date_start, date_end_train, date_end_test, nb_clusters, longueur, echantillon, n_in,
             latent_dim, input_dim,seuil, nb_iter, t_tracking, min_pip, min_element, spread,
             int_rate, trade_init]

generalization_check(run_args)

#BACKTEST_REPORT(output)
