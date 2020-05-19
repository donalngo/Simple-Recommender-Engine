import glob
import itertools
from . import init
import numpy as np
from numpy import genfromtxt as read_text_file


def read_rules_files(list_of_files):
    print("Reading : ")
    print(list_of_files[0])
    software_score_table = np.array(read_text_file(list_of_files[0], encoding='utf-8', delimiter=',')[1:, 1:])
    software_matrix = np.array(read_text_file(list_of_files[0], encoding='utf-8', delimiter=',', dtype='str'))
    feature_name = software_matrix[0, 1:]
    software_name = software_matrix[1:, 0]
    filename = [[list_of_files[0][
                 [pos for pos, char in enumerate(list_of_files[0]) if char == "_"][-1] + 1:].replace(".csv", ""),
                 feature_name.shape[0]]]

    for current_file in list_of_files[1:]:
        print(current_file)
        j = read_text_file(current_file, delimiter=',')
        k = read_text_file(current_file, delimiter=',', dtype='str')[0, 1:]
        feature_name = np.concatenate((feature_name, k), axis=0)
        filename.append(
            [current_file[[pos for pos, char in enumerate(current_file) if char == "_"]
                          [-1] + 1:].replace(".csv", ""), feature_name.shape[0]])
        software_score_table = np.concatenate((software_score_table, np.array(j[1:, 1:])), axis=1)
    return software_score_table, software_name, feature_name, filename


def read_soft_rules():
    filename_list = glob.glob(init.path+"/Recommendation/Soft Rules/*.csv")
    software_score_table, software_name, feature_name, filename = read_rules_files(filename_list)
    feature_name = [i.title() for i in feature_name]
    # Filter off the unnecessary software
    software_index = [list(software_name).index(i) for i in list(set(flatten(software_name)))]
    software_score_table = [list(software_score_table)[i] for i in software_index]
    software_name = [list(software_name)[i] for i in software_index]
    return software_score_table, software_name, feature_name, filename


def read_hard_rules():
    filename_list = glob.glob(init.path+"/Recommendation/Hard Rules/*.csv")
    software_score_table, software_name, feature_name, filename = read_rules_files(filename_list)
    return software_score_table, software_name, feature_name, filename


def requirements_to_vector(request, header_names):
    from datetime import datetime
    user_requirements = np.zeros(len(list(header_names))).astype(int)
    dropped_requirements = [i for i in request if not i.title() in header_names]
    request = [i for i in request if i.title() in header_names]


    f = open("Recommendation/Logs/Dropped Requirements.log", "a+")
    currenttime = datetime.now()
    date_time = currenttime.strftime("%m/%d/%Y, %H:%M:%S")
    f.write(f"{date_time}   DROPPED: {dropped_requirements}\n")

    for i in request:
        user_requirements[list(header_names).index(i.title())] = 1
    return user_requirements


def flatten(list_variable):
    # Reduces List of List to a single List
    flattened_variable = []
    for i in list_variable:
        if isinstance(i, list):
            flattened_variable.extend(flatten(i))
        else:
            flattened_variable.append(i)
    return flattened_variable


def compare_requirements(software_score_table, user_requirements):
    return [np.where(software_score - user_requirements == -1) for software_score in software_score_table]


def generate_unique_combinations(total_software_list, combination_size):
    # generating all combinations based on combination size
    all_combinations = list(itertools.product(*[total_software_list], repeat=combination_size))
    # grouping unique sets within combination
    unique_combination_set = [list(set(sorted(combination))) for combination in all_combinations]
    # filtering combinations with length less than defined combination size
    unique_combination_trio = [combination for combination in unique_combination_set
                               if len(combination) == combination_size]
    # filtering down to unique combinations
    unique_combinations = [list(x) for x in set(tuple(x) for x in unique_combination_trio)]
    return unique_combinations


def duo_requirements_matching(lacking_features_list, fulfilled_list, filtered_software_names):
    # find matching duo software index
    duo_match_index = sorted([sorted(list([lacking_index, fulfilled_index])) for lacking_index, lacking_feature
                              in enumerate(lacking_features_list) for fulfilled_index, fulfilled_feature
                              in enumerate(fulfilled_list) if lacking_feature == fulfilled_feature])
    # remove duplicates within duos
    duo_unique_index = list(indices for indices, _ in itertools.groupby(duo_match_index))
    # get names of software by index
    results = [[filtered_software_names[software_index] for software_index in combination] for combination in
               duo_unique_index]
    return results


def trio_requirements_matching(fulfilled_list, unique_combinations, requirements_vector, filtered_software_names):
    # Concatenate all features in a single array for each combination and append to combinations list
    match_features = [set(flatten([fulfilled_list[index] for index in combination]))
                      for combination in unique_combinations]
    # Filter features mixture which does not meet length of requirements vector
    match_index = [group_index for group_index in range(len(unique_combinations))
                   if len(match_features[group_index]) == len(requirements_vector)]
    # Filter duplicate combinations
    matches = [sorted(i) for i in [unique_combinations[i] for i in match_index]]
    # get names of software by index
    results = [[filtered_software_names[software_index] for software_index in combination]
               for combination in matches]
    return results


def multi_level_search(closed_list, user_requirements, software_names, lacking_features_list, required_matches):
    filtered_software_names, filtered_lacking_features = map(list, zip(*[[software_names[i], lacking_features_list[i]]
                                                                         for i in range(len(software_names))
                                                                         if closed_list[i] is False]))
    requirements_vector = np.where(user_requirements == 1)[0]
    lacking_features_list = [list(i[0]) for i in filtered_lacking_features if len(i[0]) != 0]
    fulfilled_list = [[j for j in requirements_vector if j not in i] for i in lacking_features_list]
    duo_results = duo_requirements_matching(lacking_features_list, fulfilled_list, filtered_software_names)
    # if results is less than pre-defined number of matches -> do trio search
    if len(duo_results) < required_matches:
        combination_size = 3
        total_software_list = range(len(filtered_software_names))
        unique_combinations = generate_unique_combinations(total_software_list, combination_size)
        trio_results = trio_requirements_matching(fulfilled_list, unique_combinations,
                                                  requirements_vector, filtered_software_names)
    else:
        trio_results = []
    results = duo_results + trio_results

    return results


def search_and_filter(user_requirements, software_score_table):
    """
    Matches all software features with user requirements and returns the Exact Match & Closed List (none match)
    :param user_requirements: numpy array
    :param software_score_table: numpy array
    :return:
        result: list of True and False
        closed_list : list of True and False
    """
    lacking_features = compare_requirements(software_score_table, user_requirements)
    number_of_requirements = len(np.argwhere(user_requirements == 1))
    filtered_list = [[np.size(i) == 0, (len(i[0]) == number_of_requirements or np.size(i) == 0)] #len(np.where(i == 0)[0]) == 1
                     for i in lacking_features]
    result, closed_list = zip(*filtered_list)
    return result, closed_list, lacking_features


def score_and_evaluate(eligible_software, requirements_vector, score_table):
    software_score = []
    k = 0
    print(eligible_software)
    for i in eligible_software:
        print(i)
        k += 1
        if type(i) == list and len(i) > 1:
            # single_recommendation or False
            score = 0
            for j in i:
                score += sum(score_table[j] * requirements_vector) / len(i)
            single_recommendation = False
        else:
            # single_recommendation or True
            score = sum(score_table[i] * requirements_vector)
        software_score.append(score)
    results = [i for i in zip(eligible_software, software_score)]
    results.sort(key=lambda x: x[1], reverse=True)
    if k == 1:
        single_recommendation = True
    else:
        single_recommendation = False
    if single_recommendation and True:
        results.sort(key=lambda x: len(x[0]))
    return results
