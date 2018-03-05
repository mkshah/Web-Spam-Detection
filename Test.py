import os, copy 
import numpy as np
import xlrd
import xlwt
import xlutils
from xlrd import open_workbook
from xlwt import Workbook

os.chdir('C:\\Users\\Samsung\\Desktop\\BITS PILANI\\YEAR-2 SEM-2\\Projects')

M = np.zeros((11402,11402))

data = open_workbook('cd.xlsx')
sh0 = data.sheet_by_index(0)

for i in range(11402):
    for j in range(11402):
        M[i][j] = sh0.cell_value(i,j)