from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from random import randint
import get_api_data
import data_generator
import datetime
import pandas
from bokeh.plotting import figure, output_file

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=None)
global df
df = pandas.DataFrame(columns=['Temperature','Humidity','Pressure','Sea_level_pressure','Altitude','Noise_level','Light_intensity','Time'])

@app.route('/')
def home():
    apiData = get_api_data.getOWMData()
    sunrise = datetime.datetime.fromtimestamp(apiData['sys']['sunrise']).strftime("%H:%M:%S")
    sunset = datetime.datetime.fromtimestamp(apiData['sys']['sunset']).strftime("%H:%M:%S")
    return render_template("main.html", city = apiData['name'], temp = apiData['main']['temp'] - 273.15, conditions = apiData['weather'][0]['main'], cloudDescr = apiData['weather'][0]['description'],humidity = apiData['main']['humidity'], windSpeed = apiData['wind']['speed'], windDirection = apiData['wind']['deg'], sunrise = sunrise, sunset = sunset, time = datetime.datetime.now().strftime("%H:%M:%S"), date = datetime.datetime.now().strftime("%Y/%m/%d"))

@app.route('/tempplot')
def tempplot():
    df = pandas.read_csv('/home/pi/Desktop/meteostation/meteostat/meteo.csv')
    plot = figure(plot_width=800, plot_height=250)
    plot.line(y=df.Temperature, x=df.Time)
    output_file('/home/pi/Desktop/meteostation/meteostat/templates/tempplot.html')
    return render_template("tempplot.html")
    
@socketio.on('my_ping')
def ping_pong():
    i = False
    df2 = 0
    if i==False:
        data = data_generator.getSensorData(df)
        df2 = data[1]
        i=True
    else:
        data = data_generator.getSensorData(df2)
        df2 = data[1]
        
    number1 = data[0]["temp"]
    number2 = data[0]["humidity"]
    number3 = data[0]["pressure"]
    number4 = data[0]["noise"]
    number5 = data[0]["altitude"]
    number6 = data[0]["lux"]
    emit('pong',{'temp':number1, 'humidity':number2, 'pressure':number3, 'noise':number4, 'elevation':number5, 'lux':number6})
                    
if __name__ == '__main__':
   socketio.run(app,debug = True)
