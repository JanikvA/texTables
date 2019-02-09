#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

# TODO allow to set labels for colms or rows
# TODO implement support for popular moduls like panda
# TODO allow to instantly create pdf


class texTable(object):
    """This class is supposed to make the creating of tables simple"""

    def __init__(self, npMat=None, arrayArray=None):
        if not (npMat is None):
            self.mat=npMat

        if not (arrayArray is None):
            self.mat=np.array(arrayArray)

        #NOTE mxn matrix: m rows
        self.rows=len(self.mat)
        self.colms=len(self.mat[0])

    def printTable(self):
        cString=("c|"*self.colms)[:-1]
        tmp=1
        tableString='''\\begin{{table}}
   \\centering
   \\begin{{tabular}}{{{cs}}}
'''.format(cs=cString)
        for e in np.nditer(self.mat):
            tableString+=str(e) + " & "
            if tmp==self.colms:
                tmp=1
                tableString=tableString[:-2]+"\\\\\n"
            else:
                tmp+=1
        tableString+='''   \\end{tabular}
\\end{table}
'''
        print tableString


    def printStandalone(self):
        pass

    def setNames(self, rowNames=None, colmNames=None):
        pass

    def isValid(self):
        pass


    def __str__(self):
        print "self.mat:\n",self.mat
        return "texTable"


def test():
    testA=[[1,2,3],[4,5,6],[7,8,9]]
    tableObj=texTable(arrayArray=testA)
    print tableObj
    tableObj.printTable()



    ta=np.array([[1, 2], [3, 4]])
    tableObj2=texTable(ta)


if __name__ == "__main__":
    test()
