# -*- coding: utf-8 -*-
"""pyahp.hierarchy.ahpcriterion

This module contains the class definition for the AHP Criteria Node in the hierarchy model.
"""

import numpy as np

from pyahp.methods import EigenvalueMethod
from pyahp.utils import normalize_priorities


class AHPCriterion:
    """AHPCriterion

    Args:
        name (str): Name of the criterion this node resembles.
        model (dict): The Analytic Hierarchy Process model.
        solver (pyahp.methods): Method used when calculating the priorities of the lower layer.
    """

    def __init__(self, name, model, solver=EigenvalueMethod):
        self.name = name
        self.solver = solver()
        self.preference_matrices = model['preferenceMatrices']
        self.leaf = False

        sub_criteria = model['subCriteria'].get(name)

        if sub_criteria is not None:
            self.sub_criteria = [AHPCriterion(n, model, solver) for n in sub_criteria]
            self.p_m_key = 'subCriteria:{}'.format(name)
        else:
            self.leaf = True
            self.p_m_key = 'alternatives:{}'.format(name)

    def __str__(self):
        return self.name

    def get_priorities(self):
        """Get the priority of the nodes in the level below this node.

        Returns:
            Priorities at current level, normalized if an internal node.
        """
        self.p_m = np.array(self.preference_matrices[self.p_m_key])
        self.sub_crit_pr = self.solver.estimate(self.p_m)

        if self.leaf:
            return self.sub_crit_pr

        criteria_pr = [criterion.get_priorities() for criterion in self.sub_criteria]

        return normalize_priorities(criteria_pr, self.sub_crit_pr)

    def persist(self, persistance, level ):
        persistance.save("------------ {} ---------------".format(self.p_m_key) ,key="LEVEL{}".format(level), level=level)
        persistance.save( np.array_str(self.p_m), key="{}:sub preference matric".format(self.p_m_key), level=level)
        persistance.save( self.sub_crit_pr, key="{}:sub priority".format(self.p_m_key), level=level )
        self.solver.persist(persistance, level+1)
        if not self.leaf:
            for criterion in self.sub_criteria:
                persistance.newline();
                criterion.persist(persistance, level+1)
        
