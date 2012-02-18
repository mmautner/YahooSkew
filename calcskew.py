
import pdb
import warnings
with warnings.catch_warnings():
    warnings.filterwarnings("ignore")

import datetime as dt
import calendar
import numpy as np
import matplotlib.pyplot as plt
import pulldata,bs

def impvol(cflag, underlying, strikes, prices, r, tte, d=0):
    iv = np.zeros(len(strikes))
    guess = 0.2
    for row in xrange(len(strikes)):
        iv[row] = bs.impvol(cflag, underlying, strikes[row], r, tte, 
                            prices[row], guess)
        if iv[row]:
            guess = iv[row]
    return iv

if __name__=="__main__":
    ticker = 'GOOG'
    now = dt.datetime.now()
    d = dict((v,k) for k,v in enumerate(calendar.month_abbr))
    expirations = (('2012','06'),)
    for (year,month) in expirations:
        (data,underlying,tte) = pulldata.yahoo(ticker, year, month)
    r = 0.005
    plt.figure()
    
    for i in [0,1]:
        if i==0:
            stk = data[i][np.nonzero(data[i][:,0] > underlying),0][0]
            bid = data[i][np.nonzero(data[i][:,0] > underlying),1][0]
            ask = data[i][np.nonzero(data[i][:,0] > underlying),2][0]
        else:
            stk = data[i][np.nonzero(data[i][:,0] < underlying),0][0]
            bid = data[i][np.nonzero(data[i][:,0] < underlying),1][0]
            ask = data[i][np.nonzero(data[i][:,0] < underlying),2][0]

        # ignore teenies
        filterInd = np.nonzero(bid > 1)
        stk = stk[filterInd[0]]
        bid = bid[filterInd[0]]
        ask = ask[filterInd[0]]

        bidIV = impvol(i-1, underlying, stk, bid, r, tte)
        askIV = impvol(i-1, underlying, stk, ask, r, tte)

        # ignore zero-vol's
        filterInd = np.nonzero(bidIV != 0)
        stk = stk[filterInd[0]]
        bidIV = bidIV[filterInd[0]]
        askIV = askIV[filterInd[0]]
        filterInd = np.nonzero(askIV != 0)
        stk = stk[filterInd[0]]
        bidIV = bidIV[filterInd[0]]
        askIV = askIV[filterInd[0]]
        plt.plot(stk,bidIV,'b.')
        plt.plot(stk,askIV,'r.')

    plt.xlabel('Strike', fontsize=14)
    plt.ylabel('Implied Volatility', fontsize=14)
    plt.title('GOOG June \'12 Skew')
    plt.show()
        


