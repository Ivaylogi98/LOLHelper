from flask import Flask, render_template, request
import json

config = {
    "DEBUG": True  # run app in debug mode
}

def get_vs_data(champion, enemy):
    with open(f'assets/vsData/{champion}.json') as f:
        data = json.load(f)
    return data[enemy]

def get_champion_names():
    with open('assets/championNames.txt') as f:
        championNames = f.readline().split(',')
    return championNames


app = Flask(__name__)

@app.route("/")
def index():
    championNames = get_champion_names()
    return render_template("index.html", champions=championNames)

@app.route('/vsdata', methods=['GET'])
def vsdata():
    champion = request.args.get("champion")
    enemy = request.args.get("enemy")

    build=[[]]
    data = get_vs_data(champion, enemy)
    
    summary = data['summary']
    build = data['build']
    tips = data['tips']
    championNames = get_champion_names()
    return render_template("vsdata.html", champions=championNames, champion=champion, enemy=enemy, summary=summary, build=build, tips=tips)