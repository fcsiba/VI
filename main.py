import speech_recognition as sr
from os import path
from textblob import TextBlob
import string
from googletrans import Translator
import mysql.connector
# from py_translator import Translator
# from py_translator import TEXTLIB

db = mysql.connector.connect(
  host="localhost",
  user="xxxx",
  passwd="xxxx"
)

audio = path.join(path.dirname(path.realpath(__file__)), "myaudio.wav")

STOP_WORDS = frozenset("""
 آ آئی آئیں آئے آتا آتی آتے آس آنا آنی آنے آپ آیا ابھی از اس اسی اسے البتہ
 الف ان انہوں انہی انہیں اور اپ اپنا اپنی اپنے اکثر اگر اگرچہ ایسا ایسی ایسے ایک اے بار بارے
 باوجود باہر بعض بغیر بلکہ بن بنا بناؤ بند بڑی بھر بھریں بھی بیس بے تا تاکہ تب تجھ
 تجھے تحت تر تم تمہارا تمہاری تمہارے تمہیں تو تک تھا تھی تھیں تھے تیری جا جاؤ جائیں جائے جاتا
 جاتی جاتے جانی جانے جب جبکہ جس جن جنہوں جنہیں جو جہاں جیسا جیسوں جیسی جیسے حالانکہ حالاں حصہ خالی
 خود درمیان دوران دوسرا دوسروں دوسری دوسرے دوں دکھائیں دی دیئے دیا دیتا دیتی دیتے دیر دینا دینی دینے
 دیکھو دیں دیے دے ذریعے رکھا رکھتا رکھتی رکھتے رکھنا رکھنی رکھنے رکھو رکھی رکھے رہ رہا رہتا رہتی رہتے
 رہنا رہنی رہنے رہو رہی رہیں رہے سا ساتھ سامنے سب سو سکا سکتا سکتے سی سے شاید صرف طرح
 طرف طور علاوہ عین لئے لا لائی لائے لاتا لاتی لاتے لانا لانی لانے لایا لو لوجی لوگ لوگوں لگ
 لگا لگتا لگتی لگی لگیں لگے لہذا لی لیا لیتا لیتی لیتے لیکن لیں لیے لے مجھ مجھے مزید مطابق
 مل مگر میرا میری میرے میں نا نہ نہیں نے وار واقعی والا والوں والی والے
 وجہ وغیرہ وہ وہاں وہی وہیں وی ویسے پایا پر پھر پیچھے چاہئے چاہتے چاہیئے چاہے چلا چلو چلیں چلے
 چونکہ چکی چکیں چکے ڈالنی ڈالنے ڈالے کئے کا کب کبھی کر کرتا کرتی کرتے کرنا کرنے کرو کریں کرے
 کس کسی کسے کم کو کوئی کون کونسا کچھ کہ کہا کہاں کہہ کہی کہیں کہے کی کیا کیسے کیونکہ
 کیوں کیے کے گئی گئے گا گویا گی گیا گے ہاں ہر ہم ہمارا ہماری ہمارے ہو ہوئی ہوئیں ہوئے
 ہوا ہوتا ہوتی ہوتیں ہوتے ہونا ہونگے ہونی ہونے ہوں ہی ہیں ہے یا یات یعنی یہ یہاں یہی یہیں
""".split())

def analyze(polarity):
   if (polarity > 0.5):
      return "Positive"
   elif (polarity < -0.5):
      return "Negative"
   else:
      return "Neutral"

r = sr.Recognizer()

with sr.AudioFile(audio) as source:
	audio = r.record(source)

try:
   sentence = r.recognize_google(audio, language = 'ur-PK')
   print("Audio Says: " + sentence)
except sr.UnknownValueError:
    print("We could not understand the accent or speed. Please try again.")
except sr.RequestError as e:
    print("We could not retrieve the service.") 

cleaned_sentence = ""
for x in sentence.split():
	if x not in STOP_WORDS:
		cleaned_sentence = cleaned_sentence + x + " "

print(cleaned_sentence)

conversion_dictionary = {}
positive_words = []
with open("Positive Words.txt", "r", encoding = 'utf-8') as pos_words:
	lines = pos_words.readlines()
	for line in lines:
		count = line.count(':')
		if (count == 2):
			english, roman, pos = line.split(':')
			positive_words.append(roman.replace('\n', '').strip())


with open("English Urdu Roman.txt", "r", encoding = 'utf-8') as conversions:
	lines = conversions.readlines()
	for line in lines:
		count = line.count(':')
		if (count == 2):
			english, urdu, roman = line.split(':')
			conversion_dictionary[roman.replace('\n', '').strip()] = urdu.replace('\n', '').strip()

urdu_positive_words = []
words_to_convert = []
for x in positive_words:
	if (x in conversion_dictionary):
		urdu_positive_words.append(conversion_dictionary[x])
	else:
		words_to_convert.append(x)

negative_words = []

positive_score = 0
negative_score = 0
length_of_call = len(cleaned_sentence.split())

for x in cleaned_sentence.split():
	if x in positive_words:
		positive_score += 1
	elif x in negative_words:
		negative_score += 1

polarity_score = (positive_score - negative_score)/length_of_call

subjectivity = 0
call_subjects = []

keywords = ['خراب']

for x in cleaned_sentence.split():
	if x in keywords:
		subjectivity += 1
		call_subjects.append(x)

subjectivity = subjectivity/length_of_call

print(positive_score)
print(subjectivity)

translator = Translator()
translations = translator.translate(words_to_convert, dest = 'urdu')
for x in translations:
	urdu_positive_words.append(x.text)

# for x in words_to_convert:
# 	s = Translator().translate(text= x, dest='urdu')
# 	urdu_positive_words.append(s.text)

urdu_positive_words = list(set(urdu_positive_words))

with open('Urdu Positive Words.txt', 'w', encoding = 'w+') as output:
	for x in urdu_positive_words:
		output.write(x)

dbcursor = db.cursor()

query = "INSERT INTO calls (call_text, polarity, sentiment, subjectivity, subjects) VALUES (%s, %s, %s, %s, %s)"
values = (cleaned_sentence, polarity, subjectivity, call_subjects)

dbcursor.execute(query, values)

db.commit()
