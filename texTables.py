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
        print'''
\\documentclass{article}
\\usepackage[left=1cm, a0paper]{geometry}
\\usepackage[graphicx]{realboxes}
\\usepackage{bm}
\\begin{document}\n'''
        self.printTable()
        print "\\end{document}"

    def setNames(self, rowNames=None, colmNames=None):
        if len(colmNames) == self.colms:  # This makes top left corner as empty
            colmNames.insert(0, " ")
        elif not(len(colmNames) == self.colms+1):
            print "WARNING: Not all colms have names"
        if not (len(rowNames) == self.rows):
            print "WARNING: Not all rows have names"
        self.rowNames = rowNames
        self.colmNames = colmNames

    def mirror(self):
        # Makes colms->rows and rows->colms
        newArrArr = []
        for a in range(self.colms):
            tmpArr = []
            for b in range(self.rows):
                tmpArr.append(self.mat[b][a])
            newArrArr.append(tmpArr)
        self.mat = np.array(newArrArr)
        self.rowNames, self.colmNames = self.colmNames, self.rowNames
        if self.rowNames:
            self.colmNames.insert(0, self.rowNames[0])
            self.rowNames.pop(0)
        self.rows, self.colms = self.colms, self.rows

    def isValid(self):
        pass

    def __str__(self):
        print "self.mat:\n", self.mat
        print "self.rowNames, self.colmNames:", self.rowNames, self.colmNames
        return "texTable"


def test():
    testA = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    tableObj = texTable(arrayArray=testA)
    colmLabels = ["a", "b", "c"]
    rowLabels = ["d", "e", "f"]
    tableObj.setNames(rowLabels, colmLabels)
    print "\n#####\n"
    print tableObj
    print "\n#####\n"
    tableObj.printTable()
    tableObj.mirror()
    print "\n#####\n"
    tableObj.printTable()

    ta = np.array([[1, 2], [3, 4]])
    tableObj2 = texTable(ta)


if __name__ == "__main__":
    test()
