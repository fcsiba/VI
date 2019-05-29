# Voice Intelligence (VI):
An audio analytics tool that helps businesses make better decisions regarding customer support and marketing campaigns. The languages we currently support are Urdu and English.

## Installation Instructions
The following software is required in order to install and run Voice Intelligence:
- Python 3.7
- MySQL Server
- Windows 10

The following Python dependencies will need to be installed before executing code:
- Flask
- TextBlob
- SpeechRecognition
- Googletrans
- NLTK
- MySQL

You can install a Python dependency by using the following command in Command Line Prompt:
> pip install dependency-name

After the dependencies have been installed, you will need to follow these steps to complete installation:
1. Extract the webapp folder in a directory on your system such as D:\Voice Intelligence\.
2. Open cmd and type the commmand: ```cd D:\Voice Intelligence\```.
3. Type the command: ```set FLASK_APP=main.py```.
4. Type the command: ```flask run```.
5. Open your browser and visit the URL: http://127.0.0.1:5000/demo.

