
import os
import google.generativeai as genai
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_gemini():
    """Initialize the Gemini API with the API key from environment variables."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.warning("GEMINI_API_KEY not found in environment variables")
        return False
    
    try:
        genai.configure(api_key=api_key)
        logger.info("Gemini API initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing Gemini API: {str(e)}")
        return False

def generate_analysis(text):
    """
    Generate enhanced sentiment analysis and homesickness assessment using Gemini.
    
    Args:
        text (str): User input text to analyze
        
    Returns:
        dict: Analysis results including sentiment score, homesickness level, and insights
    """
    if not initialize_gemini():
        logger.warning("Using fallback analysis due to Gemini API initialization failure")
        return None
    
    try:
        prompt = f"""
        Analyze the following text from an international student at UBC who may be experiencing homesickness.
        Provide a comprehensive analysis with the following components:
        
        1. Sentiment score (between -1.0 and 1.0, where -1 is very negative, 0 is neutral, and 1 is very positive)
        2. Homesickness level (between 1 and 10, where 1 is minimal and 10 is severe)
        3. Key emotional themes present in the text
        4. Specific cultural adjustment challenges identified
        5. Psychological resilience factors detected
        
        Format your response as a JSON object with these keys.
        
        Student text: "{text}"
        """
        
        # Configure the model
        generation_config = {
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config
        )
        
        response = model.generate_content(prompt)
        
        # Process the response into a structured format
        try:
            import json
            analysis_data = json.loads(response.text)
            return analysis_data
        except json.JSONDecodeError:
            # Fallback if response isn't proper JSON
            logger.warning("Could not parse Gemini response as JSON")
            
            # Attempt to extract key values from text
            lines = response.text.strip().split('\n')
            analysis_data = {}
            
            for line in lines:
                if "sentiment score" in line.lower():
                    try:
                        analysis_data["sentiment_score"] = float(line.split(":")[-1].strip())
                    except:
                        pass
                elif "homesickness level" in line.lower():
                    try:
                        analysis_data["homesickness_level"] = int(line.split(":")[-1].strip())
                    except:
                        pass
            
            return analysis_data
    
    except Exception as e:
        logger.error(f"Error generating analysis with Gemini: {str(e)}")
        return None

def generate_resilience_strategies(text, homesickness_level):
    """
    Generate personalized resilience strategies based on text content and homesickness level.
    
    Args:
        text (str): User's input text
        homesickness_level (int): Calculated homesickness level (1-10)
        
    Returns:
        list: List of strategy dictionaries with title, description, and steps
    """
    if not initialize_gemini():
        logger.warning("Using fallback strategies due to Gemini API initialization failure")
        return None
    
    try:
        prompt = f"""
        An international student at UBC has shared the following thoughts about their experience:
        
        "{text}"
        
        Their homesickness level has been assessed as {homesickness_level} out of 10.
        
        Generate 3 personalized resilience strategies to help them cope with homesickness and cultural adjustment.
        Each strategy should include:
        1. A title (concise and action-oriented)
        2. A brief description explaining the rationale and benefit
        3. 3-5 specific, actionable steps they can take to implement the strategy
        
        Format your response as a JSON array containing strategy objects with "title", "description", and "steps" keys.
        The "steps" should be an array of strings.
        
        Consider:
        - Neuroplasticity research showing gratitude practices increase dorsolateral prefrontal activity
        - Cultural context and social connection opportunities
        - Both immediate coping mechanisms and long-term resilience building
        - UBC-specific resources and Vancouver opportunities
        """
        
        # Configure the model
        generation_config = {
            "temperature": 0.7,  # More creative for strategies
            "top_p": 0.9,
            "top_k": 40,
            "max_output_tokens": 1024,
        }
        
        model = genai.GenerativeModel(
            model_name="gemini-1.0-pro",
            generation_config=generation_config
        )
        
        response = model.generate_content(prompt)
        
        # Process the response into a structured format
        try:
            import json
            strategies = json.loads(response.text)
            return strategies
        except json.JSONDecodeError:
            logger.warning("Could not parse Gemini response as JSON")
            # Return a simplified fallback
            return [
                {
                    "title": "Connect with UBC International Community",
                    "description": "Building social connections can significantly reduce homesickness.",
                    "steps": ["Join the International Student Association", "Attend cultural events on campus", "Create a study group with diverse students"]
                },
                {
                    "title": "Gratitude Journaling Practice",
                    "description": "Research shows gratitude increases prefrontal activity by 29%, creating emotional resilience.",
                    "steps": ["Write 3 things you appreciate daily", "Include both home memories and new experiences", "Review weekly to track your adjustment progress"]
                },
                {
                    "title": "Vancouver Cultural Immersion",
                    "description": "Creating positive experiences in your new environment builds new neural pathways.",
                    "steps": ["Visit a new Vancouver neighborhood weekly", "Try a local cuisine you've never experienced", "Document your discoveries in photos or writing"]
                }
            ]
            
    except Exception as e:
        logger.error(f"Error generating strategies with Gemini: {str(e)}")
        return None
