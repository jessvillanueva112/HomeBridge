import random

# Dictionary of resilience strategies organized by theme
RESILIENCE_STRATEGIES = {
    'Academic Challenges': [
        {
            'title': 'Study Group Formation',
            'description': 'Form a study group with classmates from different backgrounds. This will help you understand material from different perspectives while building social connections.'
        },
        {
            'title': 'Academic Support Services',
            'description': 'Visit UBC\'s academic support services for tutoring and learning strategies. They offer specialized support for international students.'
        },
        {
            'title': 'Professor Office Hours',
            'description': 'Regularly attend office hours to build a relationship with your professors and seek clarification on challenging concepts.'
        },
        {
            'title': 'Time Management Workshop',
            'description': 'Attend a time management workshop through UBC Student Services to develop strategies for balancing coursework and personal time.'
        }
    ],
    'Social Isolation': [
        {
            'title': 'International Student Club',
            'description': 'Join UBC\'s International Student Association or a club related to your interests to meet people with similar experiences and backgrounds.'
        },
        {
            'title': 'Language Exchange Program',
            'description': 'Participate in a language exchange program to improve your English skills while helping others learn your native language.'
        },
        {
            'title': 'Community Volunteering',
            'description': 'Volunteer for community events or organizations to meet locals and gain a sense of belonging in Vancouver.'
        },
        {
            'title': 'Residence Activities',
            'description': 'Attend activities organized by your residence or housing community to meet neighbors and build local friendships.'
        }
    ],
    'Cultural Adjustment': [
        {
            'title': 'Cultural Transition Workshop',
            'description': 'Attend a cultural transition workshop offered by UBC International Student Development to learn coping strategies for culture shock.'
        },
        {
            'title': 'Local Cuisine Exploration',
            'description': 'Try one new local restaurant each week, while also finding places that serve familiar foods from your home country when needed.'
        },
        {
            'title': 'Cultural Celebration Events',
            'description': 'Participate in cultural celebrations at UBC to share your culture and learn about others through festivals, food, and traditions.'
        },
        {
            'title': 'Vancouver Neighborhood Tour',
            'description': 'Take guided tours of different Vancouver neighborhoods to better understand the local culture and find places where you feel comfortable.'
        }
    ],
    'Family Separation': [
        {
            'title': 'Regular Communication Schedule',
            'description': 'Establish a regular schedule for video calls with family and friends from home, accounting for time zone differences.'
        },
        {
            'title': 'Digital Family Dinner',
            'description': 'Organize a monthly digital family dinner where you and your family prepare and eat meals together over video call.'
        },
        {
            'title': 'Memory Box Creation',
            'description': 'Create a physical or digital collection of photos, messages, and mementos from home to look at when feeling homesick.'
        },
        {
            'title': 'Local Family Connection',
            'description': 'Connect with a local host family through UBC\'s Host Family Program to experience family dynamics in your new country.'
        }
    ],
    'Identity Issues': [
        {
            'title': 'Identity Reflection Journal',
            'description': 'Keep a journal to reflect on how your identity is evolving and the positive aspects of integrating different cultural elements.'
        },
        {
            'title': 'Cultural Identity Workshop',
            'description': 'Attend a workshop on cultural identity development offered by UBC Counseling Services to understand your transition process.'
        },
        {
            'title': 'Multicultural Friendship Circle',
            'description': 'Form a friendship circle with other international students to discuss identity challenges and share coping strategies.'
        },
        {
            'title': 'Personal Values Clarification',
            'description': 'Complete a values clarification exercise to identify which aspects of your home and new culture align with your personal values.'
        }
    ],
    'General Wellbeing': [
        {
            'title': 'Daily Gratitude Practice',
            'description': 'Write down three things you appreciate about your new environment each day to shift focus toward positive aspects.'
        },
        {
            'title': 'Mindfulness Meditation',
            'description': 'Practice mindfulness meditation for 10 minutes daily using the MindShift app (developed specifically for students) to reduce stress.'
        },
        {
            'title': 'Nature Connection Routine',
            'description': 'Spend time in Vancouver\'s beautiful natural settings like Pacific Spirit Park or the beaches - nature exposure is proven to reduce homesickness.'
        },
        {
            'title': 'Physical Activity Plan',
            'description': 'Develop a regular physical activity routine using UBC\'s recreation facilities to improve mood and energy levels.'
        },
        {
            'title': 'Sleep Hygiene Improvement',
            'description': 'Establish a consistent sleep schedule and bedtime routine to improve sleep quality, which directly impacts emotional resilience.'
        }
    ]
}

def get_resilience_strategies(analysis):
    """Generate resilience strategies based on text analysis"""
    strategies = []
    
    # Add strategies based on identified themes
    for theme in analysis.get('themes', []):
        if theme in RESILIENCE_STRATEGIES:
            # Add 1-2 strategies for each identified theme
            theme_strategies = random.sample(RESILIENCE_STRATEGIES[theme], min(2, len(RESILIENCE_STRATEGIES[theme])))
            strategies.extend(theme_strategies)
    
    # Always include at least 2 general wellbeing strategies
    general_strategies = random.sample(RESILIENCE_STRATEGIES['General Wellbeing'], min(2, len(RESILIENCE_STRATEGIES['General Wellbeing'])))
    strategies.extend(general_strategies)
    
    # Adjust strategy selection based on sentiment
    sentiment_score = analysis.get('sentiment_score', 0)
    
    if sentiment_score < -0.5:  # Very negative
        # Add more supportive strategies
        if 'Social Isolation' not in analysis.get('themes', []):
            social_strategy = random.choice(RESILIENCE_STRATEGIES['Social Isolation'])
            strategies.append(social_strategy)
    
    # Ensure we don't have too many strategies (max 5)
    if len(strategies) > 5:
        strategies = random.sample(strategies, 5)
    
    return strategies
