from os import getenv
from dotenv import find_dotenv, load_dotenv

class Config():
    def __init__(self):
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
