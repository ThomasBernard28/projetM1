import pandas as pd


def get_all_student_results(dataframes, student):
    results = []
    for key in dataframes:
        if key != "Nom":
            period_df = dataframes[key]
            totals = period_df.iloc[1, 2:].values
            student_line = period_df[period_df.iloc[:, 1] == student]
            raw_results = student_line.iloc[0, 2:].values

            for i in range(len(raw_results)):
                if raw_results[i] == "":
                    results.append("NP")
                else:
                    result = round((raw_results[i] / totals[i]) * 20, 1)
                    results.append(result)

    return results

def get_student_results_by_period(dataframes, student, periods):
    # TODO
    pass


def get_student_results_by_competence(dataframes, student, competences):
    # TODO
    pass


def get_global_class_mean(dataframes):
    # TODO
    pass


def get_class_mean_by_competence(dataframes, competences):
    # TODO
    pass
