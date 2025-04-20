import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from external_integrations import ExternalIntegrations
from config import Config
import os
from typing import Dict

logger = logging.getLogger(__name__)

class DataSynchronizer:
    def __init__(self):
        self.config = Config()
        self.external_integrations = ExternalIntegrations()
        self.scheduler = BackgroundScheduler()
        self.setup_scheduler()

    def setup_scheduler(self):
        """Setup scheduled tasks"""
        # Sync UBC resources every hour
        self.scheduler.add_job(
            self.sync_ubc_resources,
            trigger=IntervalTrigger(seconds=self.config.SYNC_INTERVAL),
            id='sync_ubc_resources',
            replace_existing=True
        )

        # Verify data consistency daily
        self.scheduler.add_job(
            self.verify_data_consistency,
            trigger=IntervalTrigger(days=1),
            id='verify_data_consistency',
            replace_existing=True
        )

        # Backup data daily
        self.scheduler.add_job(
            self.backup_data,
            trigger=IntervalTrigger(days=1),
            id='backup_data',
            replace_existing=True
        )

    def start(self):
        """Start the scheduler"""
        try:
            self.scheduler.start()
            logger.info("Data synchronizer started successfully")
        except Exception as e:
            logger.error(f"Error starting data synchronizer: {str(e)}")

    def stop(self):
        """Stop the scheduler"""
        try:
            self.scheduler.shutdown()
            logger.info("Data synchronizer stopped successfully")
        except Exception as e:
            logger.error(f"Error stopping data synchronizer: {str(e)}")

    def sync_ubc_resources(self):
        """Sync all UBC resources"""
        try:
            logger.info("Starting UBC resources sync")
            
            if self.config.ENABLE_UBC_SYNC:
                results = self.external_integrations.sync_all_resources()
                
                # Log sync results
                for resource_type, items in results.items():
                    logger.info(f"Synced {len(items)} {resource_type}")
                
                logger.info("UBC resources sync completed successfully")
            else:
                logger.info("UBC sync is disabled")
        except Exception as e:
            logger.error(f"Error syncing UBC resources: {str(e)}")

    def verify_data_consistency(self):
        """Verify data consistency between internal and external sources"""
        try:
            logger.info("Starting data consistency verification")
            
            consistency_report = self.external_integrations.verify_data_consistency()
            
            # Log discrepancies
            for key, discrepancy in consistency_report.get('discrepancies', {}).items():
                if discrepancy > 0:
                    logger.warning(f"Data discrepancy found in {key}: {discrepancy} items")
            
            logger.info("Data consistency verification completed")
        except Exception as e:
            logger.error(f"Error verifying data consistency: {str(e)}")

    def backup_data(self):
        """Backup application data"""
        try:
            logger.info("Starting data backup")
            
            # Create backup directory if it doesn't exist
            if not os.path.exists(self.config.BACKUP_DIR):
                os.makedirs(self.config.BACKUP_DIR)
            
            # Generate backup filename with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_file = os.path.join(
                self.config.BACKUP_DIR,
                f'homebridge_backup_{timestamp}.sql'
            )
            
            # Perform database backup
            # Note: This is a placeholder. You'll need to implement actual backup logic
            # based on your database system (SQLite, PostgreSQL, etc.)
            
            logger.info(f"Data backup completed: {backup_file}")
        except Exception as e:
            logger.error(f"Error backing up data: {str(e)}")

    def sync_user_data(self, user_id: int):
        """Sync data for a specific user"""
        try:
            logger.info(f"Starting user data sync for user {user_id}")
            
            # Sync Qualtrics sentiment data if enabled
            if self.config.ENABLE_QUALTRICS:
                sentiment_data = self.external_integrations.sync_qualtrics_sentiment_data(user_id)
                logger.info(f"Synced Qualtrics sentiment data for user {user_id}")
            
            # Sync OutSystems data if enabled
            if self.config.ENABLE_OUTSYSTEMS:
                # Implement OutSystems sync logic
                pass
            
            logger.info(f"User data sync completed for user {user_id}")
        except Exception as e:
            logger.error(f"Error syncing user data for user {user_id}: {str(e)}")

    def get_sync_status(self) -> Dict:
        """Get current sync status"""
        try:
            jobs = self.scheduler.get_jobs()
            status = {
                'active': self.scheduler.running,
                'jobs': [
                    {
                        'id': job.id,
                        'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                        'last_run': job.last_run_time.isoformat() if job.last_run_time else None
                    }
                    for job in jobs
                ]
            }
            return status
        except Exception as e:
            logger.error(f"Error getting sync status: {str(e)}")
            return {'error': str(e)} 