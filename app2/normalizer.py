import pandas as pd


def normalize_results(dataframe):
    """
    This method is used to normalize the results on a 20 base
    :param dataframe: the dataframe to normalize
    :return: a dataframe with the normalized results
    """
    dataframe['Normalized'] = round((dataframe['Result'] / dataframe['Total']) * 20, 2)

    return dataframe


def get_all_student_results(dataframe, student):
    """
    This method is used to get all the results of a particular student.
    :param dataframe: The dataframe resulting from normalization
    :param student: The student name
    :return: A dataframe containing the student results
    """
    # Get all records for 1 student
    student_results = dataframe[dataframe['Name'] == student]

    final_student_df = student_results[['Name', 'Period', 'Test', 'Competence', 'Normalized']]

    return final_student_df


def get_student_results_by_period(dataframe, periods):
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


def get_class_mean_by_test(dataframe, test_name):
    """
    This method is used to get the mean of a particular test
    :param dataframe: The dataframe
    :param test_name: The name of the test we want the mean from
    :return: A tuple containing the test name and the mean
    """
    test_results = dataframe[dataframe['Test'] == test_name].copy()
    test_results.dropna(subset=['Normalized'], inplace=True)

    mean = test_results['Normalized'].mean()

    return (test_name, mean)
