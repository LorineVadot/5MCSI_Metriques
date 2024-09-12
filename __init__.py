from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)       

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("graphique.html")

@app.route('/test_commits/')
def test_commits():
    try:
        url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
        headers = {'Authorization': '7f970836ef744327b36b3f08eb37a640'}
        response = requests.get(url, headers=headers)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
  
if __name__ == "__main__":
  app.run(debug=True)
