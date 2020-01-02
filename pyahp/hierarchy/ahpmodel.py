# -*- coding: utf-8 -*-
"""pyahp.hierarchy.ahpmodel

This module contains the class definition for the AHP Model Node (root) in the hierarchy model.
"""

import numpy as np

from pyahp.hierarchy import AHPCriterion
from pyahp.methods import EigenvalueMethod
from pyahp.utils import normalize_priorities


class AHPModel:
    """AHPModel

    Args:
        model (dict): The Analytic Hierarchy Process model.
        solver (pyahp.methods): Method used when calculating the priorities of the lower layer.
    """

    def __init__(self, model, solver=EigenvalueMethod):
        self.solver = solver()
        self.preference_matrices = model['preferenceMatrices']

        criteria = model.get('criteria')
        self.criteria = [AHPCriterion(n, model, solver=solver) for n in criteria]

    def get_priorities(self, round_results=True, decimals=3):
        """Get the priority of the nodes in the level below this node.

        Args:
            round_results (bool): Return rounded priorities. Default is True.
            decimals (int): Number of decimals to round to, ignored if `round_results=False`. Default is 3.

        Returns:
            Global priorities of the alternatives in the model, rounded to `decimals` positions if `round_results=True`.
        """
        self.crit_pm = np.array(self.preference_matrices['criteria'])
        self.crit_pr = self.solver.estimate(self.crit_pm)

        self.crit_attr_pr = [criterion.get_priorities() for criterion in self.criteria]
        self.priorities = normalize_priorities(self.crit_attr_pr, self.crit_pr)

        if round_results:
            return np.around(self.priorities, decimals=decimals)

        return self.priorities

    def persist(self, persistance, level=0 ):
        persistance.save("------------ criteria ---------------",key="LEVEL{}".format(level))
        persistance.save( self.crit_pm , key="preference_matrices")
        persistance.save( self.crit_pr , key="priority")
        self.solver.persist( persistance, level+1)
        #persistance.save("------------ subCriteria ---------------",key="LEVEL{}".format(level))
        for criterion in self.criteria:
            persistance.newline();
            criterion.persist(persistance, level+1) 

