from dream.util.predict import predict

from flask import Flask, request
application = Flask(__name__)

@application.route("/")
def Print():
    return "DREAM(Detecting in Real-timE mAlicious document using Machine learning)"


@application.route("/predict", methods=["PUT", "POST"])
def get_feature():
    pass


if __name__ == '__main__':
    application.run()