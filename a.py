from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/first", methods=["GET"])
def aaa():#+ids
    return jsonify(
        {
            "name": "Брусника",
            "path": "first",
            "children": [
                {
                    "name": "west",
                    "info": {
                        "people" : "person1",
                        "boss" : "boss1"
                    },
                    "path-to-children": "/api/second"
                }, 
                {
                    "name": "south",
                    "info": "321",
                    "path-to-children": "/api/second"
                },
                                {
                    "name": "west",
                    "info": "123",
                    "path-to-children": "/api/second"
                }, 
                                {
                    "name": "west",
                    "info": "123",
                    "path-to-children": "/api/second"
                }, 
                                {
                    "name": "west",
                    "info": "123",
                    "path-to-children": "/api/second"
                }, 
            ]
        }
    )

@app.route("/api/second", methods=["GET"])
def bbb():
    return jsonify(
        {
            "name": "Новая Брусника",
            "path": "first\second",
            "children": [
                {
                    "name": "west2",
                    "info": "12345",
                    "path-to-children": "/api/second"
                }, 
                {
                    "name": "south2",
                    "info": "321012",
                    "path-to-children": "/api/second"
                }
            ]
        }
    )

def bbd():
    return jsonify(
        {
            "locations": [
                {
                    "name": "Москва",
                    "parent": [{
                        "location" : "loc",
                        "division" : "division",
                        "departament" : "..."
                    },
                    {
                        "location" : "loc",
                        "division" : "division",
                        "departament" : "..."
                    }],
                    "children": [
                        "подразделение а",
                        "подразделение б"
                    ]
                },
                {
                    "name": "Екб",
                    "parent": "",
                    "children": []
                }
            ],
            "subdivision": [
                {
                    "name": "подразделение а",
                    "parent": "Москва",
                    "children": [
                        "департамент 1"
                    ]
                },
                {
                    "name": "подразделение б",
                    "parent": "Москва",
                    "children": [
                        "департамент 2"
                    ]
                }
            ],
            "department": [
                {
                    "name": "департамент 1",
                    "parent": "подразделение а",
                    "children": [
                        "Альфа",
                        "Бета"
                    ]
                },
                {
                    "name": "департамент 2",
                    "parent": "подразделение б",
                    "children": []
                }
            ],
            "group": [
                {
                    "name": "альфа",
                    "parent": "департамент 1",
                    "children": [
                        "Альфа",
                        "Бета"
                    ]
                },
                {
                    "name": "бета",
                    "parent": "департамент 1",
                    "children": []
                }
            ]
        }
    )