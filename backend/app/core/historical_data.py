import datetime
from bokeh.io import output_file
from bokeh.layouts import row
from bokeh.models import NumeralTickFormatter, ColumnDataSource, LinearColorMapper, ColorBar, BasicTicker
from bokeh.models.tools import HoverTool
from bokeh.plotting import figure, save
from bokeh.palettes import viridis
from bokeh.transform import transform
from numpy import log
from math import sqrt

from app.core.external_data_interface import Financial_Data


class Hist_Data(Financial_Data):
    def __init__(self, securities, provider="YF", start="2000-01-01", end=datetime.date.today(), corr_method='pearson'):
        super().__init__(securities, provider, start, end)
        self._data = Financial_Data(securities=securities, provider=provider, start=start, end=end)
        self.securities = securities
        self.returns = self._calculate_returns()
        self.cum_returns = self._calculate_cum_returns()
        self.mean = self._calculate_mean()
        self.std = self._calculate_std()
        # self.skew = self._calculate_skew()
        # self.kurtosis = self._calculate_kurtosis()
        self.corr = self._calculate_corr(method=corr_method)
        self.cov = self._calculate_cov()
        self.var = self._calculate_var()
        # returns + summary statistics are set as attributes (not methods) as they will be called '000s of times
        # in monte carlo sim in Portfolio class

    def _calculate_mean(self):
        return self.returns.mean() * 252

    def _calculate_std(self):
        return self.returns.std() * sqrt(252)  # number of trading days a year

    # def _calculate_skew(self):
    #     return self.returns.skew()
    #
    # def _calculate_kurtosis(self):
    #     return self.returns.kurtosis()

    def _calculate_corr(self, method='pearson'):
        return self.returns.corr(method=method)

    def _calculate_cov(self):
        return self.returns.cov() * 252

    def _calculate_returns(self):
        return log((self.prices + self.dividends).div(self.prices.shift(1)).iloc[1:])

    def _calculate_cum_returns(self):
        return (self.returns + 1).cumprod() - 1

    def _calculate_var(self):
        return None


class Hist_Data_Plot():
    def __init__(self, securities, provider="YF", start="2000-01-01", end=datetime.date.today(), corr_method='pearson'):
        self.hist_data = Hist_Data(securities, provider=provider, start=start, end=end, corr_method=corr_method)

    def plot_summary(self):
        file_name = "hist_data.html"
        output_file(filename=file_name)
        p = row(self._plot_cumulative_returns(), self._plot_risk_return(), self._plot_correlation())
        save(p)
        return file_name

    def _plot_cumulative_returns(self):
        # Formatting
        cum_returns = figure(title="Cumulative Returns",
                             x_axis_label="Date",
                             x_axis_type="datetime",
                             y_axis_label="Cumulative Return",
                             toolbar_location="below")

        cum_returns.add_tools(HoverTool(
            tooltips=[('Asset', '$name'),
                      ('Date', '$x{%F}'),
                      ('Cumulative Return', '$y{0 %}')],
            formatters={'$x': 'datetime'}))

        cum_returns.yaxis.formatter = NumeralTickFormatter(format='0 %')

        # Plotting
        for security, color in zip(self.hist_data.securities, viridis(len(self.hist_data.securities))):
            cum_returns.line(x='Date',
                             y=security,
                             source=self.hist_data.cum_returns,
                             color=color,
                             line_width=2,
                             name=security,
                             legend_label=security)

        cum_returns.legend.location = "top_left"

        return cum_returns

    def _plot_risk_return(self):
        # Data
        cds = ColumnDataSource(
            data={'Mean Return': self.hist_data.mean,
                  'Standard Deviation': self.hist_data.std,
                  'assets': self.hist_data.securities})

        # Formatting
        risk_return = figure(title="Risk and Return",
                             x_axis_label="Standard Deviation",
                             y_axis_label="Mean Return",
                             toolbar_location="below")

        risk_return.add_tools(HoverTool(
            tooltips=[('Asset', '@assets'),
                      ('Return', '$y{0 %}'),
                      ('Standard Deviation', '$x{0 %}')]))

        risk_return.xaxis.formatter = NumeralTickFormatter(format='0 %')
        risk_return.yaxis.formatter = NumeralTickFormatter(format='0 %')

        # Plotting
        risk_return.circle(x='Standard Deviation',
                           y='Mean Return',
                           color="navy",
                           alpha=3,
                           source=cds)

        return risk_return

    def _plot_correlation(self):
        # Data
        data = self.hist_data.corr.stack().rename("correlation").reset_index()

        # Formatting
        corr_matrix = figure(title="Correlation Matrix",
                             x_range=list(data.level_0.drop_duplicates()),
                             y_range=list(data.level_1.drop_duplicates()),
                             x_axis_location="below",
                             toolbar_location="below")

        colors = viridis(5)

        mapper = LinearColorMapper(palette=colors, low=data.correlation.min(), high=data.correlation.max())

        color_bar = ColorBar(
            color_mapper=mapper,
            location=(0, 0),
            ticker=BasicTicker(desired_num_ticks=len(colors)))

        corr_matrix.add_layout(color_bar, 'right')

        corr_matrix.add_tools(HoverTool(
            tooltips=[('Asset 1', '@level_0'),
                      ('Asset 2', '@level_1'),
                      ('Correlation', '@correlation')]))

        # Plotting
        corr_matrix.rect(
            x="level_0",
            y="level_1",
            width=1,
            height=1,
            source=ColumnDataSource(data),
            line_color=None,
            fill_color=transform('correlation', mapper))

        return corr_matrix

