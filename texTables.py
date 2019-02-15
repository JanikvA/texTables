#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

# TODO allow to instantly create pdf


class texTable(object):
    """This class is supposed to make the creating of tables simple"""

    def __init__(self, npMat=None, arrayArray=None):
        if not (npMat is None):
            self.mat = npMat

        if not (arrayArray is None):
            self.mat = np.array(arrayArray)

        # NOTE mxn matrix: m rows
        self.rows = len(self.mat)
        self.colms = len(self.mat[0])

        self.rowNames = None
        self.colmNames = None

    def printTable(self):
        cString = ("c|"*self.colms)[:-1]
        if self.rowNames:
            cString += "|c"
        tmp = 1
        tableString = '''\\begin{{table}}
\\centering
\\begin{{tabular}}{{{cs}}}
'''.format(cs=cString)
        if self.colmNames:
            for i, n in enumerate(self.colmNames):
                tableString += n + " & "
                if i == self.colms:
                    tableString = tableString[:-2]+"\\\\\n"
                    tableString += "\\hline\n"
        rowNameIndex = 0
        for i, e in enumerate(np.nditer(self.mat)):

            if self.rowNames and tmp == 1:
                tableString += self.rowNames[rowNameIndex] + " & "
                rowNameIndex += 1
            tableString += str(e) + " & "
            if tmp == self.colms:
                tmp = 1
                tableString = tableString[:-2]+"\\\\\n"
            else:
                tmp += 1
        tableString += '''\\end{tabular}
\\end{table}
'''
        print tableString

    def printStandalone(self):
        pass

    def setNames(self, rowNames=None, colmNames=None):
        self.rowNames = rowNames
        self.colmNames = colmNames

    def isValid(self):
        pass

    def __str__(self):
        print "self.mat:\n", self.mat
        print "self.rowNames, self.colmNames:", self.rowNames, self.colmNames
        return "texTable"


def test():
    testA = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    tableObj = texTable(arrayArray=testA)
    colmLabels = [" ", "a", "b", "c"]
    rowLabels = ["d", "e", "f"]
    tableObj.setNames(rowLabels, colmLabels)
    print tableObj
    tableObj.printTable()

    ta = np.array([[1, 2], [3, 4]])
    tableObj2 = texTable(ta)


if __name__ == "__main__":
    test()
