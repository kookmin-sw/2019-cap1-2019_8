from flask import Flask, request, jsonify

import magic

from dreamav.core import generate_feature_vector_pdf
from dreamav.util import predict

application = Flask(__name__)

@application.route("/")
def Print():
    return "DREAM(Detecting in Real-timE mAlicious document using Machine learning)"


# TODO(@LEO_MOON) Feature extraction and predict based on file
@application.route("/dream_upload", methods=["GET", "POST"])
def upload_file():
    # if request.method == "POST":
    #
    #
    #
    #     f = request.files["file"]
    #
    #     file_magic = magic.from_buffer(f)
    #
    #     if "PDF" in file_magic:
    #         feature = pdf.core(f)
    #
    #         probability = predict.predict(feature, 0)
    #
    #     elif "Word" in file_magic:
    #         pass
    #

    result = 0
    return jsonify({
        "result": 0
    })




if __name__ == '__main__':
    application.run(host="0.0.0.0", port=8888, debug=True)