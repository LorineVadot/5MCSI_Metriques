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

@app.route('/commits/')
def commits():
    try:
        url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
        headers = {'Authorization': 'token YOUR_GITHUB_TOKEN'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for HTTP error responses
        commits_data = response.json()
        
        # Extraire les dates des commits
        commit_times = [commit['commit']['author']['date'] for commit in commits_data]
        
        # Extraire les minutes et compter les commits
        minutes = [datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M') for time in commit_times]
        minute_counts = Counter(minutes)
        
        # Préparer les données pour le graphique
        results = [{'minute': minute, 'count': count} for minute, count in minute_counts.items()]
        
        return jsonify(results=results)
    
    except requests.ConnectionError:
        return jsonify({"error": "Échec de la connexion à l'API GitHub."}), 500
    except requests.Timeout:
        return jsonify({"error": "La requête à l'API GitHub a expiré."}), 500
    except requests.RequestException as e:
        return jsonify({"error": f"Erreur lors de la requête à l'API GitHub: {str(e)}"}), 500
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')
  
if __name__ == "__main__":
  app.run(debug=True)
