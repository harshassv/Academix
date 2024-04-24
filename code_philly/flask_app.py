from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from checker import checker
# from RAG import RAG,RAG_query

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
h_history=open('history.txt','w')
# count = 0
# if not count:
h_history.write('')
# count 
h_history.close()


@app.route('/receive_data', methods=['POST'])
def receive_data():
    
    fp = open('current_url.txt','w')
    data = request.json
    if '&' in  data['url']:
        location = data['url'].find('&')
        data['url'] = data['url'][:location+1]
        print('url =',data['url'])
    else:
        data['url'] = data['url']
    response_data = {"status": "success"}
    fp.write(data['url'])
    
    # json.dump(data,fp)
    fp.close()
    
    # with open('data.json', 'r') as json_file:
    # # Load the JSON data
    #     data = json.load(json_file)

    checker(data)

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
