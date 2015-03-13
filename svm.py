__author__ = 'Yu Zhao'
from scipy import sparse

def getMatrixFromNormalizedEmailList(emaiList, wordList):
    t = []
    for i in emaiList:
        tmp = [ word in i for word in wordList ]
        t.append(tmp)
    return sparse.csr_matrix(t)