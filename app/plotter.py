import altair
import normalizer as norm


class Plotter:
    chart = None
    line_circle_chart = None
    means_chart = None
    quartiles_chart = None
    normalized_chart = None
    test_points_normalized_chart = None
    competence_normalized_chart = None

    def __init__(self, *args):
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
                    self.class_means_df = norm.get_class_mean_by_test(args[2])
                    self.class_means_df = norm.get_student_results_by_competence(self.class_means_df, [args[1]])
                    self.create_means_chart()
                    self.create_quartiles_chart()
                    self.create_line_and_circle_chart(args[0])
                    self.create_normalized_chart_for_student(args[0])

                    self.chart = altair.layer(self.means_chart, self.quartiles_chart,
                                              self.line_circle_chart, self.normalized_chart).resolve_scale(
                        color='independent')
                # Chart representing the normalisation of a student regarding the class results
                else:
                    self.class_means_df = args[0]
                    self.create_means_chart()
                    self.create_quartiles_chart()

                    self.create_points_chart_for_tests(args[0], args[1], args[2])

                    self.chart = altair.layer(self.means_chart, self.quartiles_chart,
                                              self.test_points_normalized_chart).resolve_scale(color='independent')

            # Chart representing the normalisation of a student regarding his previous results
            case 4:
                self.create_line_and_circle_chart(args[0])
                self.create_normalized_chart_for_student(args[0])
                self.chart = altair.layer(self.line_circle_chart, self.normalized_chart).resolve_scale(
                    color='independent')
                self.class_means_df = norm.get_class_mean_by_test(args[1])

                if len(args[2]) > 0:
                    self.class_means_df = norm.get_results_by_period(self.class_means_df, args[2])

                if len(args[3]) > 0:
                    self.class_means_df = norm.get_student_results_by_competence(self.class_means_df, args[3])

                self.create_quartiles_chart()
                self.create_means_chart()

                self.chart = altair.layer(self.means_chart, self.quartiles_chart, self.chart).resolve_scale(
                    color='independent')

            # Chart for the basic visualisation, multiple students, filters on the competences and periods etc.
            case 6:
                self.create_line_and_circle_chart(args[0])
                self.chart = altair.layer(self.line_circle_chart).resolve_scale(color='independent')
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
                        self.chart = altair.layer(self.quartiles_chart, self.chart).resolve_scale(color='independent')

            case _:
                raise ValueError("Invalid number of arguments")

    def create_means_chart(self):
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
        self.class_means_df['LabelQuartiles'] = 'Quartiles'
        self.quartiles_chart = altair.Chart(self.class_means_df).mark_area(opacity=0.15).encode(
            altair.X('Test:O', sort=self.class_means_df['Test'].tolist()).title(" "),
            altair.Y('Q1:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            altair.Y2('Q3:Q'),
            color=altair.Color('LabelQuartiles:N').legend(title='').scale(altair.Scale(range=['green']))
        ).properties(width=600, height=500)

    def create_line_and_circle_chart(self, df, title=""):
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
        student_chart = altair.Chart(student_df).mark_circle().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title(" "),
            altair.Y('Normalized Scaled:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            tooltip=['Name', 'Test', 'Result', 'Total', 'On10', 'Normalized Scaled'],
            color=altair.value('red')
        ).properties(width=600, height=500)
        other_students_chart = altair.Chart(other_students_df).mark_circle(opacity=0.20).encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title(" "),
            altair.Y('Normalized Scaled:Q', axis=altair.Axis(tickCount=10)).scale(domain=(0, 10)).title(" "),
            color=altair.value('white')
        ).properties(width=600, height=500)
        self.test_points_normalized_chart = altair.layer(other_students_chart, student_chart).interactive()

    def show_means(self, df):
        self.class_means_df = norm.get_class_mean_by_test(df)
        self.create_means_chart()

        if self.chart is None:
            self.chart = self.means_chart

        else:
            self.chart += self.means_chart

    def hide_means(self):
        self.means_chart = None

        self.chart = self.line_circle_chart

        if self.quartiles_chart is not None:
            self.chart += self.quartiles_chart

    def to_specs(self):
        return self.chart.to_dict()
