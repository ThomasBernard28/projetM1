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


def normalize_regarding_class(df_students, df_means, student):
    df_student = df_students[df_students['Name'] == student]
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


"""
def normalize_by_student_results(dataframe, student):
    if isinstance(student, list):
        raise TypeError("The student parameter must be a string")
    students = [student]
    student_results = get_all_student_results(dataframe, students)
    student_results['Normalized Result'] = np.nan
    student_results['Normalized Scaled'] = np.nan

    z_scores = []
    normalized_scores = []

    for i in range(len(student_results)):
        current_values = student_results['On10'][:i]
        current_mean = current_values.mean()
        current_std = current_values.std() if current_values.std() != 0 else 1

        if i == 0:
            current_z_score = 0
            current_normalized_score = 0.5  # In this case the score matches the mean

        else:
            current_z_score = (student_results.iloc[i]['On10'] - current_mean) / current_std
            all_z_scores = np.array(z_scores + [current_z_score])
            min_z = all_z_scores.min()
            max_z = all_z_scores.max()
            current_normalized_score = (current_z_score - min_z) / (max_z - min_z) if max != min_z else 0.5

        z_scores.append(current_z_score)
        normalized_scores.append(current_normalized_score)

        student_results.at[student_results.index[i], 'Normalized Result'] = current_z_score
        student_results.at[student_results.index[i], 'Normalized Scaled'] = current_normalized_score

    return student_results
"""
