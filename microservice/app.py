import json
from os import getenv

from flask import Flask
from flask import request
import pandas as pd
from dotenv import find_dotenv, load_dotenv

from utils import generate_alphabet_elements, load_from_pkl_file, create_features


class LanguageDetectorService():

    def __init__(self):

        # Set config values
        if find_dotenv() != "":
            load_dotenv()
        self.MODEL_TYPE = getenv("MODEL_TYPE", "gradient_boost")
        self.SCALER_PATH = getenv("SCALER_PATH", "models_in_pkl/scaler.pkl")
        self.PCA_PATH = getenv("PCA_PATH", "models_in_pkl/pca.pkl")
        self.GRAD_BOOST_MODEL_PATH = getenv("GRAD_BOOST_MODEL_PATH", "models_in_pkl/gradient_boost_model.pkl")
        self.DECISION_TREE_MODEL_PATH = getenv("DECISION_TREE_MODEL_PATH", "models_in_pkl/decision_tree_model.pkl")
        self.HOST = getenv("HOST", "0.0.0.0")
        self.PORT = getenv("PORT", 5000)
        self.DEBUG = getenv("DEBUG")

        # Load models
        self.alphabet_elements = generate_alphabet_elements()
        self.scaler = load_from_pkl_file(self.SCALER_PATH)
        self.pca = load_from_pkl_file(self.PCA_PATH)
        
        self.models = {}
        self.models['gradient_boost'] = load_from_pkl_file(self.GRAD_BOOST_MODEL_PATH)
        self.models['decision_tree'] = load_from_pkl_file(self.DECISION_TREE_MODEL_PATH)

        self.app = Flask(__name__)

        @self.app.route('/')
        def hello():
            return 'Detect language at route: /detect'

        @self.app.route('/detect/<string:text>')
        def changeroute(text):

            model_selection_str = request.args.get('model')

            try:
                if self.models[model_selection_str] is not None:
                    print(f"Using '{model_selection_str}' model")
            except KeyError:
                print(f"'{model_selection_str}' model is not found.")
                model_selection_str = 'gradient_boost'
                print("Using default model: 'gradient_boost'")

            print(f"Detecting language for the following text:\n{text}")
            result = self.detect_language(text, model_selection_str)       # 'grad_boost' or 'decision_tree'

            response = {
                'language': result
            }

            return json.dumps(response)

    def start(self):
        self.app.run(host=self.HOST, port=self.PORT, debug=self.DEBUG)

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


if __name__ == '__main__':
    language_detector_service = LanguageDetectorService()
    language_detector_service.start()
