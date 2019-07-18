import config
from os import remove
from watson_developer_cloud.text_to_speech_v1 import TextToSpeechV1


def text2speech(filename='', message=''):
    if filename == '':
        filename = 'F:/Python_Code/IBM/app/static/temp/output.wav'
        print(filename)

    if message == '':
        message = "Hello.Peter!"

    try:
        remove(filename)
    except:
        print("there is no file exist")

    text_to_speech = TextToSpeechV1(
        iam_apikey=config.iam_apikey,
        url=config.url
    )

    response = text_to_speech.synthesize(message, accept='audio/wav', voice=config.watsonvoice)

    with open(filename, 'wb') as audio_file:
        audio_file.write(response.get_result().content)
