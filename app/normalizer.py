import pandas as pd
import numpy as np


def normalize_results(dataframe):
    """
    This method is used to normalize the results on a 20 base
    :param dataframe: the dataframe to normalize
    :return: a dataframe with the normalized results
    """
    dataframe['Normalized'] = round((dataframe['Result'] / dataframe['Total']) * 10, 2)

    return dataframe


def get_all_student_results(dataframe, students):
    """
    This method is used to get all the results of a particular student.
    :param dataframe: The dataframe resulting from normalization
    :param students: The student name
    :return: A dataframe containing the student results
    """
    # Get all records for 1 student
    student_results = dataframe[dataframe['Name'].isin(students)]

    final_student_df = student_results[['Name', 'Period', 'Test', 'Competence', 'Normalized']]

    return final_student_df


def get_results_by_period(dataframe, periods):
    """
    This method is used to get all the results for one or more periods
    :param dataframe: The dataframe resulting from normalization
    :param periods: A list of periods
    :return: A dataframe containing the results for periods
    """
    results_by_period = dataframe[dataframe['Period'].isin(periods)]

    return results_by_period


def get_student_results_by_competence(dataframe, competences):
    """
    This method is used to get all the results for one or more competences
    :param dataframe: The dataframe we want the results from
    :param competences: A list of competences
    :return: A dataframe containing the results for competences
    """
    results_by_competence = dataframe[dataframe['Competence'].isin(competences)]

    return results_by_competence


def get_class_mean_by_test(dataframe):
    """
    This method is used to get the mean of the class for each test
    :param dataframe: The dataframe
    :return: A dataframe containing the test name and the mean
    """

    class_means = pd.DataFrame(columns=['Test', 'Period', 'Competence', 'Mean','STD', "Q1", "Q3"])

    for test in dataframe.groupby(['Test', 'Period', 'Competence']).groups.keys():
        test_name, period, competence = test

        test_df = dataframe[(dataframe['Test'] == test_name) & (dataframe['Period'] == period) & (
                dataframe['Competence'] == competence)]

        mean_normalized = test_df['Normalized'].mean()
        std_normalized = test_df['Normalized'].std()

        quantiles = test_df['Normalized'].quantile([0.25, 0.75])

        class_means.loc[len(class_means)] = [test_name, period, competence, mean_normalized, std_normalized, quantiles[0.25],
                                             quantiles[0.75]]

    class_means = class_means.set_index(['Test', 'Competence', 'Period']).reindex(
        dataframe.set_index(['Test', 'Competence', 'Period']).index).reset_index()
    class_means = class_means.drop_duplicates(subset=['Test', 'Competence', 'Period'])

    return class_means


def normalize_by_student_results(dataframe, student):
    if isinstance(student, list):
        raise TypeError("The student parameter must be a string")
    students = [student]
    student_results = get_all_student_results(dataframe, students)
    student_results['Normalized Result'] = np.nan
    student_results['Normalized Scaled'] = np.nan

    for index, row in student_results.iterrows():
        test_index = student_results.index.get_loc(index)
        previous_test_results = student_results.iloc[:test_index]['Normalized']

        mean = previous_test_results.mean(skipna=True)
        standard_deviation = previous_test_results.std(skipna=True)

        if np.isnan(standard_deviation) or standard_deviation == 0:
            normalized_result = 0.5
        else:
            normalized_result = (row['Normalized'] - mean) / standard_deviation

        student_results.at[index, 'Normalized Result'] = normalized_result

    for index, row in student_results.iterrows():
        test_index = student_results.index.get_loc(index)
        previous_normalized_results = student_results.iloc[:test_index]['Normalized Result']

        if previous_normalized_results.empty:
            normalized_scaled = 0.5

        else:
            min_normalized = previous_normalized_results.min()
            max_normalized = previous_normalized_results.max()
            if max_normalized == min_normalized:
                normalized_scaled = 0.5
            else:
                normalized_scaled = (row['Normalized Result'] - min_normalized) / (max_normalized - min_normalized)

            if not np.isnan(normalized_scaled):
                normalized_scaled = max(0, min(1, normalized_scaled))
        student_results.at[index, 'Normalized Scaled'] = normalized_scaled

    return student_results
