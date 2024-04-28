import pandas as pd
import numpy as np


def normalize_results(dataframe):
    """
    This method is used to normalize the results on a 10 base
    :param dataframe: the dataframe to normalize
    :return: a dataframe with the normalized results
    """
    dataframe['On10'] = round((dataframe['Result'] / dataframe['Total']) * 10, 2)

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

    final_student_df = student_results[['Name', 'Period', 'Test', 'Competence', 'On10']]

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

    class_means = pd.DataFrame(columns=['Test', 'Period', 'Competence', 'Mean', 'STD', "Q1", "Q3"])

    for test in dataframe.groupby(['Test', 'Period', 'Competence']).groups.keys():
        test_name, period, competence = test

        test_df = dataframe[(dataframe['Test'] == test_name) & (dataframe['Period'] == period) & (
                dataframe['Competence'] == competence)]

        mean_normalized = test_df['On10'].mean()
        std_normalized = test_df['On10'].std()

        quantiles = test_df['On10'].quantile([0.25, 0.75])

        class_means.loc[len(class_means)] = [test_name, period, competence, mean_normalized, std_normalized,
                                             quantiles[0.25],
                                             quantiles[0.75]]

    class_means = class_means.set_index(['Test', 'Competence', 'Period']).reindex(
        dataframe.set_index(['Test', 'Competence', 'Period']).index).reset_index()
    class_means = class_means.drop_duplicates(subset=['Test', 'Competence', 'Period'])

    return class_means


def normalize_regarding_class(df_students, df_means, students):
    if not isinstance(students, list):
        raise TypeError("The students parameter must be a list")
    if len(students) == 0 or len(students) > 1:
        raise ValueError("The students parameter must contain exactly one student")

    df_student = get_all_student_results(df_students, students)
    df_merged = pd.merge(df_student, df_means, on=['Test', 'Competence', 'Period'])

    df_merged['Standardized'] = (df_merged['On10'] - df_merged['Mean']) / df_merged['STD']

    IQR = df_merged['Q3'] - df_merged['Q1']
    lower_bound = df_merged['Q1'] - 1.5 * IQR
    upper_bound = df_merged['Q3'] + 1.5 * IQR

    df_filtered = df_merged[(df_merged['On10'] >= lower_bound) & (df_merged['On10'] <= upper_bound)]

    min_score = df_filtered['Standardized'].min()
    max_score = df_filtered['Standardized'].max()
    df_filtered.loc[:, 'Normalized'] = (df_filtered['Standardized'] - min_score) / (max_score - min_score)

    return df_filtered


def normalize_regarding_past_results(dataframe, students):
    if not isinstance(students, list):
        raise TypeError("The students parameter must be a list")
    if len(students) == 0 or len(students) > 1:
        raise ValueError("The students parameter must contain exactly one student")

    student_df = get_all_student_results(dataframe, students)
    student_df['Normalized'] = np.nan
    student_df['Normalized Scaled'] = np.nan

    std = student_df['On10'].std()
    mean = student_df['On10'].mean()

    student_df['Normalized'] = (student_df['On10'] - mean) / std

    min_score = student_df['Normalized'].min()
    max_score = student_df['Normalized'].max()

    student_df['Normalized Scaled'] = ((student_df['Normalized'] - min_score) / (max_score - min_score)) * 10

    return student_df
