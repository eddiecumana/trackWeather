# imports
import requests
import string
import json
import math

from crypt import methods
from flask import Flask, render_template, request, flash
from markupsafe import Markup

# applications
app = Flask(__name__)
app.secret_key = "WeatherMan2022"

@app.route("/")
def index():
    html_string = Markup("<h2>Track weather by City</h2>")
    flash(html_string)
    return render_template("index.html")

@app.route("/weather", methods=["POST"])
def weather():

    # collect data from FORM fields
    city = str(request.form['city_input'])

    if city == '':
        html_string = Markup("<h2 class='alertmessage'>Please enter a city name</h2>")

    else:
    
        # collect data from weather API
        api_key = '' # add your openweathermap API key here
        api_url = "https://api.openweathermap.org/data/2.5/weather?units=imperial&appid="+api_key+"&q="+city

        response = requests.get(api_url)
        response.raise_for_status()
        houseData = json.loads(response.text)

        # put into variables
        city_name = houseData['name']
        visibility = houseData['visibility']
        country = houseData['sys']['country']
        humidity = str(houseData['main']['humidity'])
        description = string.capwords(houseData['weather'][0]['description'])

        # condition tempature
        tempature = houseData['main']['temp']
        tempature = str(math.trunc(tempature))
        visibility = houseData['visibility']
        visibility = str(math.trunc(visibility)/1000)

        # call weather icon as a variable
        w_icon = houseData['weather'][0]['icon']
        weather_icon_url = "https://openweathermap.org/img/w/"+w_icon+".png"
    
        html_string = Markup("<h2>"+city_name+", "+country+" Weather</h2><table><tr><td>Sky Condition: "+description+"</td><td><img src='"+weather_icon_url+"'/></td></tr><tr><td colspan='2'>Current Temapure: "+tempature+" F</td></tr><tr><td colspan='2'>Current Humidity: "+humidity+"%</td></tr><tr><td colspan='2'>Current Visibilty: "+visibility+" Miles</td></tr></table>")

    flash(html_string)
    return render_template("index.html")

    # end of application
