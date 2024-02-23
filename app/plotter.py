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
            x="Test:O",
            y="Mean:Q",
            tooltip=['Test', 'Mean'],
            color=alt.value('white')
        ).interactive()

        self.means_line_chart.properties(title="Chart of the class mean")

        self.chart = self.means_line_chart

    def add_students(self, student_df):
        student_chart = alt.Chart(student_df).mark_line().encode(
            x="Test:O",
            y="Normalized:Q",
            tooltip=['Test', 'Normalized', 'Period'],
            color='Name:N'
        ).interactive()
        self.chart.properties(title="Chart of students results compared to class mean")
        self.chart = self.means_line_chart
        self.chart += student_chart

    def by_period(self, period_df):
        student_chart = alt.Chart(period_df).mark_line().encode(
            x="Test:O",
            y="Normalized:Q",
            tooltip=['Test', 'Normalized', 'Period'],
            color='Name:N'
        ).interactive()
        self.chart.properties(title="Chart of students results compared to class mean")
        self.chart = self.means_line_chart
        self.chart += student_chart

    def tospecs(self):
        self.chart_specs = self.chart.to_dict()
        return self.chart_specs

    def reset(self):
        self.chart = self.means_line_chart

