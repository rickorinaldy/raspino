from flask import Flask, request, render_template, url_for, Response, redirect
from stream import start as sts, stop as sps
from start import start_model
from stop import stop_model
import pandas as pd

app = Flask(__name__)

project = pd.read_csv("project_credential.csv")

project_arn = project.iloc[0]["project"]
model_arn = project.iloc[0]["model"]
version_name = project.iloc[0]["version"]

min_inference_units=1

@app.route('/')
def landing_page():
    return render_template("base.html")

@app.route('/start')
def start():
    # start_model(project_arn, model_arn, version_name, min_inference_units)
    return redirect(url_for('idle'))

@app.route('/idle', methods=["GET","POST"])
def idle():
    if request.method=="POST":
        return render_template("idle.html")
    else:
        return render_template("idle.html")

@app.route("/process")
def process():
    Response(sts(model_arn), mimetype="text")

@app.route("/noprocess")
def noprocess():
    Response(sps())
    
@app.route('/terminate_model')
def terminate_model():
    # stop_model(model_arn)
    return redirect(url_for("landing_page"))



app.run(host = '0.0.0.0')