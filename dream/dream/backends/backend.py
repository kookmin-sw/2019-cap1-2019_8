from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse

import magic

from dream.extract import pdf
from dream.util import predict

application = Flask(__name__)


@application.route("/")
def Print():
    return "DREAM(Detecting in Real-timE mAlicious document using Machine learning)"


# TODO(@LEO_MOON) Feature extraction based on file
@application.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        f = request.files["file"]

        file_magic = magic.from_buffer(f)

        if "PDF" in file_magic:
            feature = pdf.extract(f)

            probability = predict.predict(feature, 0)


        elif "Word" in file_magic:
            pass

        elif "Hangul" in file_magic:
            pass

        return jsonify({"probability", probability})


if __name__ == '__main__':
    application.run()