from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import os
import readFiles
#import requests
import random

app = Flask(__name__)
cors = CORS(app)

@app.route('/ocr', methods=['POST'])
@cross_origin()
def post():
        hash = random.getrandbits(64)
        path = os.path.join('./files', f'{hash}')
        os.mkdir(path)
        UPLOAD_FOLDER = path
        try:
            #token = request.headers['Authorization'].replace("Bearer ", "")
            #print(request.files, flush=True)
            for counter in range(len(request.files)):
                file = request.files.getlist(f'{counter}')[0]
                print(file, flush=True)
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))
                counter = counter + 1
            
            data = readFiles.main(UPLOAD_FOLDER)
            for file in os.scandir(UPLOAD_FOLDER):
                os.remove(file)
            os.rmdir(UPLOAD_FOLDER)
            return jsonify(data)
                
        except Exception as e: 
            print(e, flush=True)
            response = jsonify({'error': True, 'message': "Aconteceu um erro"})
            return response

@app.route('/', methods=['GET'])
@cross_origin()
def get():
    return jsonify({'hello': 'world'})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
