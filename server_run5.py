from flask import Flask, request, jsonify
import json
import requests
import os
import csv,re

from custom_dict import InsensitiveDictReader

app = Flask(__name__)
#port = 5000
port = int(os.environ["PORT"])
print(port)


@app.route('/', methods=['POST'])
def index():
    print(port)
    data = json.loads(request.get_data().decode('utf-8'))

    # FETCH THE CRYPTO NAME
#    crypto_name = data[“nlp”][“entities”][“crypto_name”][0][“raw”]
#    crypto_location = data['conversation']['memory']['location']['raw']
    crypto_area = data['conversation']['memory']['area']['raw']
    crypto_cuisine = data['conversation']['memory']['cuisine']['raw']

    # FETCH BTC/USD/EUR PRICES
    with open('restaurant_ber.csv', encoding='utf-8') as csvfile:
      reader = InsensitiveDictReader(csvfile)
      #reader = csv.DictReader(csvfile)
      #   Cuisine="Cafes & Coffee"
      #   Location="Bedok"
#      Location = crypto_location
      Cuisine = crypto_cuisine
      Area  = crypto_area
      pat = re.compile(Cuisine.lower())
#      patL = re.compile(Location.lower())
      patA = re.compile(Area.lower())
      Name=Cuisine +  " food in " + Area + "\n"
      No_index=0
      for line in reader:
 #       if ((patL.search(line['area'].lower()) != None) or (patA.search(line['area'].lower()) != None)):
        if patA.search(line['area'].lower()) != None:
          if pat.search(line['categories'].lower()) != None:  # Search for the pattern. If found,
            #print(line['name'], line['categories'], line['area'])
 #           Name = Name + " : " + line['name']
            No_index=No_index+1
            Name = Name + " [" + str(No_index) + "] " + line['name']  + "\n"

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
