#!/usr/bin/env python3
from flask import Flask, request, jsonify
from prediction import transform_to_image, predict
import urllib

def load_image_from_url(url):
    # import os
    # data_dir = '../data/real-world/'
    # file = os.path.join(data_dir, url)
    # load
    file = urllib.request.urlopen(url)
    return transform_to_image(file)

def load_image_from_file(name):
    import os
    data_dir = '../data/real-world/'
    file = os.path.join(data_dir, name)
    return transform_to_image(file)

app = Flask(__name__)


@app.route('/')
def predict_url():
    json = request.json
    url = json['url']
    print ('url:', url)
    if 'model' in json:
        model = json['model']
    else:
        model = 'default'
    print ('model:', model)
    image = load_image_from_url(url)
    # image = load_image_from_file('1000/70-house-detail.jpg')
    predicted_category, prediction = predict(image, model)

    response = {
        'category': predicted_category.tolist(),
        'prediction': prediction.tolist(),
        'model': model
    }
    return jsonify(response)

# Can not use Debug, lets Flask mess with tensorflow as it seems
# http://stackoverflow.com/questions/41991756/valueerror-tensor-is-not-an-element-of-this-graph
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8888)
    # app.run(debug=False)

