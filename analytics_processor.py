import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import numpy as np
from sqlalchemy import func, and_
from models import (
    User, MoodEntry, GratitudeEntry, UserStrategies,
    UserResources, VoiceInteractions, UserGroups
)

logger = logging.getLogger(__name__)

class AnalyticsProcessor:
    def __init__(self, db):
        self.db = db

    def calculate_user_engagement(self, user_id: int, days: int = 30) -> Dict:
        """Calculate user engagement metrics over a specified period."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        metrics = {
            'mood_entries': self._count_mood_entries(user_id, start_date, end_date),
            'gratitude_entries': self._count_gratitude_entries(user_id, start_date, end_date),
            'voice_interactions': self._count_voice_interactions(user_id, start_date, end_date),
            'resource_access': self._count_resource_access(user_id, start_date, end_date),
            'strategy_usage': self._count_strategy_usage(user_id, start_date, end_date)
        }
        
        return {
            'total_engagement': sum(metrics.values()),
            'metrics': metrics,
            'period': {'start': start_date, 'end': end_date}
        }

    def analyze_mood_trends(self, user_id: int, days: int = 30) -> Dict:
        """Analyze mood trends and patterns."""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        entries = MoodEntry.query.filter(
            and_(
                MoodEntry.user_id == user_id,
                MoodEntry.created_at.between(start_date, end_date)
            )
        ).all()
        
        if not entries:
            return {'error': 'No mood entries found for the period'}
        
        mood_scores = [entry.mood_score for entry in entries]
        homesickness_scores = [entry.homesickness_level for entry in entries]
        
        return {
            'average_mood': np.mean(mood_scores),
            'mood_volatility': np.std(mood_scores),
            'average_homesickness': np.mean(homesickness_scores),
            'homesickness_trend': self._calculate_trend(homesickness_scores),
            'mood_patterns': self._identify_mood_patterns(entries)
        }

    def generate_resilience_insights(self, user_id: int) -> Dict:
        """Generate insights about resilience strategy effectiveness."""
        strategies = UserStrategies.query.filter_by(user_id=user_id).all()
        
        if not strategies:
            return {'error': 'No strategy usage data found'}
        
        effectiveness_by_category = {}
        for strategy in strategies:
            category = strategy.resilience_strategy.category
            if category not in effectiveness_by_category:
                effectiveness_by_category[category] = []
            if strategy.effectiveness_score:
                effectiveness_by_category[category].append(strategy.effectiveness_score)
        
        insights = {
            'most_effective_category': max(
                effectiveness_by_category.items(),
                key=lambda x: np.mean(x[1]) if x[1] else 0
            )[0],
            'effectiveness_by_category': {
                cat: np.mean(scores) if scores else None
                for cat, scores in effectiveness_by_category.items()
            },
            'recommendations': self._generate_strategy_recommendations(strategies)
        }
        
        return insights

    def analyze_social_engagement(self, user_id: int) -> Dict:
        """Analyze social engagement patterns."""
        groups = UserGroups.query.filter_by(user_id=user_id).all()
        voice_interactions = VoiceInteractions.query.filter_by(user_id=user_id).all()
        
        return {
            'group_participation': len(groups),
            'active_groups': [g.group_id for g in groups if g.role != 'inactive'],
            'voice_interaction_frequency': len(voice_interactions),
            'social_engagement_score': self._calculate_social_engagement_score(groups, voice_interactions)
        }

    def generate_wellness_report(self, user_id: int) -> Dict:
        """Generate a comprehensive wellness report."""
        mood_trends = self.analyze_mood_trends(user_id)
        resilience_insights = self.generate_resilience_insights(user_id)
        social_engagement = self.analyze_social_engagement(user_id)
        engagement_metrics = self.calculate_user_engagement(user_id)
        
        return {
            'overview': {
                'mood_status': self._interpret_mood_status(mood_trends),
                'homesickness_level': self._interpret_homesickness_level(mood_trends),
                'social_engagement': self._interpret_social_engagement(social_engagement),
                'resilience_progress': self._interpret_resilience_progress(resilience_insights)
            },
            'detailed_analysis': {
                'mood_trends': mood_trends,
                'resilience_insights': resilience_insights,
                'social_engagement': social_engagement,
                'engagement_metrics': engagement_metrics
            },
            'recommendations': self._generate_wellness_recommendations(
                mood_trends, resilience_insights, social_engagement
            )
        }

    # Helper methods
    def _count_mood_entries(self, user_id: int, start_date: datetime, end_date: datetime) -> int:
        return MoodEntry.query.filter(
            and_(
                MoodEntry.user_id == user_id,
                MoodEntry.created_at.between(start_date, end_date)
            )
        ).count()

    def _count_gratitude_entries(self, user_id: int, start_date: datetime, end_date: datetime) -> int:
        return GratitudeEntry.query.filter(
            and_(
                GratitudeEntry.user_id == user_id,
                GratitudeEntry.created_at.between(start_date, end_date)
            )
        ).count()

    def _count_voice_interactions(self, user_id: int, start_date: datetime, end_date: datetime) -> int:
        return VoiceInteractions.query.filter(
            and_(
                VoiceInteractions.user_id == user_id,
                VoiceInteractions.created_at.between(start_date, end_date)
            )
        ).count()

    def _count_resource_access(self, user_id: int, start_date: datetime, end_date: datetime) -> int:
        return UserResources.query.filter(
            and_(
                UserResources.user_id == user_id,
                UserResources.accessed_at.between(start_date, end_date)
            )
        ).count()

    def _count_strategy_usage(self, user_id: int, start_date: datetime, end_date: datetime) -> int:
        return UserStrategies.query.filter(
            and_(
                UserStrategies.user_id == user_id,
                UserStrategies.tried_at.between(start_date, end_date)
            )
        ).count()

    def _calculate_trend(self, values: List[float]) -> str:
        if len(values) < 2:
            return 'insufficient_data'
        
        slope = np.polyfit(range(len(values)), values, 1)[0]
        if slope > 0.1:
            return 'increasing'
        elif slope < -0.1:
            return 'decreasing'
        else:
            return 'stable'

    def _identify_mood_patterns(self, entries: List[MoodEntry]) -> Dict:
        # Implement pattern recognition logic
        # This could include:
        # - Day of week patterns
        # - Time of day patterns
        # - Correlation with specific events
        return {
            'day_of_week_patterns': {},
            'time_of_day_patterns': {},
            'event_correlations': {}
        }

    def _generate_strategy_recommendations(self, strategies: List[UserStrategies]) -> List[str]:
        # Implement recommendation logic based on:
        # - Most effective strategies
        # - Underutilized categories
        # - Recent mood patterns
        return []

    def _calculate_social_engagement_score(self, groups: List[UserGroups], 
                                         voice_interactions: List[VoiceInteractions]) -> float:
        # Implement scoring logic based on:
        # - Group participation
        # - Voice interaction frequency
        # - Interaction quality
        return 0.0

    def _interpret_mood_status(self, mood_trends: Dict) -> str:
        # Implement interpretation logic
        return 'neutral'

    def _interpret_homesickness_level(self, mood_trends: Dict) -> str:
        # Implement interpretation logic
        return 'moderate'

    def _interpret_social_engagement(self, social_engagement: Dict) -> str:
        # Implement interpretation logic
        return 'moderate'

    def _interpret_resilience_progress(self, resilience_insights: Dict) -> str:
        # Implement interpretation logic
        return 'improving'

    def _generate_wellness_recommendations(self, mood_trends: Dict, 
                                         resilience_insights: Dict,
                                         social_engagement: Dict) -> List[str]:
        # Implement recommendation generation logic
        return [] 