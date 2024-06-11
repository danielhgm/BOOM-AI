# nlp.py
import spacy

# Cargar el modelo de Spacy
try:
    nlp = spacy.load("en_core_web_sm")
    print("Spacy model loaded successfully.")
except Exception as e:
    print(f"Error loading Spacy model: {e}")
    raise

def parse_query(query):
    doc = nlp(query)
    intents = {'greeting': ['hello', 'hi', 'hey'], 'investment': ['invest', 'investment']}
    
    for token in doc:
        for intent, keywords in intents.items():
            if token.lemma_ in keywords:
                return intent
    return 'unknown'
