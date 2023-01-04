from preprocessing import *
from encoder import *
from clusters import *
from prediction import *
from backtesting import *
from datetime import datetime
import numpy as np


def run_backtesting(Kmeans, encoder_model, pred_indexes, path, index0, index, date_start, date_end_train, date_end_test, nb_clusters, longueur, echantillon, n_in, latent_dim, input_dim,
         seuil, nb_iter, t_tracking, min_pip, min_element, spread=0.01, int_rate=0.1, trade_init=10,) -> dict:

    history_test = History(path + 'marketdata.db', index, date_end_train, date_end_test)

    dates_test, data_test = process_data(history_test, longueur, echantillon, input_dim, 'open')
    data_test_encoded = encoder_model.predict(data_test)
    equity, leverage_buy, leverage_sel, briefing = back_testing(Kmeans,
                                                                t_tracking=t_tracking,
                                                                testing_set=data_test_encoded,
                                                                spread=spread,
                                                                int_rate=int_rate,
                                                                trade_init=trade_init,
                                                                history=history_test,
                                                                predictive_clust=pred_indexes)
    maxdrawdown = max_drawdown(equity)
    bench_return = (history_test['open'].iloc[len(history_test) - 1] / history_test['open'].iloc[0] - 1)

    output = {}
    output["SYMBOL"] = index
    output["START_DATE"] = date_end_train
    output["END_DATE"] = date_end_test
    output["DATES"] = [date_start, date_end_train, date_end_test]
    output["SPREAD"] = spread
    output["N_CLUSTERS"] = nb_clusters
    output["PREDICTIVE_CLUSTERS"] = len(pred_indexes)
    output["RETURN"] = (equity[-1] / equity[0] - 1) * 100
    output["MIN_PIPS"] = min_pip
    output["N_TRADE"] = len(briefing)
    output["WIN_RATE"] = len(briefing.loc[briefing["PnL"] > 0]) / len(briefing)
    output["MAX_DRAWDOWN"] = maxdrawdown
    s = datetime.strptime(date_end_train, '%Y-%m-%d %H:%M:%S')
    e = datetime.strptime(date_end_test, '%Y-%m-%d %H:%M:%S')
    output["SHARPE"] = (equity[-1] - equity[0] - (1.01 ** ((e - s).days // 365) - 1) * equity[0]) / np.array(
        equity).std()
    output["PATH"] = path
    output["BENCHMARK_RETURN"] = bench_return * 100

    return output


def gen_check(path, index0, index, date_start, date_end_train, date_end_test, nb_clusters, longueur, echantillon, n_in, latent_dim, input_dim,
         seuil, nb_iter, t_tracking, min_pip, min_element, spread=0.01, int_rate=0.1, trade_init=10) -> list:

    print("#################PREPOCESSING DATA...#####################")
    his = History(path+'marketdata.db', index, date_start, date_end_train)
    dates_set, data_set = process_data(his, longueur, echantillon, input_dim, 'open')
    # Encoding data
    encoder_model, decoder_model, model = encoder(n_in, latent_dim, input_dim)
    model_history = model.fit(data_set, data_set, validation_split=0.05, epochs=40, batch_size=130, verbose=0, shuffle=True)
    data_set_encoded = encoder_model.predict(data_set)
    print("#################PREPOCESSING DONE#####################")


    print("#################BUILDING THE CLASSIFIER...#####################")

    Kmeans = nRaffinements(5, nb_clusters, seuil, data_set_encoded)
    Kmeans.fit(data_set_encoded)
    print("#################CLASSIFIER IS READY#####################")


    print("#################FILTERING CLUSTERS...#####################")
    clusters_dates = cluster_dates(Kmeans, np.array(dates_set))

    pred_indexes_beta = predictive_index_1(Kmeans, clusters_dates, his, t_tracking=t_tracking, min_pip=min_pip, inde=index0)
    indexes_2 = [k for k, v in clusters_dates.items() if len(v) > min_element]
    pred_indexes = [ind for ind in pred_indexes_beta if np.abs(ind) in indexes_2]
    #pred_indexes = predictive_indexe_2(Kmeans,  pred_indexes_beta, min_element=min_element)
    print("#################FILTERATION DONE#####################")

    print("#################RUNNING BACKTEST...#####################")

    x = '2016-01-06 07:00:00'
    y = '2017-01-06 07:00:00'

    x_d = datetime.strptime(x.split(' ')[0], '%Y-%m-%d')
    y_d = datetime.strptime(y.split(' ')[0], '%Y-%m-%d')
    print(x_d + 0.5 * (y_d - x_d))

    date_first_test_start = date_end_train
    mid = datetime.strftime(datetime.strptime(date_first_test_start.split(' ')[0],'%Y-%m-%d') + 0.5 * (datetime.strptime(date_end_test.split(' ')[0],'%Y-%m-%d') - datetime.strptime(date_first_test_start.split(' ')[0],'%Y-%m-%d')), '%Y-%m-%d')
    date_first_test_end = f"{mid} 07:00:00"
    date_second_test_end = date_end_test

    output_1 = run_backtesting(Kmeans, encoder_model, pred_indexes, path, index0, index, date_start, date_end_train, date_first_test_end, nb_clusters, longueur, echantillon, n_in, latent_dim, input_dim,
         seuil, nb_iter, t_tracking, min_pip, min_element, spread=0.01, int_rate=0.1, trade_init=10)

    if output_1["RETURN"] > 0:
        output_2 = run_backtesting(Kmeans, encoder_model, pred_indexes, path, index0, index, date_start, date_first_test_end, date_second_test_end, nb_clusters, longueur, echantillon, n_in, latent_dim, input_dim,
         seuil, nb_iter, t_tracking, min_pip, min_element, spread=0.01, int_rate=0.1, trade_init=10)
        return [output_1, output_2]
    else:
        print(f"#################RETURN was equal to {output_1['RETURN']} #####################")





