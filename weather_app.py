from flask import Flask, request, render_template
from config import API_KEY
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def weather():
    api_key = API_KEY
    city = request.form.get('city')

    if city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
        weather_info = requests.get(url)

        if weather_info.json().get('cod') == 404:
            result = "No city found"
        else:
            try:
                weather = weather_info.json()['weather'][0]['main']
                temp = round(weather_info.json()['main']['temp']) - 273.15
                result = f"The weather in {city} is: {weather}<br>The temperature in {city} is: {temp:.2f} ºC"
            except KeyError:
                result = "No weather data found"
    else:
        result = ""

    return render_template('weather.html', result=result)


if __name__ == "__main__":
    app.run(debug=True)
