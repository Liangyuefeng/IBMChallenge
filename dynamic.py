from flask import Flask, request, jsonify
from ibm_watson import TextToSpeechV1, SpeechToTextV1, ApiException
from datauri import DataURI
import json
import base64
import glob
import os

web = Flask(__name__)

try:
    with open("keys.json", "rb") as keyFile:
        keySet = json.load(keyFile)
        ttsService = TextToSpeechV1(url='https://gateway-lon.watsonplatform.net/text-to-speech/api', iam_apikey=keySet["tts"])
        sttService = SpeechToTextV1(url='https://gateway-lon.watsonplatform.net/speech-to-text/api', iam_apikey=keySet["stt"])
        ttsService.list_voices()
        sttService.list_models()
        flag = 1
except (EnvironmentError, json.JSONDecodeError, ApiException) as e:
    flag = 0

@web.route("/dynamic.py/<command>", methods=["POST"])
def dynamic(command):
    if flag == 1:
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
                return jsonify({"text": "nothing"})
        elif command == "storylist":
            stories = glob.glob("stories/*.json")
            result = []
            for story in stories:
                with open(story, "rb") as storyFile:
                    storyJSON = json.load(storyFile)
                    result.append({"text": storyJSON["header"]["title"]["text"], "value": os.path.basename(story)})
            return jsonify(result)
    else:
        return jsonify({"error": "keyError"})