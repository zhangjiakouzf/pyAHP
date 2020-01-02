# -*- coding: utf-8 -*-
"""pyahp.methods.eigenvalue

This module contains the class implementing the eigenvalue priority estimation method.
"""

import numpy as np
from scipy.sparse.linalg import eigs

from pyahp.methods import Method

RANDOM_INDICES = [0, 0, 0.58, 0.9, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49, 1.51]

class ConsistencyRatio:
    @staticmethod
    def _evaluate_consistency(width):
        if width > len(RANDOM_INDICES):
            return 0

        return RANDOM_INDICES[width - 1]

    def __init__(self, threshold):
        self.threshold =threshold 
        self.result = True
        self.CR=0

    def estimate(self, lamda_, width, real_vector):
        #print("Σ={}".format(sum_vector))
        #print("ω'={}".format(real_vector))
        #print("ω={}".format(w))
        #print("λmax={}".format(lamda_))
        #print("C.I.=(λ(max)-n)/(n-1)={}".format(CI))
        #print("R.I.={}".format(RI))
        #print("C.R.={} < 0.1".format(CI/RI if RI !=0 else 0.00))
        self.CI=(lamda_-width)/(width-1)
        self.RI=self._evaluate_consistency(width)
        if self.RI:
            self.CR = self.CI/self.RI
            if self.CR >= self.threshold :
                result = False
                raise AHPConsistencyError(self.threshold, self.CI, self.RI, self.CR)

    def persist(self, persistance, level ):
        persistance.save( level=level, value=self.CI,key="CI" )
        persistance.save( level=level, value=self.RI,key="RI" )
        persistance.save( level=level, value=self.CR,key="CR" )
        persistance.save( level=level, value=self.threshold,key="threshold" )
        persistance.save( level=level, value=self.result,key="Result" )


class EigenvalueMethod(Method):
    """Eigenvalue based priority estimation method
    """
    def __init__(self):
        pass

    def estimate(self, preference_matrix):
        super()._check_matrix(preference_matrix)
        self.width = preference_matrix.shape[0]

        #_, vectors = eigs(preference_matrix, k=(width-2) if (width-2) >0 else 1, sigma=width, which='LM', v0=np.ones(width))
        #_, vectors = eigs(preference_matrix,  sigma=width, which='LM', v0=np.ones(width))
        _, vectors = np.linalg.eig(preference_matrix)#, k=(width-2) if (width-2) >0 else 1, sigma=width, which='LM', v0=np.ones(width))

        self.real_vector = np.real([vec for vec in np.transpose(vectors) if not np.all(np.imag(vec))][:1])

        self.lamda_ = np.real(_[0])
        self.CR = ConsistencyRatio(0.01)
        self.CR.estimate(self.lamda_, self.width, self.real_vector) 

        self.sum_vector = np.sum(self.real_vector)
        self.normal_vector = np.around(self.real_vector, decimals=3)[0] / self.sum_vector
        return self.normal_vector 

    def persist(self, persistance, level ):
        persistance.save( level=level, value=self.width, key="n")
        persistance.save( level=level, value=self.lamda_, key="λmax" )
        self.CR.persist( persistance , level+1 )
        persistance.save( level=level, value=self.sum_vector, key="Σ")
        persistance.save( level=level, value=self.real_vector, key="ω'")
        persistance.save( level=level, value=self.normal_vector, key="ω")
