import altair
import normalizer as norm


class Plotter:
    chart = None
    line_chart = None
    circle_chart = None
    means_line_chart = None
    means_circle_chart = None
    quartiles_chart = None
    normalized_chart = None
    test_points_normalized_chart = None

    def __init__(self, *args):
        # Then not the basic chart
        if len(args) == 6:
            self.create_line_and_circle_chart(args[0])
            self.chart = altair.layer(self.line_chart + self.circle_chart).resolve_scale(color='independent')
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
                self.create_means_line_chart()
                if args[1]:
                    # If the means must be shown
                    self.chart = altair.layer(self.means_line_chart, self.chart).resolve_scale(color='independent')
                if args[5]:
                    # If the quartiles must be shown
                    self.chart = altair.layer(self.quartiles_chart, self.chart).resolve_scale(color='independent')



        # The normalized chart for a student normalization
        elif len(args) == 4:
            self.create_line_and_circle_chart(args[0])
            self.create_normalized_chart_for_student(args[0])
            self.chart = altair.layer(self.line_chart, self.circle_chart, self.normalized_chart).resolve_scale(color='independent')
            self.class_means_df = norm.get_class_mean_by_test(args[1])

            if len(args[2]) > 0:
                self.class_means_df = norm.get_results_by_period(self.class_means_df, args[2])

            if len(args[3]) > 0:
                self.class_means_df = norm.get_student_results_by_competence(self.class_means_df, args[3])

            self.create_quartiles_chart()
            self.create_means_line_chart()

            self.chart = altair.layer(self.means_line_chart, self.quartiles_chart, self.chart).resolve_scale(color='independent')

        # The chart for normalization regarding class results
        elif len(args) == 3:
            self.class_means_df = args[0]
            self.create_means_line_chart()
            self.create_means_circle_chart()
            self.create_quartiles_chart()

            self.create_points_chart_for_tests(args[0], args[1], args[2])

            self.chart = altair.layer(self.means_line_chart, self.quartiles_chart,self.means_circle_chart, self.test_points_normalized_chart).resolve_scale(color='independent')


        # The basic chart
        elif len(args) == 2:
            self.class_means_df = norm.get_class_mean_by_test(args[0])
            self.create_means_line_chart()
            self.create_means_circle_chart()
            self.create_quartiles_chart()
            self.chart = altair.layer(self.means_line_chart,self.quartiles_chart, self.means_circle_chart).resolve_scale(color='independent')

        else:
            raise ValueError("Invalid number of arguments")

    def create_means_line_chart(self):
        self.class_means_df['Label'] = 'Moyenne de la classe'
        self.means_line_chart = altair.Chart(self.class_means_df).mark_line(strokeDash=[4.1]).encode(
            altair.X('Test:O', sort=self.class_means_df['Test'].tolist()).title(
                'Nom du test'),
            altair.Y('Mean:Q', axis=altair.Axis(tickCount=10)).title('Résultat obtenu'),
            color=altair.Color('Label:N').legend(title='Légende').scale(altair.Scale(range=['white']))
        ).properties(width=600, height=500)

    def create_quartiles_chart(self):
        self.class_means_df['LabelQuartiles'] = 'Quartiles'
        self.quartiles_chart = altair.Chart(self.class_means_df).mark_area(opacity=0.15).encode(
            altair.X('Test:O', sort=self.class_means_df['Test'].tolist()).title(
                'Nom du test'),
            altair.Y('Q1:Q', axis=altair.Axis(tickCount=10)),
            altair.Y2('Q3:Q'),
            color=altair.Color('LabelQuartiles:N').legend(title='').scale(altair.Scale(range=['green']))
        ).properties(width=600, height=500)

    def create_means_circle_chart(self):
        self.means_circle_chart = altair.Chart(self.class_means_df).mark_circle().encode(
            altair.X('Test:O', sort=self.class_means_df['Test'].tolist()).title(
                'Nom du test'),
            altair.Y('Mean:Q', axis=altair.Axis(tickCount=10)).title('Résultat obtenu'),
            tooltip=['Test', 'Mean'],
            color=altair.value('green')
        ).properties(width=600, height=500)

    def create_line_and_circle_chart(self, df, title=""):
        self.line_chart = altair.Chart(df, title=title).mark_line().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title('Nom du test'),
            altair.Y('On10:Q', axis=altair.Axis(tickCount=10)).title('Résultat obtenu'),
            color=altair.Color('Name:N').legend(title='').scale(altair.Scale(scheme='category20')),
        ).properties(width=600, height=500)

        self.circle_chart = altair.Chart(df, title=title).mark_circle().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title('Nom du test'),
            altair.Y('On10:Q', axis=altair.Axis(tickCount=10)).title('Résultat obtenu'),
            tooltip=['Test', 'On10', 'Period'],
            color=altair.Color('Name:N').legend(None).scale(altair.Scale(scheme='category20'))
        ).properties(width=600, height=500)

    def create_normalized_chart_for_student(self, df):
        df['Label'] = 'Normalisé'
        self.normalized_chart = altair.Chart(df).mark_line().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title('Nom du test'),
            altair.Y('Normalized Scaled:Q', axis=altair.Axis(tickCount=10)),
            color=altair.Color('Label:N').legend(title='').scale(altair.Scale(range=['red']))
        ).properties(width=600, height=500)

    def create_normalized_chart_for_student_test(self, df, student):
        self.normalized_chart = altair.Chart(df).mark_point(
            altair.X('Test:O'),
            y='Normalized:Q',
            color=altair.condition(
                altair.datum.Name == student,
                altair.value('red'),
                altair.value('steelblue')
            )
        ).properties(width=600, height=500)

    def create_points_chart_for_tests(self, df, student_df, other_students_df):
        student_chart = altair.Chart(student_df).mark_circle().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title('Nom du test'),
            altair.Y('Normalized Scaled:Q', axis=altair.Axis(tickCount=10)),
            color=altair.value('red')
        ).properties(width=600, height=500)
        other_students_chart = altair.Chart(other_students_df).mark_circle().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title('Nom du test'),
            altair.Y('Normalized Scaled:Q', axis=altair.Axis(tickCount=10)),
            color=altair.value('white')
        ).properties(width=600, height=500)
        self.test_points_normalized_chart = altair.layer(other_students_chart, student_chart).interactive()


    def show_means(self, df):
        self.class_means_df = norm.get_class_mean_by_test(df)
        self.create_means_line_chart()

        if self.chart is None:
            self.chart = self.means_line_chart

        else:
            self.chart += self.means_line_chart

    def hide_means(self):
        self.means_line_chart = None

        self.chart = self.line_chart + self.circle_chart

        if self.quartiles_chart is not None:
            self.chart += self.quartiles_chart

    def to_specs(self):
        return self.chart.to_dict()
