# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 17:14:00 2020

@author: Donal
"""

from . import init
from .Utils import requirements_to_vector, read_hard_rules, search_and_filter, multi_level_search


def HardMatching(user_input):
    software_score_table, software_name, feature_name, filename = read_hard_rules()
    requirements = requirements_to_vector(user_input, feature_name)

    # Check if user data has the same format as software data
    if software_score_table.shape[1] == requirements.shape[0]:
        result, closed_list, compared_features = search_and_filter(requirements, software_score_table)
        results = [software_name[i] for i in range(len(result)) if result[i] is True]
        if len(results) <= init.number_of_match:
            # continue search if no results
            required_matches = init.number_of_match - len(results)
            result = multi_level_search(closed_list, requirements, software_name, compared_features, required_matches)
            results += result
            return results

        else:
            return results


    else:
        print(f"Shape of user requirements is different from software requirements"
              f"{requirements.shape[0]} vs {str(software_score_table.shape[1])}")
        results = None
