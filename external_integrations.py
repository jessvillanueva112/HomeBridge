import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional
import json
from models import db, Resource, SupportGroup, User
from config import Config

logger = logging.getLogger(__name__)

class ExternalIntegrations:
    def __init__(self):
        self.config = Config()
        self.session = requests.Session()
        self.setup_authentication()

    def setup_authentication(self):
        """Setup authentication for external services"""
        self.session.headers.update({
            'Authorization': f'Bearer {self.config.UBC_API_KEY}',
            'Content-Type': 'application/json'
        })

    def sync_ubc_counselling_services(self) -> List[Resource]:
        """Sync UBC Counselling Services resources"""
        try:
            # UBC Counselling Services API endpoint
            response = self.session.get(
                'https://students.ubc.ca/api/counselling-services'
            )
            data = response.json()

            resources = []
            for service in data['services']:
                resource = Resource(
                    name=service['name'],
                    description=service['description'],
                    category='Mental Health',
                    location=service.get('location', 'UBC Counselling Services'),
                    contact_info=service.get('contact'),
                    hours=service.get('hours'),
                    url=service.get('url')
                )
                resources.append(resource)
                db.session.add(resource)

            db.session.commit()
            return resources
        except Exception as e:
            logger.error(f"Error syncing UBC Counselling Services: {str(e)}")
            return []

    def sync_ubc_support_groups(self) -> List[SupportGroup]:
        """Sync UBC Support Groups"""
        try:
            # UBC Support Groups API endpoint
            response = self.session.get(
                'https://students.ubc.ca/api/support-groups'
            )
            data = response.json()

            groups = []
            for group in data['groups']:
                support_group = SupportGroup(
                    name=group['name'],
                    description=group['description'],
                    meeting_time=group.get('meeting_time'),
                    location=group.get('location'),
                    contact_person=group.get('contact_person'),
                    contact_email=group.get('contact_email')
                )
                groups.append(support_group)
                db.session.add(support_group)

            db.session.commit()
            return groups
        except Exception as e:
            logger.error(f"Error syncing UBC Support Groups: {str(e)}")
            return []

    def sync_qualtrics_sentiment_data(self, user_id: int) -> Dict:
        """Sync sentiment analysis data from Qualtrics"""
        try:
            # Qualtrics API endpoint
            response = self.session.get(
                f'https://api.qualtrics.com/v3/sentiment-analysis',
                params={'userId': user_id}
            )
            data = response.json()

            return {
                'sentiment_score': data.get('sentiment_score'),
                'key_phrases': data.get('key_phrases', []),
                'emotions': data.get('emotions', {})
            }
        except Exception as e:
            logger.error(f"Error syncing Qualtrics sentiment data: {str(e)}")
            return {}

    def sync_ubc_student_services(self) -> List[Resource]:
        """Sync UBC Student Services resources"""
        try:
            # UBC Student Services API endpoint
            response = self.session.get(
                'https://students.ubc.ca/api/student-services'
            )
            data = response.json()

            resources = []
            for service in data['services']:
                resource = Resource(
                    name=service['name'],
                    description=service['description'],
                    category=service.get('category', 'Student Services'),
                    location=service.get('location'),
                    contact_info=service.get('contact'),
                    hours=service.get('hours'),
                    url=service.get('url')
                )
                resources.append(resource)
                db.session.add(resource)

            db.session.commit()
            return resources
        except Exception as e:
            logger.error(f"Error syncing UBC Student Services: {str(e)}")
            return []

    def sync_ubc_international_student_services(self) -> List[Resource]:
        """Sync UBC International Student Services"""
        try:
            # UBC International Student Services API endpoint
            response = self.session.get(
                'https://students.ubc.ca/api/international-student-services'
            )
            data = response.json()

            resources = []
            for service in data['services']:
                resource = Resource(
                    name=service['name'],
                    description=service['description'],
                    category='International Student Support',
                    location=service.get('location'),
                    contact_info=service.get('contact'),
                    hours=service.get('hours'),
                    url=service.get('url')
                )
                resources.append(resource)
                db.session.add(resource)

            db.session.commit()
            return resources
        except Exception as e:
            logger.error(f"Error syncing UBC International Student Services: {str(e)}")
            return []

    def sync_ubc_events(self) -> List[Dict]:
        """Sync UBC Events"""
        try:
            # UBC Events API endpoint
            response = self.session.get(
                'https://events.ubc.ca/api/events',
                params={'category': 'international_students'}
            )
            data = response.json()

            return data.get('events', [])
        except Exception as e:
            logger.error(f"Error syncing UBC Events: {str(e)}")
            return []

    def sync_ubc_academic_resources(self) -> List[Resource]:
        """Sync UBC Academic Resources"""
        try:
            # UBC Academic Resources API endpoint
            response = self.session.get(
                'https://students.ubc.ca/api/academic-resources'
            )
            data = response.json()

            resources = []
            for resource in data['resources']:
                academic_resource = Resource(
                    name=resource['name'],
                    description=resource['description'],
                    category='Academic Support',
                    location=resource.get('location'),
                    contact_info=resource.get('contact'),
                    hours=resource.get('hours'),
                    url=resource.get('url')
                )
                resources.append(academic_resource)
                db.session.add(academic_resource)

            db.session.commit()
            return resources
        except Exception as e:
            logger.error(f"Error syncing UBC Academic Resources: {str(e)}")
            return []

    def sync_all_resources(self) -> Dict:
        """Sync all external resources"""
        return {
            'counselling_services': self.sync_ubc_counselling_services(),
            'support_groups': self.sync_ubc_support_groups(),
            'student_services': self.sync_ubc_student_services(),
            'international_services': self.sync_ubc_international_student_services(),
            'academic_resources': self.sync_ubc_academic_resources(),
            'events': self.sync_ubc_events()
        }

    def update_user_profile(self, user_id: int, external_data: Dict) -> bool:
        """Update user profile with external data"""
        try:
            user = User.query.get(user_id)
            if not user:
                return False

            # Update user profile with external data
            if 'profile' in external_data:
                profile_data = external_data['profile']
                if hasattr(user, 'profile'):
                    for key, value in profile_data.items():
                        if hasattr(user.profile, key):
                            setattr(user.profile, key, value)

            db.session.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating user profile: {str(e)}")
            return False

    def verify_data_consistency(self) -> Dict:
        """Verify data consistency between internal and external sources"""
        try:
            # Get counts from internal database
            internal_counts = {
                'resources': Resource.query.count(),
                'support_groups': SupportGroup.query.count(),
                'users': User.query.count()
            }

            # Get counts from external APIs
            external_counts = {
                'resources': len(self.sync_ubc_student_services()),
                'support_groups': len(self.sync_ubc_support_groups()),
                'users': 0  # This would need to be implemented based on your authentication system
            }

            return {
                'internal_counts': internal_counts,
                'external_counts': external_counts,
                'discrepancies': {
                    key: abs(internal_counts[key] - external_counts[key])
                    for key in internal_counts
                }
            }
        except Exception as e:
            logger.error(f"Error verifying data consistency: {str(e)}")
            return {} 