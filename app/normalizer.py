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
        totals = dataframes[key].iloc[1, 2:].values
        period_means = []
        if key != "Nom":
            for col in range(2, len(dataframes[key].columns) - 2):
                # It is the number of student that were absent
                nbr_of_nan = (dataframes[key].iloc[3:, col] == "").sum()
                # We replace it by 0 so we can sum
                dataframes[key].iloc[3:, col].replace("", 0, inplace=True)
                test_sum = dataframes[key].iloc[3:, col].sum()

                # The mean is computed like this : we divide the test sum by the number of student that did the test
                # i.e. the number of row - the 3 rows that are not related to grades - the number of student hat were
                # absent. Then the sum is divided by the test total and multiplied by 20 to get the mean.
                # Col index starts at 2 for the dataframes but has to start at 0 for the lists it is why there are - 2
                # Finally the mean is round to decimal
                test_mean = round(((test_sum/(len(dataframes[key]) - 3 - nbr_of_nan))/totals[col-2])*20, 1)

                period_means.append((competences[col - 2], test_mean))
            class_mean[key] = period_means

    return class_mean




def get_class_mean_by_competence(dataframes, competences):
    # TODO
    pass
