import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def back_testing(classifier, t_tracking, testing_set, spread, int_rate, trade_init, history, predictive_clust):
    """
    Runs a backtestinf of the classification model during the testing period
    :param classifier: the clustering model
    :param t_tracking: the time of tracking if a cluster once it's recognized
    :param testing_set: the dataset used for testing(normalized and encoded)
    :param trade_init: number of initial trades
    :param history: pandas' dataframe containing the period of testing
    :param predictive_clust: the numbers of predictive clusters
    :return: variation of equity, leverage buy & sell, sortino ratio and a pandas' dataframe 'briefing' containing the orders made
    """
    N = testing_set.shape[0]-t_tracking
    briefing = pd.DataFrame(columns = ['date', 'position', 'buy price', 'sell price', 'PnL' ])
    equity =[history['open'].iloc[0] * trade_init]*N
    leverage_buy = [0]*N
    leverage_sell = [0]*N

    long = []
    short = []
    pips_spread_long = []
    pips_spread_short = []

    pos = 0
    neg = 0

    for t in range(0, N-t_tracking, t_tracking):
        nb_cluster = classifier.predict(np.array(testing_set[t]).reshape(1,-1)) #Il faut savoir quoi mettre ici selon la structure de l'autoencod
        if nb_cluster in predictive_clust:
            pip = history['open'].iloc[t+t_tracking]/history['open'].iloc[t] -1
            PnL = equity[t]*(pip - spread)
            equity[t] += PnL

            long.append(PnL)
            pips_spread_long.append(pip - spread)

            equity = equity[:t+1] + [e + PnL for e in equity[t+1:]]
            briefing.loc[len(briefing)] = [history['date'].iloc[t], 'buy', history['open'].iloc[t], history['close'].iloc[t+t_tracking], PnL]
            leverage_buy = [leverage_buy[i] + 0.1 if i in range(t, t+t_tracking) else leverage_buy[i] for i in range(len(leverage_buy))]
        elif -nb_cluster in predictive_clust:
            pip = history['open'].iloc[t+t_tracking]/history['open'].iloc[t] -1
            if pip > 0:
                pos += 1
            else:
                neg += 1

            PnL = equity[t]*(pip + spread)
            equity[t] += PnL

            short.append(PnL)
            pips_spread_short.append(pip + spread)

            equity = equity[:t+1] + [e + PnL for e in equity[t+1:]]
            briefing.loc[len(briefing)] = [history['date'].iloc[t], 'sell', history['open'].iloc[t], history['close'].iloc[t+t_tracking], PnL]
            leverage_sell = [leverage_sell[i] - 0.1 if i in range(t, t+t_tracking) else leverage_sell[i] for i in range(len(leverage_buy))]

    print("POSITIVE PIPS: ", pos)
    print("NEGATIVE PIPS: ", neg)
    print("TOTAL: ", pos + neg )


    long_short_relation = sum(long) / sum(short)
    sum_long = sum(long)
    sum_short = sum(short)
    mean_long = np.mean(long)
    mean_short = np.mean(short)
    max_pips_long = max(pips_spread_long)
    min_pips_long = min(pips_spread_long)
    mean_pips_long = np.mean(pips_spread_long)
    max_pips_short = max(pips_spread_short)
    min_pips_short = min(pips_spread_short)
    mean_pips_short = np.mean(pips_spread_short)

    spread_params = [long_short_relation, sum_long, sum_short, mean_long, mean_short,
                     max_pips_long, min_pips_long, mean_pips_long,
                     max_pips_short, min_pips_short, mean_pips_short]

    return equity, leverage_buy, leverage_sell, briefing, spread_params

def max_drawdown(equity:list):
    """
    Mesure le max drawdown, la perte maximale encaissée, du portefeuille
    """
    maxi = 0
    j=1
    while j<len(equity):
        if equity[j]<equity[j-1]:
            i = j
            while  i<len(equity) and equity[i] < equity[i-1]:
                i+=1
            maxi = max(maxi, (equity[j-1]-equity[i-1])/equity[j-1])
            j = i
        else:
            j+=1
    return maxi


########################## Not USED FUNCTION IN THE MODEL###########################################


def plot_backtest(equity, leverage_b, leverage_s):
    """
    Plots the backtesting results
    """
    plt.subplot(1, 2, 1)
    plt.plot(equity, color='r')
    plt.xlabel("time")
    plt.ylabel("Equity")
    plt.grid()
    plt.title('Equity overtime')

    plt.subplot(1, 2, 2)
    leverage = [sum(x) for x in zip(leverage_b, leverage_s)]
    plt.plot(leverage, color='r')
    plt.xlabel("time")
    plt.ylabel("Leverage")
    plt.grid()
    plt.title('Leverage overtime')

    plt.savefig("Backtesting_plot")

