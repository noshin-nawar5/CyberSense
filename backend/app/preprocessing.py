"""
Text Preprocessing Module for CyberSense
Handles text cleaning, normalization, tokenization, and lemmatization
"""

import re
from typing import List, Optional
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Try to import NLTK components (graceful fallback if not available)
try:
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tokenize import TreebankWordTokenizer
    import nltk
    
    # Download required NLTK data if not present
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    try:
        nltk.data.find('corpora/wordnet')
    except LookupError:
        nltk.download('wordnet', quiet=True)
    
    try:
        nltk.data.find('corpora/omw-1.4')
    except LookupError:
        nltk.download('omw-1.4', quiet=True)
    
    NLTK_AVAILABLE = True
    
except ImportError:
    logger.warning("NLTK not available. Using basic preprocessing.")
    NLTK_AVAILABLE = False

# Initialize NLTK components if available
if NLTK_AVAILABLE:
    wnl = WordNetLemmatizer()
    tokenizer = TreebankWordTokenizer()
    base_stop = set(stopwords.words('english'))
else:
    wnl = None
    tokenizer = None
    base_stop = set()

# Custom stop words
custom_stop_extra = {
    'rt', 'amp', 'u', 'im', 'mkr', 'dont', 'like', 'one', 'get', 'know',
    'think', 'people', 'us', 'also', 'school', 'time'
}

# Short meaningful tokens to keep
allow_short = {'no', 'ok', 'ah'}

# Contraction normalizations
contraction_map = {
    r"\bim\b": "i am",
    r"\bur\b": "you are",
    r"\bu\b": "you",
    r"\bdont\b": "do not",
    r"\bdoesnt\b": "does not",
    r"\bdidnt\b": "did not",
    r"\bive\b": "i have",
    r"\bshes\b": "she is",
    r"\bhe's\b": "he is",
    r"\bthats\b": "that is",
    r"\bwont\b": "will not",
    r"\bcant\b": "can not",
    r"\bwouldnt\b": "would not",
    r"\bshouldnt\b": "should not"
}

# Regex patterns
URL_RE = re.compile(r"http\S+|www\.\S+")
MENTION_RE = re.compile(r"@\w+")
HASHTAG_RE = re.compile(r"#\w+")
HTML_ENTITY_RE = re.compile(r"&\w+;|&amp;")
NON_ALPHANUM_RE = re.compile(r"[^a-zA-Z0-9\s]")
REPEAT_CHAR_RE = re.compile(r"(.)\1{2,}")
WHITESPACE_RE = re.compile(r"\s+")

def clean_text_basic(text: str) -> str:
    """
    Basic text cleaning without NLTK dependencies
    
    Args:
        text: Input text string
        
    Returns:
        Cleaned text string
    """
    if not isinstance(text, str):
        text = str(text)
    
    # Lowercase
    txt = text.lower()
    
    # Remove URLs
    txt = URL_RE.sub(" ", txt)
    
    # Remove mentions
    txt = MENTION_RE.sub(" ", txt)
    
    # Remove hashtags (keep the text, remove the #)
    txt = HASHTAG_RE.sub(lambda m: m.group(0)[1:], txt)
    
    # Remove HTML entities
    txt = HTML_ENTITY_RE.sub(" ", txt)
    
    # Normalize contractions
    for pattern, replacement in contraction_map.items():
        txt = re.sub(pattern, replacement, txt)
    
    # Remove punctuation
    txt = NON_ALPHANUM_RE.sub(" ", txt)
    
    # Collapse repeated characters
    txt = REPEAT_CHAR_RE.sub(r"\1\1", txt)
    
    # Normalize whitespace
    txt = WHITESPACE_RE.sub(" ", txt).strip()
    
    return txt

def clean_text_advanced(text: str) -> str:
    """
    Advanced text cleaning with NLTK (tokenization, lemmatization, stopword removal)
    
    Args:
        text: Input text string
        
    Returns:
        Cleaned and processed text string
    """
    if not NLTK_AVAILABLE:
        logger.warning("NLTK not available. Falling back to basic cleaning.")
        return clean_text_basic(text)
    
    if not isinstance(text, str):
        text = str(text)
    
    # Basic cleaning first
    txt = text.lower()
    txt = URL_RE.sub(" ", txt)
    txt = MENTION_RE.sub(" ", txt)
    txt = HTML_ENTITY_RE.sub(" ", txt)
    
    # Normalize contractions
    for pattern, replacement in contraction_map.items():
        txt = re.sub(pattern, replacement, txt)
    
    # Remove punctuation
    txt = NON_ALPHANUM_RE.sub(" ", txt)
    
    # Collapse repeated characters
    txt = REPEAT_CHAR_RE.sub(r"\1\1", txt)
    
    # Tokenization
    tokens = tokenizer.tokenize(txt)
    
    # Filter and lemmatize tokens
    clean_tokens = []
    for token in tokens:
        # Skip digits
        if token.isdigit():
            continue
        
        # Skip short tokens unless allowed
        if len(token) <= 2 and token not in allow_short:
            continue
        
        # Skip custom stopwords
        if token in custom_stop_extra:
            continue
        
        # Skip standard stopwords
        if token in base_stop:
            continue
        
        # Lemmatize
        lemma = wnl.lemmatize(token, pos='v')  # Verb form
        lemma = wnl.lemmatize(lemma, pos='n')  # Noun form
        
        # Final length check
        if len(lemma) <= 1:
            continue
        
        clean_tokens.append(lemma)
    
    return " ".join(clean_tokens)

def clean_text(text: str, mode: str = 'advanced') -> str:
    """
    Main text cleaning function with mode selection
    
    Args:
        text: Input text string
        mode: 'basic' or 'advanced' (default: 'advanced')
        
    Returns:
        Cleaned text string
    """
    try:
        if mode == 'basic':
            return clean_text_basic(text)
        else:
            return clean_text_advanced(text)
    except Exception as e:
        logger.error(f"Error cleaning text: {str(e)}")
        # Fallback to basic cleaning
        return clean_text_basic(text)

def batch_clean_texts(texts: List[str], mode: str = 'advanced') -> List[str]:
    """
    Clean multiple texts at once
    
    Args:
        texts: List of text strings
        mode: 'basic' or 'advanced'
        
    Returns:
        List of cleaned text strings
    """
    return [clean_text(text, mode) for text in texts]

# For backward compatibility with existing code
def clean_text_improved(text: str) -> str:
    """
    Alias for clean_text with advanced mode
    For compatibility with text_preprocessing.py
    """
    return clean_text(text, mode='advanced')

if __name__ == "__main__":
    # Test the preprocessing
    test_texts = [
        "RT @user: This is a test http://example.com #test",
        "I dont like this!!! It's sooooo annoying...",
        "you're stupid and ugly",
        "@user ur an idiot lol"
    ]
    
    print("Testing text preprocessing:\n")
    for text in test_texts:
        cleaned = clean_text(text)
        print(f"Original: {text}")
        print(f"Cleaned:  {cleaned}")
        print()
