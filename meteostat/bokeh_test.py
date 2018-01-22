import pandas
from bokeh.plotting import figure, output_file, show
df = pandas.read_csv('/home/pi/Desktop/meteostation/meteostat/meteo.csv')
plot = figure(plot_width=800, plot_height=250)
plot.line(y=df.Temperature, x=df.Time)
output_file('/home/pi/Desktop/meteostation/meteostat/templates/tempplot.html')
show(plot)