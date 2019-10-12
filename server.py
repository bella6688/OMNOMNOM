#%%
from flask import Flask, request, jsonify
import json
import requests
import csv,re
import os
from custom_dict import InsensitiveDictReader

app = Flask(__name__)
port = int(os.environ["PORT"])
print(port)


@app.route('/', methods=['POST'])
def index():
    print(port)
    data = json.loads(request.get_data().decode('utf-8'))

    # FETCH THE AREA, CUISINE FROM 
    restaurant_area = data['conversation']['memory']['area']['raw']
    restaurant_cuisine = data['conversation']['memory']['cuisine']['raw']

    with open('restaurant_ber.csv', encoding='utf-8') as csvfile:
      reader = InsensitiveDictReader(csvfile)
      #reader = csv.DictReader(csvfile)
      #   Cuisine="Cafes & Coffee"
      #   Location="Bedok"

      cuisine = restaurant_cuisine
      area  = restaurant_area
      pat = re.compile(cuisine.lower())
      patA = re.compile(area.lower())
      Name = cuisine +  " food in " + area + "\n"
      no_index=0
      for line in reader:
        if patA.search(line['area'].lower()) != None:
          if pat.search(line['categories'].lower()) != None:  # Search for the pattern. If found,
            #print(line['name'], line['categories'], line['area'])
 #           Name = Name + " : " + line['name']
            no_index=no_index+1
            Name = Name + " [" + str(no_index) + "] " + line['name']  + ' $' + line['price'] + "\n"

    return jsonify(
                          status=200,
                          replies=[{
                              'type': 'text',
                              'content': (Name)
                                  }]
                          )


@app.route('/errors', methods=['POST'])
def errors():
    print(json.loads(request.get_data()))
    return jsonify(status=200)

#app.run(port=port)
app.run(port=port, host="0.0.0.0")
