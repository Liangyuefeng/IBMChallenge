from ibm_watson import SpeechToTextV1
from os.path import join, dirname
import json
import os


def main():
    directory = "audio"
    for filename in os.listdir(r'./' + directory):
        stt(filename)
        # print(filename)


def stt(audio_name, text_name="text.txt", audio_path="./audio/", text_path="./text/"):
    speech_to_text = SpeechToTextV1(
        iam_apikey='GbMDTvaUm4mwVHY9hOnY9ixYiyB24bOBVIMrGFcHxjTL',
        url='https://gateway-lon.watsonplatform.net/speech-to-text/api'
    )

    # recognize audio
    with open(join(dirname(__file__), '%s%s' % (audio_path, audio_name)),
                   'rb') as audio_file:
        speech_recognition_results = speech_to_text.recognize(
            audio=audio_file,
            speaker_labels=True,
        ).get_result()

    # output text file
    # speaker_labels

    ls_sl = speech_recognition_results['speaker_labels']
    different_speaker = False
    with open('%s%s' % (text_path, text_name), 'a') as text:
        text.write("Speaker Labels:\n")
        ft = ls_sl[0]["from"]
        for j in range(len(ls_sl)):
            if different_speaker is True:
                ft = ls_sl[j]["from"]   # from time
                different_speaker = False

            if j == len(ls_sl) - 1:
                if ls_sl[j]["speaker"] == ls_sl[j-1]["speaker"]:
                    tt = ls_sl[j]["to"]   # to time
                    text.write("Time: %s to %s\n" % (time_transfer(int(ft)), time_transfer(int(tt))))
                    text.write("Speaker: %s\n\n" % (ls_sl[j]["speaker"]))
                else:
                    tt = ls_sl[j-1]["to"]  # to time
                    text.write("Time: %s to %s\n" % (time_transfer(int(ft)), time_transfer(int(tt))))
                    text.write("Speaker: %s\n\n" % (ls_sl[j-1]["speaker"]))

                    ft = ls_sl[j]["from"]
                    tt = ls_sl[j]["to"]   # to time
                    text.write("Time: %s to %s\n" % (time_transfer(int(ft)), time_transfer(int(tt))))
                    text.write("Speaker: %s\n\n" % (ls_sl[j]["speaker"]))
            elif ls_sl[j]["speaker"] != ls_sl[j+1]["speaker"]:
                different_speaker = True
                tt = ls_sl[j]["to"]   # to time
                text.write("Time: %s to %s\n" % (time_transfer(int(ft)), time_transfer(int(tt))))
                text.write("Speaker: %s\n\n" % (ls_sl[j]["speaker"]))
        text.write("Transcript:")
    # transcript
    ls = speech_recognition_results['results']
    for i in range(len(ls)):
        start_time = round(speech_recognition_results['results'][i]['alternatives'][0]['timestamps'][0][1])
        ls_of_time = len(speech_recognition_results['results'][i]['alternatives'][0]['timestamps']) - 1
        end_time = round(speech_recognition_results['results'][i]['alternatives'][0]['timestamps'][ls_of_time][2])
        transcript = speech_recognition_results['results'][i]['alternatives'][0]['transcript']

        print(json.dumps(speech_recognition_results, indent=2))

        with open('%s%s' % (text_path, text_name), 'a') as text:
            text.write("\n---------- %s to %s ----------%s\n" % (time_transfer(start_time), time_transfer(end_time), str(i+1)))
            text.write(transcript)

    with open('%s%s' % (text_path, text_name), 'a') as text:
        text.write("\n------------------end------------------\n")
    old_name = '%s%s' % (text_path, text_name)
    new_name = '%s%s.txt' % (text_path, audio_name)
    if os.path.exists(new_name):
        os.remove(new_name)
    os.renames(old_name, new_name)


def time_transfer(time):
    minutes = int(time/60)
    seconds = time % 60
    t = "%s m %s s" % (minutes, seconds)
    return t


if __name__ == '__main__':
    main()
