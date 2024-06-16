from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

from cfg import app
from TreeCollector import TreeCollector, ExcelParser, UserDb

#Создать структуру
#Доделать распределение determine_type
#Генерить id для каждого элемента


@app.route('/')
def main():

    return 'main'

@app.route('/api/get-root/<string:name>/')
def get_main_root(name):
    root = TreeCollector.get_root(name)
    return root.toJSON()

@app.route('/api/get-root/<string:path>')
def get_root(path: str):
    return "None"

@app.route('/api/get-filter-data')
def get_filter_data():
    a = TreeCollector.get_filter_data()
    return jsonify(a)


#UserDb.delete_table()
#UserDb.create_table()

#a = ExcelParser.get_rows("app/Tables/Structure.xlsx")

#for i in a:
    #ExcelParser.insert_staff_db(i)

app.run(host="0.0.0.0")