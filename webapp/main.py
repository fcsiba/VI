from flask import Flask, url_for, render_template, request, jsonify
from werkzeug.utils import secure_filename
from textprocessor import SpeechRecognition as SR, UrduTextProcessor as UTP, Call, Database
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD']=True
app.config['DEBUG']=True

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
    	if request.form['urdutext'] != '':
    		text = request.form['urdutext']
    	elif request.files['audiofile'].filename != '':
	    	f = request.files['audiofile']
	    	text = SR.transcribeWithGoogle(f)
    	else:
	    	return jsonify({'error': 'NaN'})
    	polarity = UTP.analyzeSentiment(text)
    	sentiment = UTP.getSentimentLabel(polarity)
    	if (sentiment == 'Negative'):
    		calltype = 'Complaint'
    	elif(sentiment == 'Neutral'):
    		calltype = 'Query'
    	else:
    		calltype = 'Review'
    	keywords, subjectivity = UTP.findKeywords(text)
    	keywords = " ,".join(keywords)
    	if (keywords == ' ,'):
    		keywords = 'None'
    	#f.save('/files/' + secure_filename(f.filename))
    	subjects, density = UTP.findSubjects(text)
    	subjects = " ,".join(subjects)
    	if (subjects == ' ,'):
    		subjects = 'None'

    	record = Call('none', text, polarity, subjectivity, sentiment, keywords, subjects, density, calltype)
    	Database.addCall(record)
    	
    	returnvalues = {'text': text, 'sentiment': sentiment, 'calltype': calltype, 'keywords': keywords, 'callsubject': subjects, 'error': ''}
    	return jsonify(returnvalues)

@app.route("/visualizations")
def visualization(name = None): 
    sentimentlegend = 'Analysis by Sentiments'
    sentimentlabels = ["Positive", "Negative", "Neutral"]
    positivecalls = Database.runQuery("SELECT COUNT(*) AS cnt from calls where sentiment = 'Positive'")
    negativecalls = Database.runQuery("SELECT Count(*) AS cnt from calls where sentiment = 'Negative'")
    neutralcalls = Database.runQuery("SELECT Count(*) AS cnt from calls where sentiment = 'Neutral'")
    sentimentvalues = [positivecalls[0]['cnt'], negativecalls[0]['cnt'], neutralcalls[0]['cnt']]
    typelegend = 'Analysis by Sentiments'
    typelabels = ["Review", "Complaint", "Query"]
    reviews = Database.runQuery("SELECT COUNT(*) AS cnt from calls where calltype = 'Review'")
    complaints = Database.runQuery("SELECT Count(*) AS cnt from calls where calltype = 'Complaint'")
    queries = Database.runQuery("SELECT Count(*) AS cnt from calls where calltype = 'Query'")
    typevalues = [reviews[0]['cnt'], complaints[0]['cnt'], queries[0]['cnt']]
    subjectandsentiments = Database.runQuery("SELECT subjects, sentiment, COUNT(*) AS cnt FROM calls GROUP BY subjects, sentiment")
    subandsen = {}
    for x in subjectandsentiments:
        if x['subjects'] not in subandsen:
            subandsen[x['subjects']] = [("Positive", 0), ("Negative", 0), ("Neutral", 0)]
        if x['sentiment'] == 'Positive':
            subandsen[x['subjects']][0] = ("Positive", x['cnt'])
        elif x['sentiment'] == 'Negative':
            subandsen[x['subjects']][1] = ("Negative", x['cnt'])
        else:
            subandsen[x['subjects']][2] = ("Neutral", x['cnt'])
    return render_template('visualizations.html', name=name, typelegend = typelegend, typelabels = typelabels, typevalues = typevalues, sentimentvalues = sentimentvalues, sentimentlabels = sentimentlabels, sentimentlegend = sentimentlegend, subandsen = subandsen)
