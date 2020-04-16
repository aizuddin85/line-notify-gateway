#!/bin/env python3
"""
Line Notify Gateway Application
License: MIT
"""

import logging, sys, os
import requests
from datetime import datetime
from flask import Flask, render_template, request, jsonify

LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'
app = Flask(__name__)

if "debug" in os.environ: 
  debug = "on"
else:
  debug = "off"

def reformat_datetime(datetime):
    """
    Reformat of datetime to humand readable.
    """
    datetime = datetime.split('T')
    date = datetime[0]
    time = datetime[1].split('.')[0]
    return date + " " + time

def firing_alert(request):
    """
    Firing alert to line notification with message payload.
    """
    if request.json['status'] == 'firing':
        icon = "⛔⛔⛔"
        status = "Firing"
        # UTC timezone as per SRE best practise and openshift default TZ
        time = reformat_datetime(request.json['alerts'][0]['startsAt'] + ' UTC')
    else:
        icon = "🔷🔷🔷"
        status = "Resolved"
        # UTC timezone as per SRE best practise and openshift default TZ
        time = str(datetime.now().date()) + ' ' + str(datetime.now().time().strftime('%H:%M:%S') + ' UTC')
    header = {'Authorization':request.headers['AUTHORIZATION']}
    for alert in request.json['alerts']:
        msg = "Alertmanager: " + icon + "\nAlert name: " +  alert['labels']['alertname'] + "\nStatus: " + status + "\nSeverity: " + alert['labels']['severity'] + "\nTime: " + time + "\nMessage: " + alert['annotations']['message'] 
        msg = {'message': msg}
        if debug == "on":
          print("Payload: " + str(msg))
        response = requests.post(LINE_NOTIFY_URL, headers=header, data=msg)

@app.route('/')
def index():
    """
    Show summary information on web browser.
    """
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    return jsonify({'status':'success'}), 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    """
    Firing message to Line notify API when it's triggered.
    """
    if debug == "on":
      logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
      logging.debug(str(request.json))
    if request.method == 'GET':
        return jsonify({'status':'success'}), 200
    if request.method == 'POST':
        try:
            firing_alert(request)
            return jsonify({'status':'success'}), 200
        except Exception as err:
            raise err
            return jsonify({'status':'bad request'}), 400

@app.route('/metrics')
def metrics():
    """
    Expose metrics for monitoring tools.
    """

if __name__ == "__main__":
      if debug  == "on":
        app.run(host='0.0.0.0',debug=True)
      else:
         app.run(host='0.0.0.0')
  

