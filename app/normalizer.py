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

    final_student_df = student_results[['Name', 'Period', 'Test', 'Competence', 'On10', 'Result', 'Total']]

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


def normalize_regarding_class(df_students, df_means):
    """
    This method is used to normalize the results of a student in regard with the previous results of the class.
    It uses for now a basic normalization using interquartile range, standard deviation and mean. To scale the normalized
    results on a 10 base, the min and max of the normalized results are used.
    :param df_students: The dataframe containing the students results
    :param df_means: The dataframe containing the class means, quartiles, mean and standard deviation for each test
    :return: A dataframe containing the normalized results
    """

    # Merge the two dataframes for future operations
    df_merged = pd.merge(df_students, df_means, on=['Test', 'Competence', 'Period'])

    # Standardize the results
    df_merged['Standardized'] = (df_merged['On10'] - df_merged['Mean']) / df_merged['STD']

    min_score = df_merged['Standardized'].min()
    max_score = df_merged['Standardized'].max()

    # Normalize the results and scale them
    df_merged.loc[:, 'Normalized'] = (df_merged['Standardized'] - min_score) / (max_score - min_score)
    df_merged.loc[:, 'Normalized Scaled'] = df_merged['Normalized'] * 10

    return df_merged


def normalize_regarding_past_results(dataframe, students, outliers):
    """
    This method is used to normalize the results of a student in regard of his previous results.
    :param dataframe: The dataframe with all students results
    :param students: A list containing the student name that has to be normalized
    :return: A dataframe with the normalized results
    """
    if not isinstance(students, list):
        raise TypeError("The students parameter must be a list")
    if len(students) == 0 or len(students) > 1:
        raise ValueError("The students parameter must contain exactly one student")

    student_df = get_all_student_results(dataframe, students).copy()
    student_df['Normalized'] = np.nan
    student_df['Normalized Scaled'] = np.nan

    if outliers:
        # Compute the quartiles and the interquartile range
        q1 = student_df['On10'].quantile(0.25)
        q3 = student_df['On10'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        # Remove the outliers from the dataframe
        student_filtered = student_df[(student_df['On10'] >= lower_bound) & (student_df['On10'] <= upper_bound)].copy()

    else:
        student_filtered = student_df.copy()

    # Compute std and mean on filtered data
    std = student_filtered['On10'].std()
    mean = student_filtered['On10'].mean()

    # Apply the normalization formula on non-filtered data
    student_df.loc[:, 'Normalized'] = (student_df['On10'] - mean) / std

    min_score = student_df['Normalized'].min()
    max_score = student_df['Normalized'].max()

    student_df.loc[:, 'Normalized Scaled'] = ((student_df['Normalized'] - min_score) / (max_score - min_score)) * 10

    return student_df


def normalize_regarding_competence(dataframe, student, competence, outliers):
    """
    This method is used to normalize the results of a student in a particular compretence in regard of his previous
    results in this particular competence.
    :param dataframe: The dataframe with all students results
    :param student: The student name that has to be normalized
    :param competence: The competence that has to be normalized
    :return: A dataframe containing the normalized results
    """
    student_df = get_all_student_results(dataframe, [student]).copy()
    competence_df = get_student_results_by_competence(student_df, [competence]).copy()

    competence_df['Normalized'] = np.nan
    competence_df['Normalized Scaled'] = np.nan

    if outliers:
        q1 = competence_df['On10'].quantile(0.25)
        q3 = competence_df['On10'].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        competence_filtered = competence_df[(competence_df['On10'] >= lower_bound) & (competence_df['On10'] <= upper_bound)].copy()

    else:
        competence_filtered = competence_df.copy()

    std = competence_filtered['On10'].std()
    mean = competence_filtered['On10'].mean()

    competence_df.loc[:, 'Normalized'] = (competence_df['On10'] - mean) / std

    min_score = competence_df['Normalized'].min()
    max_score = competence_df['Normalized'].max()

    competence_df.loc[:, 'Normalized Scaled'] = ((competence_df['Normalized'] - min_score) / (max_score - min_score)) * 10

    return competence_df
