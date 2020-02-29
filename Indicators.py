import numpy as np
import warnings
warnings.simplefilter("ignore")


# Few indicators you can use to build your own strategy

def SMA(data, period):
    return [np.mean(data[idx - (period - 1):idx+1]) for idx in range(0, len(data))]


def ALMA(data, period, offset, sigma):
    m = np.floor(offset * (period - 1))
    s = period / sigma
    alma = np.zeros(data.shape)
    w_sum = np.zeros(data.shape)

    for i in range(len(data)):
        if i < period-1:
            continue
        else:
            for j in range(period):
                w = np.exp(-(j - m) * (j - m) / (2 * s * s))
                alma[i] += data[i - period + j] * w
                w_sum[i] += w
            alma[i] = alma[i] / w_sum[i]

    return alma


def VWMA(data, vol, period):
    sma_data_vol = SMA(data * vol, period)
    sma_vol = SMA(vol, period)
    vwma = [sma_data_vol[i] / sma_vol[i] for i in range(0, len(data))]
    return vwma


def parabolic_sar(new, start, increment, stop):
    initial_af = start
    step_af = increment
    end_af = stop
    new.reset_index(inplace=True)

    new['trend'] = 0
    new['sar'] = 0.0
    new['real sar'] = 0.0
    new['ep'] = 0.0
    new['af'] = 0.0

    new['trend'][1] = 1 if new['Close'][1] > new['Close'][0] else -1
    new['sar'][1] = new['High'][0] if new['trend'][1] > 0 else new['Low'][0]
    new.at[1, 'real sar'] = new['sar'][1]
    new['ep'][1] = new['High'][1] if new['trend'][1] > 0 else new['Low'][1]
    new['af'][1] = initial_af

    for i in range(2, len(new)):

        temp = new['sar'][i - 1] + new['af'][i - 1] * (new['ep'][i - 1] - new['sar'][i - 1])
        if new['trend'][i - 1] < 0:
            new.at[i, 'sar'] = max(temp, new['High'][i - 1], new['High'][i - 2])
            temp = 1 if new['sar'][i] < new['High'][i] else new['trend'][i - 1] - 1
        else:
            new.at[i, 'sar'] = min(temp, new['Low'][i - 1], new['Low'][i - 2])
            temp = -1 if new['sar'][i] > new['Low'][i] else new['trend'][i - 1] + 1
        new.at[i, 'trend'] = temp

        if new['trend'][i] < 0:
            temp = min(new['Low'][i], new['ep'][i - 1]) if new['trend'][i] != -1 else new['Low'][i]
        else:
            temp = max(new['High'][i], new['ep'][i - 1]) if new['trend'][i] != 1 else new['High'][i]
        new.at[i, 'ep'] = temp

        if np.abs(new['trend'][i]) == 1:
            temp = new['ep'][i - 1]
            new.at[i, 'af'] = initial_af
        else:
            temp = new['sar'][i]
            if new['ep'][i] == new['ep'][i - 1]:
                new.at[i, 'af'] = new['af'][i - 1]
            else:
                new.at[i, 'af'] = min(end_af, new['af'][i - 1] + step_af)
        new.at[i, 'real sar'] = temp

    sar = new
    del sar['real sar'], sar['ep'], sar['af'], sar['trend']
    sar.set_index('index', inplace=True)
    return sar
