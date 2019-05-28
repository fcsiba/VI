from flask import Flask, url_for, render_template, request, jsonify
from werkzeug.utils import secure_filename
from textprocessor import SpeechRecognition as SR, UrduTextProcessor as UTP, Call, Database
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index(name = None):
	return render_template('index.html', name=name)

@app.route("/demo")
def demo(name = None):
	return render_template('demo.html', name=name)
    
@app.route("/demo/upload", methods=['GET', 'POST'])
def uploadaudiofile():
    if request.method == 'POST':
    	f = request.files['audiofile']
    	text = SR.transcribeWithGoogle(f)
    	sentiment = UTP.getSentimentLabel(UTP.analyzeSentiment(text))
    	if (sentiment == 'Negative'):
    		calltype = 'Complaint'
    	elif(sentiment == 'Neutral'):
    		calltype = 'Query'
    	else:
    		calltype = 'Review'
    	keywords = " ,".join(UTP.findKeywords(text))
    	if (keywords == ' ,'):
    		keywords = ''
    	#f.save('/files/' + secure_filename(f.filename))
    	subjects = " ,".join(UTP.findSubjects(text))
    	if (subjects == ' ,'):
    		subjects = ''
    	returnvalues = {'text': text, 'sentiment': sentiment, 'calltype': calltype, 'keywords': keywords, 'callsubject': subjects}
    	return jsonify(returnvalues)
