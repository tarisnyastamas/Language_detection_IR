import json
import datetime

import validators
from flask import Flask
from flask import request
import pandas as pd

from config import Config
from utils import generate_alphabet_elements, load_from_pkl_file, create_features, load_url, cleaning


class LanguageDetectorService():

    def __init__(self):

        # Set config values
        print(f'{datetime.datetime.now()} [ INFO ] Setting config values, building alphabet element, loading models...')
        self.config = Config()

        # Load models
        self.alphabet_elements = generate_alphabet_elements()
        self.scaler = load_from_pkl_file(self.config.SCALER_PATH)
        self.pca = load_from_pkl_file(self.config.PCA_PATH)
        
        self.models = {}
        self.models['gradient_boost'] = load_from_pkl_file(self.config.GRAD_BOOST_MODEL_PATH)
        self.models['decision_tree'] = load_from_pkl_file(self.config.DECISION_TREE_MODEL_PATH)
        print(f'{datetime.datetime.now()} [ INFO ] Loaded {list(self.models.keys())} models')

        self.app = Flask(__name__)

        @self.app.route('/')
        def hello():
            return 'Detect language at route: /detect'

        @self.app.route('/detect/<string:input>')
        def changeroute(input):
            url = request.args.get('url')
            if url is not None:
                if validators.url(url):
                    print(f'{datetime.datetime.now()} [ INFO ] Working with URL: {url}')
                    html = load_url(url)
                    text = cleaning(html)
                else:
                    print(f"{datetime.datetime.now()} [ WARNING ] URL is invalid, working with input: '{input}'")
                    text = input
            else:
                print(f"{datetime.datetime.now()} [ INFO ] Working with simple text: {input}")
                text = input

            # Check model selector string
            model_selection_str = self.select_model(request.args.get('model'))

            # Detect the language of the text/website
            if url is None:
                print(f"{datetime.datetime.now()} [ INFO ] Detecting the language of this text: {text}")
            else:
                print(f"{datetime.datetime.now()} [ INFO ] Detecting the language of this website: {url}")

            result = self.detect_language(text, model_selection_str)       # 'grad_boost' or 'decision_tree'
            print(f'{datetime.datetime.now()} [ OUTPUT ] Detected language: {result}')

            # Create a response and return it
            response = {
                'language': result
            }
            return json.dumps(response)

    def start(self):
        print(f'{datetime.datetime.now()} [ INFO ] Starting language detection service at: http://{self.config.HOST}:{self.config.PORT}/')
        self.app.run(host=self.config.HOST, port=self.config.PORT, debug=self.config.DEBUG)

    def transform_input_text(self, text):
        text_df = pd.DataFrame([text], columns = ['Sentences'])
        text_df = create_features(text_df, self.alphabet_elements)

        feature_cols = list(text_df.columns)[1:]

        x = text_df[feature_cols]

        x = self.scaler.transform(x)
        x = self.pca.transform(x)

        return x

    def detect_language(self, text, model_type):

        x = self.transform_input_text(text)
        y_pred = self.models[model_type].predict(x)

        return y_pred[0]

    def select_model(self, model_selection_str):
        try:
            if self.models[model_selection_str] is not None:
                print(f"{datetime.datetime.now()} [ INFO ] Using '{model_selection_str}' model")
        except KeyError:
            print(f"{datetime.datetime.now()} [ WARNING ] '{model_selection_str}' model is not found. Using default model: 'gradient_boost'")
            model_selection_str = 'gradient_boost'
        return model_selection_str


if __name__ == '__main__':
    language_detector_service = LanguageDetectorService()
    language_detector_service.start()
