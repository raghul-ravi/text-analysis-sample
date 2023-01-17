from flask import Flask, request, jsonify
from spellchecker import SpellChecker
import spacy

app = Flask(__name__)

text = "Spacy is a powerful library for natural language processing in Python. Spacy is also a good tool for text classification and named entity recognition"

spell = SpellChecker()
nlp = spacy.load("en_core_web_sm")

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()
    search_strings = data["search_strings"]
    doc = nlp(text)
    entities = [(ent.text,ent.label_) for ent in doc.ents]
    results = []
    for search_string in search_strings:
        corrected_search_string = spell.correction(search_string)
        count = text.count(corrected_search_string)
        original_count = text.count(search_string)
        start = 0
        indexes = []
        while True:
            start = text.find(corrected_search_string, start)
            if start == -1:
                break
            end = start + len(corrected_search_string)
            indexes.append((start, end))
            start += 1
        if corrected_search_string != search_string:
            results.append({'original': search_string, 'corrected': corrected_search_string, 'count': count if count > 0 else original_count,'indexes':indexes})
        elif count > 0:
            results.append({'original': search_string, 'corrected': corrected_search_string, 'count': count,'indexes':indexes})
        elif original_count > 0:
            results.append({'original': search_string, 'corrected': corrected_search_string, 'count': original_count,'indexes':indexes})
        else:
            results.append({'original': search_string, 'corrected': corrected_search_string, 'count': 0,'indexes':[]})
    results.append({'entities':entities})
    return jsonify(results)

if __name__ == '__main__':
        app.run(debug=True, host='0.0.0.0', port=1212)
