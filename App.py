from flask import Flask, json

from TreeCollector import TreeCollector

application = Flask(__name__)

tc = TreeCollector()

@application.route('/')
def get_root():

    root = tc.get_locations()
    return root.toJSON()

if __name__ == '__main__':
    application.run(debug = True)