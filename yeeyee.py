from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import numpy as np
import cv2
from urllib.request import Request
from urllib.request import urlopen

bot = Flask(__name__)
cors = CORS(bot, resources={r"/": {"origins" : "*"}})
api = Api(bot)

catparser = reqparse.RequestParser()
catparser.add_argument("url", type=str)

class cat_test(Resource):
    def post(self):
        args = catparser.parse_args()

        pic_ext = ['.jpg', '.png', '.jpeg']

        try:
            for ext in pic_ext:
                if args["url"].endswith(ext):
                    print('testing')
                    #image = cv2.imread(message.attachments[0])
                    req = Request(args["url"], headers = {"User-Agent": "Mozilla/5.0"})
                    resp = urlopen(req)
                    arr = np.asarray(bytearray(resp.read()), dtype="uint8")
                    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)

                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                    detector = cv2.CascadeClassifier('util/haarcascade_frontalcatface.xml')
                    rects = detector.detectMultiScale(gray, scaleFactor=1.3,
                        minNeighbors=5, minSize=(75, 75))

                    if np.any(rects):
                        return {"eval" : True, "rects" : rects.tolist()}
                    else:
                        return {"eval" : False, "rects" : str(None)}
        except Exception as e:
            return {"eval" : False, "error" : str(e)}

spaceparser = reqparse.RequestParser()
spaceparser.add_argument("sample", type=str)
spaceparser.add_argument("spacing", type=int)

class space(Resource):
    def post(self):
        args = spaceparser.parse_args()
        newstr = ""
        for char in args["sample"]:
            newchar = char + (" " * args["spacing"])
            newstr += newchar
        return {"spaced" : newstr}

ohnoparser = reqparse.RequestParser()
ohnoparser.add_argument("text", type=str)

class kill_me(Resource):
    def post(self):
        text = ohnoparser.parse_args()["text"]
        cursed = ""
        for i in text:
            if i.lower() in ["r", "l"]:
                cursed += "w"
            else:
                cursed += i
        cursed += " uwu <3"
        return {"oh no bro" : cursed}

api.add_resource(kill_me, "/api/uwu", methods=['POST'])
api.add_resource(space, "/api/space", methods=['POST'])
api.add_resource(cat_test, "/api/test", methods=['POST'])

if __name__ == "__main__":
    bot.run(debug=True, port=8000)
