import altair
import normalizer as norm


class Plotter:
    chart = None
    line_chart = None
    circle_chart = None
    means_line_chart = None
    means_circle_chart = None
    quartiles_chart = None

    def __init__(self, *args):
        # Then not the basic chart
        if len(args) == 6:
            self.create_line_and_circle_chart(args[0])
            self.chart = self.line_chart + self.circle_chart
            if args[1] or args[5]:
                # If the means or the quartiles must be shown
                self.class_means_df = norm.get_class_mean_by_test(args[2])

                if len(args[3]) > 0:
                    # In this case the df must be filtered by periods
                    self.class_means_df = norm.get_results_by_period(self.class_means_df, args[3])

                if len(args[4]) > 0:
                    # In this case the df must be filtered by competences
                    self.class_means_df = norm.get_student_results_by_competence(self.class_means_df, args[4])

                if args[5]:
                    # If the quartiles must be shown
                    self.create_quartiles_chart()
                    self.chart += self.quartiles_chart

                if args[1]:
                    # If the means must be shown
                    self.create_means_line_chart()
                    self.chart += self.means_line_chart



        # The basic chart
        elif len(args) == 2:
            self.class_means_df = norm.get_class_mean_by_test(args[0])
            self.create_means_line_chart()
            self.create_means_circle_chart()
            self.create_quartiles_chart()
            self.chart = self.quartiles_chart + self.means_line_chart + self.means_circle_chart

        else:
            raise ValueError("Invalid number of arguments")

    def create_means_line_chart(self):
        self.means_line_chart = altair.Chart(self.class_means_df).mark_line(strokeDash=[4.1]).encode(
            altair.X('Test:O', sort=self.class_means_df['Test'].tolist()).title(
                'Nom du test'),
            altair.Y('Mean:Q', axis=altair.Axis(tickCount=20)).title('Résultat obtenu'),
            color=altair.value('white')
        ).properties(width=600, height=500)

    def create_quartiles_chart(self):
        self.quartiles_chart = altair.Chart(self.class_means_df).mark_area(opacity=0.15).encode(
            altair.X('Test:O', sort=self.class_means_df['Test'].tolist()).title(
                'Nom du test'),
            altair.Y('Q1:Q', axis=altair.Axis(tickCount=20)),
            altair.Y2('Q3:Q'),
            color=altair.value('green')
        ).properties(width=600, height=500)

    def create_means_circle_chart(self):
        self.means_circle_chart = altair.Chart(self.class_means_df).mark_circle().encode(
            altair.X('Test:O', sort=self.class_means_df['Test'].tolist()).title(
                'Nom du test'),
            altair.Y('Mean:Q', axis=altair.Axis(tickCount=20)).title('Résultat obtenu'),
            tooltip=['Test', 'Mean'],
            color=altair.value('green')
        ).properties(width=600, height=500)

    def create_line_and_circle_chart(self, df, title=""):
        self.line_chart = altair.Chart(df, title=title).mark_line().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title('Nom du test'),
            altair.Y('Normalized:Q', axis=altair.Axis(tickCount=20)).title('Résultat obtenu'),
            color='Name:N'
        ).properties(width=600, height=500)

        self.circle_chart = altair.Chart(df, title=title).mark_circle().encode(
            altair.X('Test:O', sort=df['Test'].tolist()).title('Nom du test'),
            altair.Y('Normalized:Q', axis=altair.Axis(tickCount=20)).title('Résultat obtenu'),
            tooltip=['Test', 'Normalized', 'Period'],
            color='Name:N'
        ).properties(width=600, height=500)

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

    def to_specs(self):
        return self.chart.to_dict()
