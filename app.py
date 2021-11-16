from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import csv
import json

app = Flask(__name__)
api = Api(app)

items = [] 

with open("live_tag_data.csv", "r") as f:  # opens the csv in read mode
    reader = csv.reader(f)
    next(reader)
    data = []
    for row in reader:
        data.append({'id': row[0], 'description': row[1],
        'name': row[2], 'value': row[3], 'type': row[4], 'start_time': row[5],
        'end_time': row[6], 'condition': row[7]})

with open("equipments.json", "w") as f:  # opens the csv in write mode
    json.dump(data, f, indent=4)

with open('./equipments.json') as access_json:
        equipments = json.load(access_json)
        for item in equipments:

            id = item['id']
            description = item['description']
            name = item['name']
            value = item['value']
            type = item['type']
            start_time = item ['start_time']
            end_time = item['end_time']
            condition = item['condition']

            equip = {
                'id': id,
                'description': description,
                'name': name,
                'value': value,
                'type': type, 
                'start_time': start_time, 
                'end_time': end_time, 
                'condition': condition 
            }
            items.append(equip)

equipments = data


class Item(Resource):
    global items

    #@app.route ('/item/<name>' , methods = ['GET'], endpoint = 'get_name')
    def get(self, name): #Function gets each element of the list when it's called by the name 
        for item in items: 
            if item['name'] == name:
                return item 
        return {'item': None}, 404

    #@app.route ('/item/<id>', methods = ['GET'], endpoint = 'get_id')
    def get_id(id): # Function gets each element of the list when its called by the id 
        for item in items: 
            if item['id'] == id:
                return item 
        return {'item': None}, 404
    

    @app.route ('/item/<name>' , methods = ['POST'], endpoint = 'post_item')
    def post_item(name): 
        datas = request.get_json()
        item = {'name': name, 'id': datas['id'], 'description': datas['description'], 
        'value': datas['value'], 'type': datas['type'], 'start_time': datas['start_time'],
         'end_time': datas['end_time'], 'condition': datas['condition']}
        items.append(item)

        with open("equipments.json", "w") as f:  # opens the csv in write mode
            data.append(item)
            json.dump(data, f, indent=4)
        return item, 201


class EquipmentList(Resource):
    def get(self):
        return equipments #{'equipments' : equipments}


api.add_resource(Item, '/item/<name>')
#api.add_resource(Item, '/items/<id>')
api.add_resource(EquipmentList, '/equipments')

if __name__ == "__main__":
    app.run(port=8500, debug = True)