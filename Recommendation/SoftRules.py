# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 10:42:57 2020

@author: Donal
"""
from .Utils import requirements_to_vector, flatten, read_soft_rules, score_and_evaluate


def SoftMatching(eligible_software, user_requirements):
    software_score_table, software_name, feature_name, filename = read_soft_rules()
    requirements_vector = requirements_to_vector(user_requirements, feature_name)
    flatten_software = flatten(eligible_software)
    score_table = {i: (software_score_table[software_name.index(i)]) for i in set(flatten_software)}
    results = score_and_evaluate(eligible_software, requirements_vector, score_table)

    return results
