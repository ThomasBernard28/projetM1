import altair as alt
import normalizer as norm


class Plotter:
    chart_specs = None
    chart = None
    means_dataframe = None
    means_line_chart = None

    def __init__(self, dataframe):
        self.means_dataframe = norm.get_class_mean_by_test(dataframe)

        self.means_line_chart = alt.Chart(self.means_dataframe).mark_line(strokeDash=[4.1]).encode(
            alt.X('Test:O', sort=dataframe['Test'].tolist()).title('Nom du test'),
            alt.Y('Mean:Q').title('Résultat obtenu'),
            tooltip=['Test', 'Mean'],
            color=alt.value('white')
        ).interactive()

        self.means_line_chart.properties(title="Chart of the class mean")

        self.chart = self.means_line_chart

    def add_students(self, student_df):
        student_chart = alt.Chart(student_df).mark_line().encode(
            alt.X('Test:O', sort=student_df['Test'].tolist()).title('Nom du test'),
            alt.Y('Normalized:Q').title('Résultat obtenu'),
            color='Name:N'
        ).interactive()
        self.chart.properties(title="Chart of students results compared to class mean")
        self.chart = self.means_line_chart
        self.chart += student_chart

        student_ball_chart = alt.Chart(student_df).mark_circle().encode(
            alt.X('Test:O', sort=student_df['Test'].tolist()).title('Nom du test'),
            alt.Y('Normalized:Q').title('Résultat obtenu'),
            tooltip=['Test', 'Normalized', 'Period'],
            color='Name:N'
        ).interactive()
        self.chart += student_ball_chart

    def by_period(self, period_df):
        self.chart = None
        student_chart = alt.Chart(period_df).mark_line().encode(
            alt.X('Test:O', sort=period_df['Test'].tolist()).title('Nom du test'),
            alt.Y('Normalized:Q').title('Résultat obtenu'),
            color='Name:N'
        ).interactive()
        self.chart = student_chart
        self.chart.properties(title="Chart of students results compared to class mean")

        student_ball_chart = alt.Chart(period_df).mark_circle().encode(
            alt.X('Test:O', sort=period_df['Test'].tolist()).title('Nom du test'),
            alt.Y('Normalized:Q').title('Résultat obtenu'),
            tooltip=['Test', 'Normalized', 'Period'],
            color='Name:N'
        ).interactive()
        self.chart += student_ball_chart


    def tospecs(self):
        self.chart_specs = self.chart.to_dict()
        return self.chart_specs

    def reset(self):
        self.chart = self.means_line_chart

