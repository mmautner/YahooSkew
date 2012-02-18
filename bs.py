from scipy.stats import norm
from scipy.optimize import newton
import numpy as np

# s: stock price       k: Strike Price
# v: volatility(std)   r: risk free rate
# t: time              d: contineous dividend yield

def bs(cflag,s,k,v,r,t):
    d1=(np.log(s/k)+(r+v*v/2)*t)/(v*np.sqrt(t))
    d2=d1-v*np.sqrt(t)
    if cflag:   # call
        return s*norm.cdf(d1) - k*np.exp(-r*t)*norm.cdf(d2)
    else:       # put
        return k*np.exp(-r*t)*norm.cdf(-d2) - s*norm.cdf(-d1)

def delta(cflag,s,k,v,r,t):
    d1=(np.log(s/k)+(r+v*v/2)*t)/(v*np.sqrt(t))
    if cflag:   # call
        return norm.cdf(d1)
    else:       # put
        return norm.cdf(-d1) - 1

def gamma(s,k,v,r,t):
    d1=(np.log(s/k)+(r+v*v/2)*t)/(v*np.sqrt(t))
    return norm.pdf(d1)/(s*v*np.sqrt(t))

def vega(s,k,v,r,t):
    d1=(np.log(s/k)+(r+v*v/2)*t)/(v*np.sqrt(t))
    return s*norm.pdf(d1)*np.sqrt(t)

def theta(cflag,s,k,v,r,t):
    d1=(np.log(s/k)+(r+v*v/2)*t)/(v*np.sqrt(t))
    d2=d1-v*np.sqrt(t)
    if cflag:   # call
        return -s*norm.pdf(d1)*v/(2*np.sqrt(t)) - r*k*np.exp(-r*t)*norm.pdf(d2)
    else:       # put
        return -s*norm.pdf(d1)*v/(2*np.sqrt(t)) + r*k*np.exp(-r*t)*norm.pdf(-d2)
    
def rho(s,k,v,r,t):
    return

def impvol(cflag,s,k,r,t,c,guess,tolerance=0.005,maxnum=1000):
    sigma = guess
    f = lambda x: bs(cflag,s,k,x,r,t)-c
    v = lambda y: vega(s,k,y,r,t)
    sigma = newton(f,guess,fprime=v,tol=tolerance,maxiter=maxnum)
    if sigma <=0:
        sigma = 0
    elif sigma > 1:
        sigma = 0
    return sigma

if __name__=="__main__":
    # cflag, S, K, v, r, dte, dividend
    print "Call:"
    print 'price: ',bs(True, 41.,40.,.3,.08,.25)
    print 'delta: ',delta(True, 41.,40.,.3,.08,.25)
    print 'gamma: ',gamma(41.,40.,.3,.08,.25)
    print 'vega: ',vega(41.,40.,.3,.08,.25)
    print 'theta: ',theta(True, 41.,40.,.3,.08,.25)

    print "\n\nPut:"
    print 'price: ',bs(False, 41.,40.,.3,.08,.25)
    print 'delta: ',delta(False, 41.,40.,.3,.08,.25)
    print 'gamma: ',gamma(41.,40.,.3,.08,.25)
    print 'vega: ',vega(41.,40.,.3,.08,.25)
    print 'theta: ',theta(False, 41.,40.,.3,.08,.25)

