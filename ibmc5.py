from flask import Flask, render_template, request, current_app, jsonify
from ibm_watson import TextToSpeechV1, SpeechToTextV1, ApiException
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
        response = ttsService.synthesize(postData["text"], accept='audio/mp3',voice=postData["lang"]).get_result()
        return jsonify({"blobB64": "data:audio/mpeg;base64,{}".format(base64.b64encode(response.content).decode("utf-8"))})
    elif command == "langlist":
        voices = ttsService.list_voices().get_result()
        result = []
        for voice in voices["voices"]:
            result.append({"text": voice["description"], "value": voice["name"]})
        return jsonify(result)
    elif command == "modellist":
        models = sttService.list_models().get_result()
        result = []
        for model in models["models"]:
            result.append({"text": model["description"], "value": model["name"]})
        return jsonify(result)
    elif command == "stt":
        uri = DataURI(postData["blobB64"])
        response = sttService.recognize(audio=uri.data, content_type=uri.mimetype, word_alternatives_threshold=0.9, keywords=['yes', 'no', 'option', 'one', 'two', 'three', 'four'], keywords_threshold=0.9).get_result()
        if len(response['results']) > 0:
            return jsonify({"text": response['results'][0]["alternatives"][0]["transcript"]})
        else:
            return  jsonify({"text": "nothing"})

@web.route("/<path:path>")
def staticFiles(path):
    return current_app.send_static_file(path.lstrip("/"))

if __name__ == '__main__':
    print("IBM Challenge 5 WSGI Server")
    print("Powered by the Magnificent Six 2019, All Rights Reserved.")
    print()
    port = input("Port number for HTTP service (leave blank for 80): ")
    while True:
        ttsKey = input("IBM Watson Text to Speech API key: ")
        sttKey = input("IBM Watson Speech to Text API key: ")
        ttsService = TextToSpeechV1(url='https://gateway-lon.watsonplatform.net/text-to-speech/api', iam_apikey=ttsKey)
        sttService = SpeechToTextV1(url='https://gateway-lon.watsonplatform.net/speech-to-text/api', iam_apikey=sttKey)
        try:
            print("Initialising Text to Speech service...")
            ttsService.list_voices()
            print("Initialising Speech to Text service...")
            sttService.list_models()
            break
        except ApiException as ex:
            print("Service initialising failed with status code {}: {}".format(ex.code, ex.message))
            print("Please try another key.")
    web.run(host="0.0.0.0", port=port if port != "" and port.isnumeric() else "80")