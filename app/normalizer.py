import pandas as pd


def get_all_student_results(dataframes, student):
    """
    This method is used to get a dictionary containing all the results of particular student.
    The keys of the dict are the periods i.e. the different sheets in the Excel
    The value is a list of tuples. Each tuple contains the competence and the result of the test on 20
    :param dataframes: A dictionary containing all the sheets of the Excel file where keys are the periods
    :param student: A string containing the name of the student
    :return: A dictionary containing the student's result
    """
    results = {}
    # for loop on the different periods
    for key in dataframes:
        if key != "Nom":
            period_df = dataframes[key]
            # List containing the test's totals
            totals = period_df.iloc[1, 2:].values
            # List containing the competences
            competences = period_df.iloc[2, 2:].values
            # The student's result line matching the name
            student_line = period_df[period_df.iloc[:, 1] == student]
            # List containing the results
            raw_results = student_line.iloc[0, 2:].values

            period_result = []

            for i in range(len(raw_results)):
                if raw_results[i] == "":
                    period_result.append((competences[i], "NP"))
                else:
                    result = round((raw_results[i] / totals[i]) * 20, 1)
                    period_result.append((competences[i], result))

            results[key] = period_result

    return results


def get_student_results_by_period(results, periods):
    """
    This method is used to get the results of a student over one or more periods.
    This method is intended to be used after a first call on the previous method get_all_student_results()
    :param results: A dictionary containing the results of a particular student that we got from get_all_student_results()
    :param periods: A list containing one or more periods we want the results from
    :return: A dictionary containing the results of the student over one or more periods
    """
    filtered_results = {}
    for key in periods:
        # The key of results dictionary is the name of the period
        if key in results:
            filtered_results[key] = results[key]

    return filtered_results


def get_student_results_by_competence(results, competences):
    """
    This method is used to get the results of a student over one or more competences.
    :param results: A dictionary containing the results of a particular student that we got from get_all_student_results()
    :param competences: A list containing one or more competences we want the results from
    :return: A dictionary containing the results of the student over one or more competences
    """
    filtered_results = {}
    for key in results:
        period_result = []
        for test in results[key]:
            # The first element of test tuple is the competence
            if test[0] in competences:
                period_result.append(test)
        filtered_results[key] = period_result
    return filtered_results


def get_global_class_mean(dataframes):
    class_mean = {}
    for key in dataframes:
        competences = dataframes[key].iloc[2, 2:].values
        dataframes[key].fillna(0)
        period_means = []
        if key != "Nom":
            for col in range(2, len(dataframes[key].columns)):
                test_sum = dataframes[key].iloc[3:, col].sum()
                period_means.append((competences[col], test_sum/dataframes[key].rows - 4))
        class_mean[key] = period_means

    return class_mean




def get_class_mean_by_competence(dataframes, competences):
    # TODO
    pass
