import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from collections import Counter
import random
import logging

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
except Exception as e:
    logging.error(f"Error downloading NLTK data: {str(e)}")

# Define common homesickness themes and keywords
HOMESICKNESS_THEMES = {
    'family': ['family', 'mom', 'dad', 'parents', 'siblings', 'sister', 'brother', 'relatives', 'home'],
    'food': ['food', 'cuisine', 'dish', 'meal', 'restaurant', 'cook', 'cooking', 'taste', 'flavor'],
    'culture': ['culture', 'tradition', 'customs', 'language', 'cultural', 'celebration', 'festival', 'holiday'],
    'social': ['friends', 'social', 'lonely', 'loneliness', 'isolation', 'connect', 'relationships', 'belong'],
    'academics': ['study', 'school', 'class', 'professor', 'assignment', 'exam', 'grade', 'academic', 'university'],
    'environment': ['weather', 'climate', 'environment', 'landscape', 'nature', 'city', 'place', 'neighborhood'],
    'identity': ['identity', 'self', 'who I am', 'belong', 'fit in', 'different', 'foreigner', 'international']
}

# Define resilience strategies for each theme
RESILIENCE_STRATEGIES = {
    'family': [
        {
            'name': 'Virtual Family Time',
            'description': 'Schedule regular video calls with family members to maintain connection. Create a routine that works across time zones.'
        },
        {
            'name': 'Family Photo Journal',
            'description': 'Create a digital or physical album of family photos and memories. Add to it regularly and look at it when feeling homesick.'
        },
        {
            'name': 'Care Package Exchange',
            'description': 'Exchange care packages with family that include small items that remind you of home.'
        }
    ],
    'food': [
        {
            'name': 'Cook Cultural Dishes',
            'description': 'Learn to cook your favorite dishes from home. Invite new friends to share these meals and cultural experiences.'
        },
        {
            'name': 'Find Authentic Restaurants',
            'description': 'Research and visit restaurants in Vancouver that serve authentic food from your culture.'
        },
        {
            'name': 'Food Exchange Club',
            'description': 'Create or join a food exchange club where international students share dishes from their home countries.'
        }
    ],
    'culture': [
        {
            'name': 'Cultural Events Calendar',
            'description': 'Create a calendar of cultural celebrations and find ways to celebrate them in your new home.'
        },
        {
            'name': 'Join Cultural Associations',
            'description': 'Connect with cultural or country-specific associations at UBC or in Vancouver.'
        },
        {
            'name': 'Share Your Culture',
            'description': 'Organize events to share aspects of your culture with new friends and classmates.'
        }
    ],
    'social': [
        {
            'name': 'UBC Club Participation',
            'description': 'Join clubs or organizations at UBC that align with your interests to meet like-minded people.'
        },
        {
            'name': 'Volunteer Work',
            'description': 'Participate in volunteer activities to meet people and feel connected to your new community.'
        },
        {
            'name': 'Friendship Building Activities',
            'description': 'Attend social events specifically designed for international students to make new friends.'
        }
    ],
    'academics': [
        {
            'name': 'Study Group Formation',
            'description': 'Form or join study groups to connect with classmates and improve academic performance.'
        },
        {
            'name': 'Use University Resources',
            'description': 'Take advantage of academic support services like tutoring, writing centers, and academic advisors.'
        },
        {
            'name': 'Academic Goal Setting',
            'description': 'Set clear, achievable academic goals and celebrate your progress to build confidence.'
        }
    ],
    'environment': [
        {
            'name': 'Explore Vancouver',
            'description': 'Take time to explore and appreciate the natural beauty and unique aspects of Vancouver.'
        },
        {
            'name': 'Create Comfortable Space',
            'description': 'Make your living space comfortable and personal with items that make you feel at home.'
        },
        {
            'name': 'Nature Connection',
            'description': 'Spend time in nature to reduce stress and build connection to your new environment.'
        }
    ],
    'identity': [
        {
            'name': 'Identity Journaling',
            'description': 'Keep a journal about your experience and how your identity is growing and changing.'
        },
        {
            'name': 'Find Cultural Mentors',
            'description': 'Connect with senior students from your culture who have successfully navigated the transition.'
        },
        {
            'name': 'Integrate New and Old',
            'description': 'Find ways to integrate aspects of your home culture with your new experiences in Canada.'
        }
    ],
    'general': [
        {
            'name': 'Daily Gratitude Practice',
            'description': 'Take a few minutes each day to write down three things you are grateful for in your new environment.'
        },
        {
            'name': 'Mindfulness Meditation',
            'description': 'Practice mindfulness meditation to stay grounded and present during difficult moments.'
        },
        {
            'name': 'Physical Exercise Routine',
            'description': 'Establish a regular exercise routine to boost mood and build physical resilience.'
        }
    ]
}

def analyze_text(text):
    """
    Analyze the text to identify sentiment and key themes related to homesickness.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Analysis results including sentiment score and identified themes
    """
    try:
        # Initialize sentiment analyzer
        sia = SentimentIntensityAnalyzer()
        
        # Analyze sentiment
        sentiment = sia.polarity_scores(text)
        
        # Tokenize text
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
        
        # Identify themes
        identified_themes = {}
        for theme, keywords in HOMESICKNESS_THEMES.items():
            theme_score = sum(1 for token in filtered_tokens if token in keywords)
            if theme_score > 0:
                identified_themes[theme] = theme_score
        
        # Get most frequent words for content understanding
        word_freq = Counter(filtered_tokens)
        most_common_words = word_freq.most_common(10)
        
        return {
            'sentiment_score': sentiment['compound'],
            'identified_themes': identified_themes,
            'most_common_words': most_common_words,
            'text_length': len(tokens)
        }
    
    except Exception as e:
        logging.error(f"Error analyzing text: {str(e)}")
        # Return basic analysis if there's an error
        return {
            'sentiment_score': 0,
            'identified_themes': {'general': 1},
            'error': str(e)
        }

def generate_strategies(analysis_results):
    """
    Generate personalized resilience strategies based on the text analysis.
    
    Args:
        analysis_results (dict): Results from text analysis
        
    Returns:
        list: List of strategy dictionaries
    """
    strategies = []
    
    try:
        # Get the identified themes
        identified_themes = analysis_results.get('identified_themes', {})
        
        # If no specific themes were identified, use general strategies
        if not identified_themes:
            identified_themes = {'general': 1}
        
        # Sort themes by relevance
        sorted_themes = sorted(identified_themes.items(), key=lambda x: x[1], reverse=True)
        
        # Select top 3 themes (or fewer if less than 3 were identified)
        top_themes = sorted_themes[:min(3, len(sorted_themes))]
        
        # Add a general theme if we have less than 3 themes
        if len(top_themes) < 3 and 'general' not in [t[0] for t in top_themes]:
            top_themes.append(('general', 0))
        
        # For each top theme, select a strategy
        for theme, _ in top_themes:
            theme_strategies = RESILIENCE_STRATEGIES.get(theme, RESILIENCE_STRATEGIES['general'])
            strategy = random.choice(theme_strategies)
            
            # Only add if not already included
            if strategy not in strategies:
                strategies.append(strategy)
        
        # If the sentiment is very negative, add a specific emotional support strategy
        sentiment_score = analysis_results.get('sentiment_score', 0)
        if sentiment_score < -0.5 and len(strategies) < 5:
            emotional_strategy = {
                'name': 'Emotional First Aid',
                'description': 'When feeling overwhelmed, try the 5-4-3-2-1 grounding technique: Acknowledge 5 things you see, 4 things you can touch, 3 things you hear, 2 things you smell, and 1 thing you taste.'
            }
            strategies.append(emotional_strategy)
        
        # Add general strategies if we have less than 3 total
        while len(strategies) < 3:
            general_strategy = random.choice(RESILIENCE_STRATEGIES['general'])
            if general_strategy not in strategies:
                strategies.append(general_strategy)
        
        return strategies
    
    except Exception as e:
        logging.error(f"Error generating strategies: {str(e)}")
        # Return basic strategies if there's an error
        return [
            {
                'name': 'Connect with Others',
                'description': 'Reach out to fellow students or join a club to build your social connections.'
            },
            {
                'name': 'Practice Self-Care',
                'description': 'Take time each day for activities that help you relax and recharge.'
            },
            {
                'name': 'Explore Your New Home',
                'description': 'Set aside time to explore Vancouver and discover what makes it special.'
            }
        ]
