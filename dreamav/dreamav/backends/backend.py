import numpy as np
import magic
import os
import time

from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from dreamav.util import generate_feature_vector_pdf
from dreamav.core import predict

application = Flask(__name__)

@application.route("/")
def Print():
    return "DREAM-AV"

@application.route("/dream_upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        start = time.time()
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file.save(filename)
        file_magic = magic.from_file(filename)

        if "PDF" in file_magic:
            feature = generate_feature_vector_pdf.extract(filename)
            start = time.time()
            result_dict = predict.predict_pdf(feature)
            os.remove(filename)
            return jsonify(result_dict)

        elif "Composite Document" in file_magic:
            f_list = np.array([filename])
            result_dict = predict.predict_msword(f_list, np.zeros((f_list.shape)))
            os.remove(filename)
            return jsonify(result_dict)

        else:
            os.remove(filename)
            return jsonify({
                "unsupported file format": -1
            })


    else:
        return jsonify({
            "Upload check": 1
        })


if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8888, debug=True)