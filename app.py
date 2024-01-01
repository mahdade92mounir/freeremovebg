from flask import Flask, render_template, jsonify, request
from utils.background import remove_bg_image
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 
warnings.filterwarnings("ignore", category=UserWarning) 
import gc

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/removebg", methods=["POST"])
def remove_bg():
    image = request.json.get("image")
    
    if image is not None:
        result = remove_bg_image(
            image, 
            to_base64=True, 
            myme=True,
            _format="png"
        )
        response = {
            "result": result
        }
        gc.collect()  # Forcez la libération de la mémoire
        return response
    return "Something went wrong!"


if __name__ == '__main__':
    app.run(host='0.0.0.0')