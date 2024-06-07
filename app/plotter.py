import altair
import normalizer as norm


class Plotter:
    """
    This class is used to create the different charts used in the application
    Each chart is an object of the class Plotter and is created with the __init__ method
    The init method takes a variable number of arguments to create the different charts
    Each length of arguments corresponds to a different chart
    The global variable chart is the chart that will be displayed
    Each other chart is a sub_chart that will be added or not to the global chart
    """
    chart = None
    means_chart = None
    sub_chart = None
    line_circle_chart = None
    quartiles_chart = None
    normalized_chart = None
    test_points_normalized_chart = None
    competence_normalized_chart = None
    class_repartition_chart = None

    def __init__(self, *args):
        """
        This method is used to create the different charts.
        :param args: Variable number of arguments
        """
        match len(args):
            # Basic chart containing the mean and the quartiles
            case 1:
                self.class_means_df = norm.get_class_mean_by_test(args[0])
                self.create_means_chart()
                self.create_quartiles_chart()
                self.chart = altair.layer(self.means_chart, self.quartiles_chart).resolve_scale(color='independent')
            case 3:
                # Chart representing the normalisation of a student regarding a competence
                if isinstance(args[1], str):
                    self.create_line_and_circle_chart(args[0])
                    self.create_normalized_chart_for_student(args[0])
                    self.sub_chart = altair.layer(self.line_circle_chart, self.normalized_chart).resolve_scale(
                        color='independent')
                    self.chart = altair.layer(self.sub_chart).resolve_scale(color='independent')

                # Chart representing the normalisation of a student regarding the class results
                else:
                    self.create_points_chart_for_tests(args[0], args[1], args[2])
                    self.sub_chart = altair.layer(self.test_points_normalized_chart).resolve_scale(color='independent')
                    self.chart = altair.layer(self.sub_chart).resolve_scale(color='independent')

            # Chart representing the normalisation of a student regarding his previous results
            case 4:
                self.create_line_and_circle_chart(args[0])
                self.create_normalized_chart_for_student(args[0])
                self.sub_chart = altair.layer(self.line_circle_chart, self.normalized_chart).resolve_scale(
                    color='independent')
                self.chart = altair.layer(self.sub_chart).resolve_scale(color='independent')

            # Chart for the basic visualisation, multiple students, filters on the competences and periods etc.
            case 6:
                self.create_line_and_circle_chart(args[0])
                self.sub_chart = altair.layer(self.line_circle_chart).resolve_scale(color='independent')
                self.chart = self.sub_chart
                if args[1] or args[5]:
                    # If the means or the quartiles must be shown
                    self.class_means_df = norm.get_class_mean_by_test(args[2])

                    if len(args[3]) > 0:
                        # In this case the df must be filtered by periods
                        self.class_means_df = norm.get_results_by_period(self.class_means_df, args[3])

                    if len(args[4]) > 0:
                        # In this case the df must be filtered by competences
                        self.class_means_df = norm.get_student_results_by_competence(self.class_means_df, args[4])

                    self.create_quartiles_chart()
                    self.create_means_chart()
                    if args[1]:
                        # If the means must be shown
                        self.chart = altair.layer(self.means_chart, self.chart).resolve_scale(color='independent')
                    if args[5]:
                        # If the quartiles must be shown
                        self.chart = altair.layer(self.chart, self.quartiles_chart).resolve_scale(color='independent')

            case _:
                raise ValueError("Invalid number of arguments")

    def create_means_chart(self):
        """
        This method is used to create the chart representing the means of the class
        It is composed of two sub-charts, a line chart and a circle chart
        :return: The layered chart containing the two sub-charts
        """
        self.class_means_df['Label'] = 'Moyenne de la classe'
        means_line_chart = altair.Chart(self.class_means_df).mark_line(strokeDash=[4.1]).encode(
            altair.X('Test:O', sort=self.class_means_df['Test'].tolist()).title(" "),
            altair.Y('Mean:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            color=altair.Color('Label:N').legend(title='Légende').scale(altair.Scale(range=['white']))
        ).properties(width=600, height=500)
        means_circle_chart = altair.Chart(self.class_means_df).mark_circle().encode(
            altair.X('Test:O', sort=self.class_means_df['Test'].tolist()).title(" "),
            altair.Y('Mean:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            tooltip=['Test', 'Mean', 'Period', 'Competence'],
            color=altair.value('green')
        ).properties(width=600, height=500)
        self.means_chart = altair.layer(means_line_chart, means_circle_chart).interactive()

    def create_quartiles_chart(self):
        """
        This method is used to create the chart representing the quartiles of the class.
        It is composed of an area chart
        :return: The area chart representing the quartiles
        """
        self.class_means_df['LabelQuartiles'] = 'Quantiles'
        self.quartiles_chart = altair.Chart(self.class_means_df).mark_area(opacity=0.15).encode(
            altair.X('Test:O', sort=self.class_means_df['Test'].tolist()).title(" "),
            altair.Y('Q1:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            altair.Y2('Q3:Q'),
            color=altair.Color('LabelQuartiles:N').legend(title='').scale(altair.Scale(range=['green']))
        ).properties(width=600, height=500)

    def create_line_and_circle_chart(self, df, title=""):
        """
        This method is used to create the line and circle chart representing the results of a student.
        It is composed of two sub-charts, a line chart and a circle chart
        :param df: The dataframe containing the results of the student
        :param title: The option is set to "" by default
        :return: The layered chart containing the two sub-charts
        """
        line_chart = altair.Chart(df, title=title).mark_line().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title(" "),
            altair.Y('On10:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            color=altair.Color('Name:N').legend(title='').scale(altair.Scale(scheme='category20')),
        ).properties(width=600, height=500)

        circle_chart = altair.Chart(df, title=title).mark_circle().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title(" "),
            altair.Y('On10:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            tooltip=['Name', 'Test', 'Result', 'Total', 'On10', 'Period'],
            color=altair.Color('Name:N').legend(None).scale(altair.Scale(scheme='category20'))
        ).properties(width=600, height=500)
        self.line_circle_chart = altair.layer(line_chart, circle_chart).interactive()

    def create_normalized_chart_for_student(self, df):
        """
        This method is used to create the chart representing the normalisation of the student results.
        It is composed of two sub-charts, a line chart and a circle chart
        :param df: the dataframe containing the results of the student
        :return: the layered chart containing the two sub-charts
        """
        df['Label'] = 'Normalisé'
        line_normalized_chart = altair.Chart(df).mark_line().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title(" "),
            altair.Y('Normalized Scaled:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            color=altair.Color('Label:N').legend(title='').scale(altair.Scale(range=['red']))
        ).properties(width=600, height=500)
        circle_normalized_chart = altair.Chart(df).mark_circle().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title(" "),
            altair.Y('Normalized Scaled:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            tooltip=['Name', 'Test', 'Result', 'Total', 'On10', 'Normalized Scaled'],
            color=altair.Color('Label:N').legend(title='').scale(altair.Scale(range=['red']))
        ).properties(width=600, height=500)
        self.normalized_chart = altair.layer(line_normalized_chart, circle_normalized_chart).interactive()

    def create_points_chart_for_tests(self, df, student_df, other_students_df):
        """
        This method is used to create the chart representing the normalisation of the student results regarding the class
        It is composed of two sub-charts, a circle chart for the student and a circle chart for the other students
        The student chart is in red and the other students chart is in white
        :param df: The global dataframe containing the results of the class
        :param student_df: The dataframe containing the results of the student
        :param other_students_df: The dataframe containing the results of the other students
        :return: the layered chart containing the two sub-charts
        """
        student_chart = altair.Chart(student_df).mark_circle().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title(" "),
            altair.Y('Normalized Scaled:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            tooltip=['Name', 'Test', 'Result', 'Total', 'On10', 'Normalized Scaled'],
            color=altair.value('red')
        ).properties(width=600, height=500)
        other_students_chart = altair.Chart(other_students_df).mark_circle(opacity=0.3).encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title(" "),
            altair.Y('Normalized Scaled:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            color=altair.value('white')
        ).properties(width=600, height=500)
        self.test_points_normalized_chart = altair.layer(other_students_chart, student_chart).interactive()

    def create_repartition_chart(self, df):
        """
        This method is used to create the chart representing the repartition of the class results.
        It is composed of a circle chart
        :param df: The dataframe containing the results of the class
        :return: The chart representing the repartition of the class results
        """
        self.class_repartition_chart = altair.Chart(df).mark_circle().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title(" "),
            altair.Y('On10:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            tooltip=['Name', 'Test', 'Result', 'Total', 'On10', 'Period'],
            color=altair.value('white')
        ).properties(width=600, height=500).interactive()

    def show_means(self, df):
        """
        This method is used to show the means of the class
        It adds the means chart to the global chart. If the global chart is None, the means chart is the global chart
        Otherwise, the means chart is added to the global chart
        :param df: The results of the class
        """
        self.class_means_df = norm.get_class_mean_by_test(df)
        self.create_means_chart()

        if self.chart is None:
            self.chart = altair.layer(self.means_chart).resolve_scale(color='independent')

        else:
            self.chart = altair.layer(self.means_chart, self.chart).resolve_scale(color='independent')

    def hide_means(self):
        """
        This method is used to hide the means of the class. It sets the means chart to None and the global chart to the
        sub chart if it exists.
        """
        self.means_chart = None

        self.chart = self.sub_chart

        if self.quartiles_chart is not None:
            self.chart = altair.layer(self.quartiles_chart, self.chart).resolve_scale(color='independent')

    def show_quartiles(self, df):
        """
        This method is used to show the quartiles of the class
        :param df: The dataframe containing the results of the class
        """
        self.class_means_df = norm.get_class_mean_by_test(df)
        self.create_quartiles_chart()

        if self.chart is None:
            self.chart = altair.layer(self.quartiles_chart).resolve_scale(color='independent')

        else:
            self.chart = altair.layer(self.chart, self.quartiles_chart).resolve_scale(color='independent')

    def hide_quartiles(self):
        """
        This method is used to hide the quartiles of the class. It sets the quartiles chart to None and the global chart
        to the sub chart if it exists.
        """
        self.quartiles_chart = None

        self.chart = self.sub_chart

        if self.means_chart is not None:
            self.chart = altair.layer(self.means_chart, self.chart).resolve_scale(color='independent')

    def show_points(self, df):
        """
        This method is used to show the repartition of the class results
        :param df: The dataframe containing the results of the class
        """
        self.create_repartition_chart(df)
        self.chart = altair.layer(self.means_chart, self.quartiles_chart, self.class_repartition_chart).resolve_scale(
            color='independent')

    def hide_points(self):
        """
        This method is used to hide the repartition of the class results. It sets the class repartition chart to None
        """
        self.class_repartition_chart = None
        self.chart = altair.layer(self.means_chart, self.quartiles_chart).resolve_scale(color='independent')

    def to_specs(self):
        """
        This method is used to convert the chart to a dictionary in order to display it
        :return: The chart as a dictionary
        """
        return self.chart.to_dict()
