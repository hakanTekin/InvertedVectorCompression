#import numpy
from io import TextIOWrapper
import math
from os import replace, stat_result
from typing import Text
from bitstream import BitStream
from golomb_coding import golomb_coding
from golomb import encode, decode

#The code is set to run for normal crawl dataset
dv_file_mod = 0 #1 for 16 proc, 0 for crawl.dv files
doc_file = 'crawl.docs' #'crawl.16proc0.docs'
terms_file = 'crawl.terms' #'crawl.16proc0.terms'
dv_0_file = 'crawl.DV.0' #'crawl.16proc0.DV'
dv_1_file = 'crawl.DV.1'
"""
Hakan Ahmet Tekin
CMPE 414 Project 2
"""

#I have only tried the 16proc0 dataset since the machine I am working on is quite slow

"""
This program creates an Inverted Document Vector file IDV. Then it compresses the file and creates IDV.compressed.


For creating the IDV file, dictionaries are used to store each word.
Then, the documents these words appear in are recorded to the relevand dictionary entry.
After the dictionary is completely built, it is written line by line to the .IDV file


For compression, golomb encoding is used with a few different operations
1- The document ID's are sorted in ascending order
2- The golomb values are replaced with a number that adds up to the original ID when all the previous numbers are summed together
    2-1- If the ID's are : 1 5 21, then the replacement array is : 1 4 16
3- The new values are converted to golomb code(a string of 0's and 1's) one by one with a constant value of 1000
4- The golomb codes are replaced with index values that show where each 1 is located in. Since there are very little 1's in a golomb code, this part helps shorten the resulting file by a lot.
    4-1- If the golomb code is 000101, then the replacement value is 35 (1's are in index 3 and 5)
5- the resulting values are written to file IDV.compressed

The code itself is relatively short, but I have tried several approaches to be able to compress the file (finding a suitable approach took most of the time in this project).
"""

'''
This method recieves a string and finds the 1's inside, then writes the indexes of ones to the IDV.compressed file
'''
def write_index_ones(a, f:TextIOWrapper):
    previous_index = 0
    # print(f'i: {i} \n')
    for x in a:
        val = golomb_coding(x,1000)
        index = 0
        previous_index = 0
        while True:
            index = val.find("1", index+1, len(val))
            if index==-1:
                break
            f.write(f'{index-previous_index+1}')    
            previous_index = index+1
        f.write('.')
    f.write('\n')


golomb_constant = 1000

'''
Converts a dictionary entry with document id's into an array of indexes (of 1's) created from the golomb codes, then sends that array to the write_index_ones method
''' 
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
            write_index_ones(z,golombFile)


'''
Basically the main method, each step of the project is executed from this method, in the python scirpt, only this method is called.
'''
def mainline():
    kvp = dict()

    with open(terms_file, 'r') as file:
        for l in file:
            arr = l.split(' ')
            kvp[ int(arr[1]) ] = []
        print('x')
    if dv_file_mod == 1:
        with open('crawl.16proc0.DV') as dvfile:
            docindex = 1
            for l in dvfile:
                arr = l.split(' ')
                i = 1
                while i < arr.__len__():
                    kvp[ int(arr[i]) ].append(docindex)
                    i+=2
                docindex+=1
    elif dv_file_mod == 0:
        with open(dv_0_file) as dvfile:
            docindex = 1
            for l in dvfile:
                arr = l.split(' ')
                i = 1
                while i < arr.__len__():
                    kvp[ int(arr[i]) ].append(docindex)
                    i+=2
                docindex+=1
        with open(dv_1_file) as dvfile:
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
            y = kvp[i]
            y.sort()
            newfile.write(f'{len(kvp)/2}')
            for x in y:
                newfile.write(f' {x}')
            newfile.write('\n')
        print('yy')

    with open('crawl.16proc0.IDV', 'r') as f: 
        golomb_with_sum(f)
mainline()