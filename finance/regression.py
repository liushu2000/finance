#import pandas as pd
# import numpy as np
from scipy import stats
from xlrd import open_workbook
#from scipy import stats
#from rpy import r
# from numpy import arange,array,ones,linalg
# from pylab import plot,show

data = open_workbook('/home/shu/Downloads/japan_data.xlsx',on_demand=True)
table = data.sheets()[0]
line1 = table.col_values(0)
line2 = table.col_values(1)
gradient, intercept, r_value, p_value, std_err = stats.linregress(line1,line2)
print line1, line2
print "Gradient and intercept", gradient, intercept
# print r.lsfit(x,y)['coefficients']