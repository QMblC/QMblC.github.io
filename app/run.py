from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

from cfg import app
from TreeCollector import TreeCollector, ExcelParser, UserDb

#Создать структуру
#Доделать распределение determine_type
#Генерить id для каждого элемента

CORS(app)

@app.route('/')
def main():

    return 'main'

@app.route('/api/get-root/<string:name>')
def get_main_root(name):
    root = TreeCollector.get_root(name)
    return root

@app.route('/api/get-filter-data')
def get_filter_data():
    a = TreeCollector.get_filter_data()
    return jsonify(a)

@app.route('/api/get-path', methods = ['POST'])
def get_path():
    data_type = request.json['id']
    name = request.json['name']
    a = TreeCollector.get_path(data_type, name)
    return a

@app.route('/test/1_2_3_4')
def tes():
    return "yes"


UserDb.delete_table()
UserDb.create_table()

a = ExcelParser.get_rows("Structure.xlsx")#для докер удалить app

for i in a:
    ExcelParser.insert_staff_db(i)

app.run(host="0.0.0.0")


