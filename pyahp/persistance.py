# -*- coding: utf-8 -*-
"""pyahp.methods.eigenvalue

This module contains the class implementing the eigenvalue priority estimation method.
"""

class Persistance:
    def __init__(self, indents="        "):
        self.indents=indents

    def newline(self):
        print("\n")

    def save( self, value, level=0, key="" ):
        indents = self.indents*level
        if not key:
            key = "none"
        print(indents, key, "=",value)

