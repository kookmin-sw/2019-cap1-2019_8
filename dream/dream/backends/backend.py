from flask import Flask, request
from flask_restful import Resource, Api, reqparse

from dream.extract import pdf

application = Flask(__name__)


@application.route("/")
def Print():
    return "DREAM(Detecting in Real-timE mAlicious document using Machine learning)"


# TODO(@LEO_MOON) Feature extraction based on file
@application.route("/upload")
def upload_file():
    if request.method == "POST":
        f = request.files["file"]





if __name__ == '__main__':
    application.run()