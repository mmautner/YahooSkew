
import urllib2, sys, pdb
import datetime, calendar
import numpy as np
from scipy.stats import norm
from scipy.optimize import newton
import matplotlib.pyplot as plt
from BeautifulSoup import BeautifulSoup
import bs

def yahoo(ticker, year, month):
    """Queries/parses/returns data from Yahoo finance options page

    Argument are all strings, (e.g. 'GOOG', '2012', '03')
    Returns (optionsdata, underlying, timetoexpiration)
    """
    url='http://finance.yahoo.com/q/op?s='+ticker+'&m='+year+'-'+month
    try:
        response=urllib2.urlopen(url)
    except e:
        if hasattr(e,'reason'):
            return ([], 0, 0) # failed to reach server
        elif hasattr(e,'code'):
            return ([], 0, 0) # server couldn't fulfill request
    html = response.read()
    soup = BeautifulSoup(html)
    try:
        underlying = soup.findAll('span', id='yfs_l84_'+ticker.lower())[0].contents[0]
    except Exception, e:
        f = open('notparsed.html','wb')
        f.write(html)
        f.close()
        return ([], 0, 0)
    try:
        underlying = float(underlying)
    except Exception, e:
        print 'value error? '
    options = soup.findAll('table', {'class':'yfnc_datamodoutline1'})
    if len(options)!=2:
        print 'incorrect # of tables with class=\'yfnc_datamodoutline1\'...'
        sys.exit(1)

    # risk-free rate
    r = 0.0

    # pull expiration date (assume market closes 4PM--time-zone?)
    expdate = soup.findAll('table', 
                {'class':'yfnc_mod_table_title1'})[0].findAll("td")[1].contents[0]
    tte = gettte(expdate)

    data = {}
    for i in xrange(len(options)):  # should be just 2 times through (calls/puts)
        trs = options[i].findAll('tr')
        # strike, bid, ask, volume, oi, IV
        x = np.zeros((len(trs)-2,5))
        # first row is th's: 1strike,2symbol,3last,4chg,5bid,6ask,7vol,8oi
        for j in xrange(2,len(trs)):
            tds = trs[j].findAll('td')
            strike = tds[0].findAll('strong')[0].contents[0].replace(',','')
            try: x[j-2,0] = float(strike)
            except: pass
            bid = tds[4].contents[0].replace(',','')
            try: x[j-2,1] = float(bid)
            except: pass
            ask = tds[5].contents[0].replace(',','')
            try: x[j-2,2] = float(ask)
            except: pass
            volume = tds[6].contents[0].replace(',','')
            try: x[j-2,3] = float(volume)
            except: pass
            openinterest = tds[7].contents[0].replace(',','')
            try: x[j-2,4] = float(openinterest)
            except: pass
        data[i] = x
    return (data, underlying, tte)

def gettte(expdate):
    # pull expiration date (assume market closes 4PM--time-zone?)
    expdate = expdate[16:].split(',')
    expdate = [frag.strip() for frag in expdate]
    
    #day
    try: day = int(expdate[1][-2:])
    except: pass #error, unparsed day

    #month
    d = dict((v,k) for k,v in enumerate(calendar.month_abbr))
    month = 0
    for k,v in d.items():
        if k == expdate[1][0:3]:
            month = v
            break
    if  month == 0: pass #error, unparsed month
    
    #year
    try: year = int(expdate[2])
    except: pass #error, unparsed year

    expiration = datetime.datetime(year,month,day,4,0,0)
    td = expiration - datetime.datetime.now()
    daysdiff = float(td.seconds/86400.0 + td.days)
    return daysdiff/365.0

if __name__=="__main__":
    (data,underlying,tte) = yahoo('GOOG', '2012', '03')
