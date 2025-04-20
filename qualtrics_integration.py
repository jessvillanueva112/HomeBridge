import logging
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from config import Config

logger = logging.getLogger(__name__)

class QualtricsIntegration:
    def __init__(self):
        self.config = Config()
        self.base_url = f"https://{self.config.QUALTRICS_DATA_CENTER}.qualtrics.com/API/v3"
        self.headers = {
            "X-API-TOKEN": self.config.QUALTRICS_API_TOKEN,
            "Content-Type": "application/json"
        }

    def get_survey_responses(self, survey_id: str, start_date: Optional[datetime] = None) -> List[Dict]:
        """Get survey responses from Qualtrics"""
        try:
            endpoint = f"{self.base_url}/surveys/{survey_id}/responses"
            
            # Add date filter if provided
            params = {}
            if start_date:
                params["startDate"] = start_date.isoformat()
            
            response = requests.get(endpoint, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data.get("result", {}).get("elements", [])
        except Exception as e:
            logger.error(f"Error getting survey responses: {str(e)}")
            return []

    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text using Qualtrics sentiment analysis"""
        try:
            endpoint = f"{self.base_url}/sentiment/analyze"
            
            payload = {
                "text": text,
                "language": "en"  # Default to English
            }
            
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {"error": str(e)}

    def get_user_sentiment_history(self, user_id: int, days: int = 30) -> List[Dict]:
        """Get sentiment history for a specific user"""
        try:
            # Get survey responses for the user
            survey_id = self.config.QUALTRICS_USER_SURVEY_ID
            start_date = datetime.now() - timedelta(days=days)
            
            responses = self.get_survey_responses(survey_id, start_date)
            
            # Filter responses for the specific user
            user_responses = [
                response for response in responses
                if response.get("userId") == str(user_id)
            ]
            
            # Analyze sentiment for each response
            sentiment_history = []
            for response in user_responses:
                text = response.get("text", "")
                if text:
                    sentiment = self.analyze_sentiment(text)
                    sentiment_history.append({
                        "timestamp": response.get("timestamp"),
                        "text": text,
                        "sentiment": sentiment
                    })
            
            return sentiment_history
        except Exception as e:
            logger.error(f"Error getting user sentiment history: {str(e)}")
            return []

    def get_sentiment_trends(self, user_id: int, days: int = 30) -> Dict:
        """Get sentiment trends for a specific user"""
        try:
            sentiment_history = self.get_user_sentiment_history(user_id, days)
            
            if not sentiment_history:
                return {"error": "No sentiment data available"}
            
            # Calculate average sentiment
            sentiments = [entry["sentiment"].get("score", 0) for entry in sentiment_history]
            avg_sentiment = sum(sentiments) / len(sentiments)
            
            # Calculate sentiment volatility
            volatility = sum((s - avg_sentiment) ** 2 for s in sentiments) / len(sentiments)
            
            # Identify significant changes
            changes = []
            for i in range(1, len(sentiments)):
                change = sentiments[i] - sentiments[i-1]
                if abs(change) > 0.5:  # Threshold for significant change
                    changes.append({
                        "timestamp": sentiment_history[i]["timestamp"],
                        "change": change
                    })
            
            return {
                "average_sentiment": avg_sentiment,
                "volatility": volatility,
                "significant_changes": changes,
                "total_entries": len(sentiment_history)
            }
        except Exception as e:
            logger.error(f"Error getting sentiment trends: {str(e)}")
            return {"error": str(e)}

    def sync_qualtrics_data(self, user_id: int) -> Dict:
        """Sync Qualtrics data for a specific user"""
        try:
            logger.info(f"Starting Qualtrics data sync for user {user_id}")
            
            # Get sentiment history
            sentiment_history = self.get_user_sentiment_history(user_id)
            
            # Get sentiment trends
            sentiment_trends = self.get_sentiment_trends(user_id)
            
            # Prepare sync report
            sync_report = {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "sentiment_history_count": len(sentiment_history),
                "sentiment_trends": sentiment_trends,
                "status": "success"
            }
            
            logger.info(f"Qualtrics data sync completed for user {user_id}")
            return sync_report
        except Exception as e:
            logger.error(f"Error syncing Qualtrics data for user {user_id}: {str(e)}")
            return {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "status": "error",
                "error": str(e)
            } 