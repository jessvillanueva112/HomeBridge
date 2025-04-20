import logging
from qualtrics_integration import QualtricsIntegration
from config import Config

# Configure logging
logging.basicConfig(
    level=Config.LOG_LEVEL,
    format=Config.LOG_FORMAT
)
logger = logging.getLogger(__name__)

def main():
    try:
        # Validate configuration
        Config.validate_config()
        
        # Initialize Qualtrics integration
        qualtrics = QualtricsIntegration()
        
        # Example: Sync data for a specific user
        user_id = "example_user_123"
        sync_report = qualtrics.sync_qualtrics_data(user_id)
        
        # Print the sync report
        logger.info("Sync Report:")
        logger.info(f"Average Sentiment: {sync_report['average_sentiment']:.2f}")
        logger.info(f"Volatility: {sync_report['volatility']:.2f}")
        
        if sync_report['significant_changes']:
            logger.info("Significant Sentiment Changes:")
            for change in sync_report['significant_changes']:
                logger.info(f"Date: {change['date']}, Change: {change['change']:.2f}")
        
        # Example: Analyze sentiment for a specific text
        text = "I'm feeling really overwhelmed with my studies and missing home."
        sentiment_result = qualtrics.analyze_sentiment(text)
        logger.info(f"Sentiment Analysis Result: {sentiment_result}")
        
    except Exception as e:
        logger.error(f"Error in example script: {str(e)}")
        raise

if __name__ == "__main__":
    main() 