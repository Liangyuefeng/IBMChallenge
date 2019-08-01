# IBM Challenge 5 - Interactive Story Telling
## What is all this about?
A simple vocal interating game for sight impaired people. Load a interactive story in pre-defined format and enjoying the fully automatic story telling.

There can be player choices inside stories, making endings differ based on the choices made.

This is a part of IBM AI Challenge 2019 in the University of Liverpool.

Text to Speech and Speech to Text services are based on IBM Watson AI platform.
## How to use?
* Python 3.7.3. + `ibm_watson`, `flask` and `python_datauri` library.
* A browser supporting HTML5 audio recording and playing. Some working browser showed below.
  * Microsoft Edge
  * WebKit family
  * Firefox
  * ~~Internet Explorer 11~~
* A HTTP server. The code cannot be ran by itself from version 1.1.0. A HTTP server with WSGI is intended. Tons of tutorials online to help you do this.
  * IIS (tested and currently based on)
    * On IIS make sure you configured the number of instances correctly for better performance.
	* Spaces within path (such as `Program Files`) will mess the configuration up, stay frosty.
  * Nginx
  * Apache
  * ...
* Place a JSON file named `keys.json` contains IBM Watson API key in the given format with `dynamic.py`. Sample file can be found in files. You need 2 keys for both TTS and STT.
  * Get an IBM account at [https://www.ibm.com/watson](https://www.ibm.com/watson)
  * You may want to mask the file from your HTTP server.
## Who did this?
A bunch of students from the University of Liverpool, participating IBM AI Challenge 2019.

We are **the Team Diesel Engine**.

**Captain:** Miguel Li

**Coding:** Cheng Bi (Speech to Text), Chaoyi Han (UI & Game Logic), Yuefeng Liang (Text to Speech)

**Story Design:** Miguel Li, Linwei Yang, Yukun Zhou

**Team Management:** Miguel Li, Linwei Yang, Yukun Zhou
## Libraries Used
* [jQuery 3.4.1](https://jquery.com)
* [jQuery EasyUI 1.8.1](https://jeasyui.com)