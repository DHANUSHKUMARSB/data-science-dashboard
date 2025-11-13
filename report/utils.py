from pathlib import Path
import pickle

# Root is project root (two parents above this file: report/ -> project root)
ROOT_PATH = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT_PATH / "assets" / "model.pkl"

def load_model():
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model
