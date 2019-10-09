#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import numpy as np
import os


class texTable(object):
    # This class is supposed to make the creating of tables simple

    # Dependencies: numpy
    # os+pdflatex for creating pdf output

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

    def getTableString(self, rotate=False):
        cString = ("c|" * self.colms)[:-1]
        if self.rowNames:
            cString += "|c"
        tmp = 1
        tableEnv = "table"
        if rotate:
            tableEnv = "sidewaystable"
        tableString = '''\\begin{{{tabEnv}}}
\\centering
\\begin{{tabular}}{{{cs}}}
'''.format(cs=cString, tabEnv=tableEnv)
        if self.colmNames:
            for i, n in enumerate(self.colmNames):
                tableString += n + " & "
                if i == self.colms:
                    tableString = tableString[:-2] + "\\\\\n"
                    tableString += "\\hline\n"
        rowNameIndex = 0
        for i, e in enumerate(np.nditer(self.mat)):
            if self.rowNames and tmp == 1:
                tableString += self.rowNames[rowNameIndex] + " & "
                rowNameIndex += 1
            tableString += str(e) + " & "
            if tmp == self.colms:
                tmp = 1
                tableString = tableString[:-2] + "\\\\\n"
            else:
                tmp += 1
        tableString += '''\\end{{tabular}}
\\end{{{tabEnv}}}
'''.format(tabEnv=tableEnv)
        return tableString

    def getStandaloneTable(self, big=False, rotate=False):
        tmpString = "\\documentclass{article}"
        if big:
            tmpString += '''\\usepackage[left=1cm, a0paper]{geometry}\n'''
            if rotate:
                tmpString += "\\usepackage{rotating}\n"
        tmpString += "\\begin{document}\n"
        tmpString += self.getTableString(rotate=rotate)
        tmpString += "\\end{document}"
        return tmpString

    def setNames(self, rowNames=None, colmNames=None, compatible=False):
        if len(colmNames) == self.colms:  # This makes top left corner as empty
            colmNames.insert(0, " ")
        elif not (len(colmNames) == self.colms + 1):
            print "WARNING: Not all colms have names"
            print len(colmNames), self.colms
        if not (len(rowNames) == self.rows):
            print "WARNING: Not all rows have names"
            print len(rowNames), self.rows
        if compatible:
            for r in range(len(rowNames)):
                rowNames[r] = rowNames[r].replace("_", " ")
            for r in range(len(colmNames)):
                colmNames[r] = colmNames[r].replace("_", " ")
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

    def createPDF(self, fileName="table", clean=False, big=False,
                  rotate=False):
        # Needs pdflatex
        texName = fileName + ".tex"
        if os.path.isfile(texName):
            print texName, "Already exists!"
            decision = raw_input("Are you sure you want to overwrite it?[y/n]")
            if not (decision == "y"):
                return
        texFile = open(texName, "w")
        texFile.write(self.getStandaloneTable(big=big, rotate=rotate))
        texFile.close()
        # os.system("pdflatex -halt-on-error {} &> /dev/null".format(texName))
        os.system("pdflatex {}".format(texName))
        if clean:
            os.system("rm {a}.log {a}.tex {a}.aux".format(a=fileName))
