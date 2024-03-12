import altair as alt
import normalizer as norm


class Plotter2:
    chart = None
    line_chart = None
    circle_chart = None
    means_line_chart = None

    def __init__(self, class_df):
        self.class_means_df = norm.get_class_mean_by_test(class_df)

    def create_means_line_chart(self):
        self.means_line_chart = alt.Chart(self.class_means_df, title="Moyenne de la classe").mark_line(
            strokeDash=[4.1]).encode(
            alt.X('Test:O', sort=self.class_means_df['Test'].tolist()).title('Nom du test'),
            alt.Y('Mean:Q').title('Résultat obtenu'),
            tooltip=['Test', 'Mean'],
            color=alt.value('white')
        )

    def create_means_line_chart_by_period(self, period_df):
        self.means_line_chart = alt.Chart(period_df, title="Moyenne de la classe").mark_line(
            strokeDash=[4.1]).encode(
            alt.X('Test:O', sort=period_df['Test'].tolist()).title('Nom du test'),
            alt.Y('Mean:Q').title('Résultat obtenu'),
            tooltip=['Test', 'Mean'],
            color=alt.value('white')
        )

    def create_line_and_circle_chart(self, df, title=""):
        self.line_chart = alt.Chart(df, title=title).mark_line().encode(
            alt.X('Test:O', sort=df['Test'].tolist()).title('Nom du test'),
            alt.Y('Normalized:Q').title('Résultat obtenu'),
            color='Name:N'
        )

        self.circle_chart = alt.Chart(df).mark_circle().encode(
            alt.X('Test:O', sort=df['Test'].tolist()).title('Nom du test'),
            alt.Y('Normalized:Q').title('Résultat obtenu'),
            tooltip=['Test', 'Normalized', 'Period'],
            color='Name:N'
        )

    def reset_chart_to_means(self):
        if self.means_line_chart is None:
            self.create_means_line_chart()
            self.chart = self.means_line_chart
        else:
            self.chart = self.means_line_chart

    def add_infos(self):
        if self.line_chart is not None and self.circle_chart is not None:
            self.chart += self.line_chart + self.circle_chart
        else:
            self.chart = self.means_line_chart
        self.chart.interactive()

    def reset_chart_to_empty(self):
        self.chart = None

    def hide_means(self):
        if self.line_chart is not None and self.circle_chart is not None:
            self.means_line_chart = None
            self.chart = self.line_chart + self.circle_chart
            self.chart.interactive()
        else:
            pass

    def show_means(self):
        if self.means_line_chart is None:
            self.create_means_line_chart()

        if self.line_chart is None and self.circle_chart is None:
            self.chart = self.means_line_chart

        else:
            self.chart += self.means_line_chart

        self.chart.interactive()

    def tospecs(self):
        return self.chart.to_dict()
