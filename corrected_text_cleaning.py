# Cleaning & normalization with PROPER Tokenization, Stemming & Lemmatization

import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import TreebankWordTokenizer

# Initialize - Added TreebankWordTokenizer for proper tokenization
wnl = WordNetLemmatizer()
ps = PorterStemmer()  # For stemming (optional - see below)
tokenizer = TreebankWordTokenizer()  # PROPER tokenizer instead of split()
base_stop = set(stopwords.words('english'))

# Custom extra stop tokens observed in your top words
custom_stop_extra = {
    'rt', 'amp', 'u', 'im', 'mkr', 'dont', 'like', 'one', 'get', 'know',
    'think', 'people', 'dont', 'us', 'also', 'school','time','get'
}

# Optionally keep some short meaningful tokens
allow_short = {'no','ok','ah'} 

# Contraction normalizations (basic)
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
    r"\bthats\b": "that is"
}

# regex patterns
URL_RE = re.compile(r"http\S+|www\.\S+")
MENTION_RE = re.compile(r"@\w+")
HTML_ENTITY_RE = re.compile(r"&\w+;|&amp;")
NON_ALPHANUM_RE = re.compile(r"[^a-zA-Z0-9\s]")
REPEAT_CHAR_RE = re.compile(r"(.)\1{2,}")  # reduce repeated chars

def clean_text_improved(text):
    """
    Clean text with proper TOKENIZATION, STEMMING, and LEMMATIZATION.
    
    Process:
    1. Lowercase and remove URLs, mentions, HTML entities
    2. Normalize contractions
    3. Remove punctuation and collapse repeated characters
    4. TOKENIZE using TreebankWordTokenizer (better than split())
    5. Remove stopwords, digits, short tokens
    6. LEMMATIZE (converts words to their base form - more accurate than stemming)
    
    Note: Currently using LEMMATIZATION only (more accurate).
    To use STEMMING instead, uncomment the stemming line and comment out lemmatization.
    """
    if not isinstance(text, str):
        text = str(text)
    txt = text.lower()
    # remove urls, mentions, html entities
    txt = URL_RE.sub(" ", txt)
    txt = MENTION_RE.sub(" ", txt)
    txt = HTML_ENTITY_RE.sub(" ", txt)
    # normalize common contractions/chat tokens
    for patt, repl in contraction_map.items():
        txt = re.sub(patt, repl, txt)
    # remove punctuation but keep spaces and alphanumerics
    txt = NON_ALPHANUM_RE.sub(" ", txt)
    # collapse repeated characters (loooove -> loove)
    txt = REPEAT_CHAR_RE.sub(r"\1\1", txt)
    
    # PROPER TOKENIZATION using TreebankWordTokenizer (NOT simple split!)
    toks = tokenizer.tokenize(txt)
    
    clean_toks = []
    for t in toks:
        # remove digits
        if t.isdigit():
            continue
        # remove tokens (<=2) unless in allow_short
        if len(t) <= 2 and t not in allow_short:
            continue
        # remove tokens in custom stoplist
        if t in custom_stop_extra:
            continue
        # remove stopwords
        if t in base_stop:
            continue
        
        # OPTION 1: STEMMING (faster, cruder) - Currently commented out
        # stemmed = ps.stem(t)
        # clean_toks.append(stemmed)
        
        # OPTION 2: LEMMATIZATION (slower, more accurate) - Currently ACTIVE
        # Apply verb lemmatization first, then noun
        lemma = wnl.lemmatize(t, pos='v')  # verb form first
        lemma = wnl.lemmatize(lemma, pos='n')  # then noun form
        
        # final length check
        if len(lemma) <= 1:
            continue
        clean_toks.append(lemma)
    
    return " ".join(clean_toks)

# Apply to dataframe
print('Starting text cleaning with proper tokenization and lemmatization...')
df['clean_text'] = df['text'].astype(str).map(clean_text_improved)
print(f'Cleaned {len(df)} texts successfully!')

# Quick check: top 10 cleaned examples
df[['text','clean_text']].head(10)
