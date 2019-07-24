from flask import Flask, render_template, request, current_app, jsonify
from ibm_watson import TextToSpeechV1, SpeechToTextV1
from datauri import DataURI
import json
import base64

web = Flask(__name__)

@web.route("/")
def index():
    return current_app.send_static_file("index.html")

@web.route("/dynamic/<command>", methods=["POST"])
def dynamic(command):
    postData = request.form
    if command == "tts":
        service = TextToSpeechV1(url='https://gateway-lon.watsonplatform.net/text-to-speech/api', iam_apikey='04Z3vK9211huu2-VdfDxBGll7u90TQn_A1I_z0hjSPlc')
        response = service.synthesize(postData["text"], accept='audio/mp3',voice=postData["lang"]).get_result()
        return jsonify({"blobB64": "data:audio/mpeg;base64,{}".format(base64.b64encode(response.content).decode("utf-8"))})
    elif command == "langlist":
        service = TextToSpeechV1(url='https://gateway-lon.watsonplatform.net/text-to-speech/api', iam_apikey='04Z3vK9211huu2-VdfDxBGll7u90TQn_A1I_z0hjSPlc')
        voices = service.list_voices().get_result()
        result = []
        for voice in voices["voices"]:
            result.append({"text": voice["description"], "value": voice["name"]})
        return jsonify(result)
    elif command == "modellist":
        service = SpeechToTextV1(url='https://gateway-lon.watsonplatform.net/speech-to-text/api', iam_apikey='H8hCy1Zih1Ffy8TWuBOQQ0YE5Nbo2yNBh-IXJsq2-1uk')
        models = service.list_models().get_result()
        result = []
        for model in models["models"]:
            result.append({"text": model["description"], "value": model["name"]})
        return jsonify(result)
    elif command == "stt":
        uri = DataURI(postData["blobB64"])
        service = SpeechToTextV1(url='https://gateway-lon.watsonplatform.net/speech-to-text/api', iam_apikey='H8hCy1Zih1Ffy8TWuBOQQ0YE5Nbo2yNBh-IXJsq2-1uk')
        response = service.recognize(audio=uri.data, content_type=uri.mimetype, word_alternatives_threshold=0.9, keywords=['yes', 'no', 'option', 'one', 'two', 'three', 'four'], keywords_threshold=0.9).get_result()
        print(json.dumps(response))
        return jsonify({"text": response['results'][0]["alternatives"][0]["transcript"]})

@web.route("/<path:path>")
def staticFiles(path):
    return current_app.send_static_file(path.strip("/"))

if __name__ == '__main__':
    web.run(host="0.0.0.0", port="8000")