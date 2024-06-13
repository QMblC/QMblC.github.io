from flask import Flask, json

from app.TreeCollector import TreeCollector

app = Flask(__name__)

tc = TreeCollector()

@app.route('/')
def get_root():

    root = tc.get_locations()
    return root.toJSON()


app.run(host="0.0.0.0", port=5000)