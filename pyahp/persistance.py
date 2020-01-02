# -*- coding: utf-8 -*-
"""pyahp.methods.eigenvalue

This module contains the class implementing the eigenvalue priority estimation method.
"""

import csv
import numpy as np

class Persistance:
    def __init__(self, indents="        ", path="./result.csv"):
        self.indents=indents
        self.path=path
        self.f = open( self.path, "w",newline="")
        self.f.write('\ufeff')
        self.f_csv = csv.writer(self.f,dialect='excel')

    def newline(self):
        self.f_csv.writerow([])
        print("\n")

    def save( self, value, level=0, key="" ):
        indents = self.indents*level
        if not key:
            key = "none"
#        print(type(value))
        print(indents, key, "=",value)
        if isinstance( value, np.ndarray ):
            self.f_csv.writerow([None]*level+["{} =".format(key)])
            if len(value.shape) ==1 :
                self.f_csv.writerow([None]*level+value.tolist())
            else:
                for row in value.tolist():
                    self.f_csv.writerow([None]*level+row)
        else:
            self.f_csv.writerow([None]*level+["{} =".format(key),value])

