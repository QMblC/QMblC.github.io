from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

from cfg import app
from TreeCollector import TreeCollector, ExcelParser, UserDb

#Создать структуру
#Доделать распределение determine_type
#Генерить id для каждого элемента


@app.route('/')
def get_root():

    return 'main'

@app.route('/api/get-root/<string:name>/')
def get_main_root(name):
    root = TreeCollector.get_root(name)
    return root.toJSON()

@app.route('/test')
def test():

    return {"members" : ["m1", "m2", "m3"]}

#UserDb.delete_table()
#UserDb.create_table()

#a = ExcelParser.get_rows("app/Tables/Structure.xlsx")

#for i in a:
    #ExcelParser.insert_staff_db(i)
app.run(host="0.0.0.0", port=5000)