import os
os.system('python3 setup.py install')
os.system('python3 -m spacy download en')
os.system(
    'python3 -c "import nltk; nltk.download(\'punkt\'); nltk.download(\'averaged_perceptron_tagger\'); nltk.download(\'stopwords\')"'
)
os.system('gunicorn -w 4 --bind 0.0.0.0:5000 wsgi')
