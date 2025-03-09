import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from collections import Counter

# Ensure required NLTK data is downloaded
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')

# Initialize lemmatizer and stop words
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Keywords related to homesickness and adaptation
homesickness_keywords = [
    'home', 'miss', 'family', 'friend', 'lonely', 'alone', 'culture', 'different',
    'strange', 'food', 'language', 'weather', 'adapt', 'adjust', 'struggle',
    'lost', 'confused', 'isolation', 'far', 'distance', 'custom', 'tradition',
    'unfamiliar', 'belong', 'comfort', 'routine', 'nostalgia'
]

# Emotion words for sentiment analysis
positive_words = [
    'happy', 'good', 'great', 'excellent', 'better', 'improvement', 'enjoy',
    'hope', 'positive', 'progress', 'excited', 'comfortable', 'confident',
    'grateful', 'thankful', 'opportunity', 'friend', 'connection', 'learn',
    'grow', 'adapt', 'overcome', 'success', 'achieve', 'manage', 'cope'
]

negative_words = [
    'sad', 'bad', 'terrible', 'worse', 'difficult', 'hard', 'struggle',
    'lonely', 'alone', 'homesick', 'miss', 'upset', 'anxious', 'worry',
    'stressed', 'confused', 'lost', 'frustrated', 'overwhelmed', 'tired',
    'exhausted', 'depressed', 'disconnected', 'isolated', 'afraid', 'scared'
]

def preprocess_text(text):
    """Preprocess text for analysis"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and digits
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\d+', ' ', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stop words and lemmatize
    filtered_tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    return filtered_tokens

def extract_keywords(tokens):
    """Extract relevant keywords from the processed text"""
    # Count word frequencies
    word_freq = Counter(tokens)
    
    # Get the most common words (excluding very short words)
    common_words = [word for word, count in word_freq.most_common(15) if len(word) > 2]
    
    # Check for homesickness-related words
    homesickness_related = [word for word in tokens if word in homesickness_keywords]
    
    # Combine and remove duplicates
    all_keywords = list(set(common_words + homesickness_related))
    
    return all_keywords[:10]  # Return top 10 keywords

def calculate_sentiment(tokens):
    """Calculate sentiment score based on positive and negative words"""
    positive_count = sum(1 for word in tokens if word in positive_words)
    negative_count = sum(1 for word in tokens if word in negative_words)
    
    total_count = positive_count + negative_count
    
    if total_count == 0:
        return 0  # Neutral
    
    return (positive_count - negative_count) / total_count  # Range: -1 to 1

def identify_themes(text):
    """Identify themes in the text"""
    themes = []
    
    # Academic challenges
    academic_words = ['class', 'course', 'study', 'professor', 'grade', 'exam', 'assignment', 'lecture']
    if any(word in text.lower() for word in academic_words):
        themes.append('Academic Challenges')
    
    # Social isolation
    social_words = ['friend', 'lonely', 'alone', 'social', 'party', 'talk', 'connection', 'relationship']
    if any(word in text.lower() for word in social_words):
        themes.append('Social Isolation')
    
    # Cultural adjustment
    cultural_words = ['culture', 'different', 'food', 'tradition', 'custom', 'language', 'adapt', 'adjust']
    if any(word in text.lower() for word in cultural_words):
        themes.append('Cultural Adjustment')
    
    # Family separation
    family_words = ['family', 'parent', 'mom', 'dad', 'mother', 'father', 'sibling', 'brother', 'sister', 'home']
    if any(word in text.lower() for word in family_words):
        themes.append('Family Separation')
    
    # Identity issues
    identity_words = ['identity', 'belong', 'fit', 'who', 'myself', 'change', 'same', 'different']
    if any(word in text.lower() for word in identity_words):
        themes.append('Identity Issues')
    
    return themes

def analyze_text(text):
    """Analyze text to identify themes, emotions, and keywords"""
    # Preprocess the text
    tokens = preprocess_text(text)
    
    # Extract keywords
    keywords = extract_keywords(tokens)
    
    # Calculate sentiment
    sentiment_score = calculate_sentiment(tokens)
    
    # Identify themes
    themes = identify_themes(text)
    
    # Determine the emotional state
    if sentiment_score > 0.3:
        emotional_state = "Positive"
    elif sentiment_score < -0.3:
        emotional_state = "Negative"
    else:
        emotional_state = "Neutral"
    
    # Prepare the analysis result
    analysis = {
        'keywords': keywords,
        'sentiment_score': sentiment_score,
        'emotional_state': emotional_state,
        'themes': themes,
        'text_length': len(text)
    }
    
    return analysis
