from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string
import spacy

# Load SpaCy's English model
nlp = spacy.load("en_core_web_sm")

def preprocess_text(text):
    """
    Tokenize and normalize text (e.g., actor roles, use case names).
    """
    # Tokenize and lowercase
    tokens = word_tokenize(text.lower())
    # Remove stopwords and punctuation
    tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]
    return tokens