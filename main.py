#import numpy
from io import TextIOWrapper
import math
from os import replace, stat_result
from typing import Text
from bitstream import BitStream
from golomb_coding import golomb_coding
from golomb import encode, decode

def get_ones(a, f:TextIOWrapper):
    max = 0
    # print(f'i: {i} \n')
    for x in a:
        gol = golomb_coding(x,1000)
        index = 0
        max = 0
        while (index<len(gol)-1):
            index = gol.find("1",max,len(gol))
            if(index==-1):
                break
            else:
                f.write(f'{(index+1)-max}-')
                
                max = index+1
        # file_craw_IDV_compressed.write(f'{len(gol)-max}. ')
        f.write('.')
    f.write('\n')


golomb_constant = 1000
def golomb_with_sum(idvFile:TextIOWrapper):
    with open('crawl.16proc0.IDV.compressed', 'w') as golombFile: #open in binary form
        count = 0
        for l in idvFile:
            s = l.split(' ')
            ss = []
            for i in range(1,s.__len__(),1):
                ss.append(int(s[i]))
            sum = 0
            z = []
            for i in range(ss.__len__()):
                z.append(ss[i] - sum)
                sum += ss[i]-sum
            get_ones(z,golombFile)

def mainline():
    kvp = dict()

    with open('crawl.16proc0.terms', 'r') as file:
        for l in file:
            arr = l.split(' ')
            kvp[ int(arr[1]) ] = []
        print('x')

    with open('crawl.16proc0.DV') as dvfile:
        docindex = 1
        for l in dvfile:
            arr = l.split(' ')
            i = 1
            while i < arr.__len__():
                kvp[ int(arr[i]) ].append(docindex)
                i+=2
            docindex+=1

    with open('crawl.16proc0.IDV', 'w+') as newfile:
        for i in range(0,len(kvp)):
            y = kvp[i].sort()
            newfile.write(f'{len(kvp)/2}')
            for x in y:
                newfile.write(f' {x}')
            newfile.write('\n')
        print('yy')

with open('crawl.16proc0.IDV', 'r') as f: 
    golomb_with_sum(f)