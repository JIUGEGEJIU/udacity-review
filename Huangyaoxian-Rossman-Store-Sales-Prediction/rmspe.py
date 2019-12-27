import numpy as np

def rmspe(y, y_hat):
    return np.sqrt(np.mean((y_hat/y-1) ** 2))

def rmspe_xg(y_hat, y):
    y = np.expm1(y.get_label())
    y_hat = np.expm1(y_hat)
    return "rmspe", rmspe(y, y_hat)