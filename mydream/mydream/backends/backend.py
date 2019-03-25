from flask import Flask, request, jsonify

import magic

from mydream.extract import pdf
from mydream.util import predict

application = Flask(__name__)


@application.route("/")
def Print():
    return "DREAM(Detecting in Real-timE mAlicious document using Machine learning)"


# TODO(@LEO_MOON) Feature extraction and predict based on file
@application.route("/dream_upload", methods=["POST"])
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
    application.run(host="0.0.0.0", port=8888, debug=True)