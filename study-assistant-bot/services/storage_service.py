"""
Storage service for Study Assistant Bot.
Handles local filesystem and AWS S3 storage.
"""

import logging
import os
from pathlib import Path
from typing import Optional, BinaryIO
from datetime import datetime
from config import Config

logger = logging.getLogger(__name__)


class StorageService:
    """Abstract storage service."""
    
    def upload_file(self, source_path: str, destination: str) -> bool:
        """Upload file to storage."""
        raise NotImplementedError
    
    def download_file(self, source: str, destination_path: str) -> bool:
        """Download file from storage."""
        raise NotImplementedError
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file from storage."""
        raise NotImplementedError
    
    def get_file_url(self, file_path: str) -> Optional[str]:
        """Get URL for file."""
        raise NotImplementedError


class LocalStorageService(StorageService):
    """Local filesystem storage service."""
    
    def __init__(self, base_path: str = None):
        """Initialize local storage service."""
        self.base_path = Path(base_path or Config.STORAGE_LOCAL_PATH)
        self.base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Local storage initialized at: {self.base_path}")
    
    def upload_file(self, source_path: str, destination: str) -> bool:
        """Upload file to local storage."""
        try:
            source = Path(source_path)
            if not source.exists():
                logger.error(f"Source file not found: {source_path}")
                return False
            
            dest = self.base_path / destination
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            dest.write_bytes(source.read_bytes())
            logger.info(f"File uploaded: {destination}")
            return True
        except Exception as e:
            logger.error(f"Error uploading file: {e}")
            return False
    
    def download_file(self, source: str, destination_path: str) -> bool:
        """Download file from local storage."""
        try:
            src = self.base_path / source
            if not src.exists():
                logger.error(f"Source file not found: {source}")
                return False
            
            dest = Path(destination_path)
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            dest.write_bytes(src.read_bytes())
            logger.info(f"File downloaded: {source}")
            return True
        except Exception as e:
            logger.error(f"Error downloading file: {e}")
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file from local storage."""
        try:
            path = self.base_path / file_path
            if path.exists():
                path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False
    
    def get_file_url(self, file_path: str) -> Optional[str]:
        """Get URL for local file."""
        return str(self.base_path / file_path)


class S3StorageService(StorageService):
    """AWS S3 storage service."""
    
    def __init__(self):
        """Initialize S3 storage service."""
        try:
            import boto3
            self.s3_client = boto3.client(
                's3',
                aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
                region_name=Config.AWS_REGION,
            )
            self.bucket_name = Config.AWS_BUCKET_NAME
            logger.info(f"S3 storage initialized for bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"Error initializing S3: {e}")
            raise
    
    def upload_file(self, source_path: str, destination: str) -> bool:
        """Upload file to S3."""
        try:
            self.s3_client.upload_file(
                source_path,
                self.bucket_name,
                destination,
                ExtraArgs={'ContentType': self._get_content_type(destination)},
            )
            logger.info(f"File uploaded to S3: {destination}")
            return True
        except Exception as e:
            logger.error(f"Error uploading file to S3: {e}")
            return False
    
    def download_file(self, source: str, destination_path: str) -> bool:
        """Download file from S3."""
        try:
            self.s3_client.download_file(
                self.bucket_name,
                source,
                destination_path,
            )
            logger.info(f"File downloaded from S3: {source}")
            return True
        except Exception as e:
            logger.error(f"Error downloading file from S3: {e}")
            return False
    
    def delete_file(self, file_path: str) -> bool:
        """Delete file from S3."""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_path,
            )
            logger.info(f"File deleted from S3: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error deleting file from S3: {e}")
            return False
    
    def get_file_url(self, file_path: str) -> Optional[str]:
        """Get URL for S3 file."""
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_path},
                ExpiresIn=3600,
            )
            return url
        except Exception as e:
            logger.error(f"Error generating presigned URL: {e}")
            return None
    
    @staticmethod
    def _get_content_type(file_path: str) -> str:
        """Get content type for file."""
        ext = Path(file_path).suffix.lower()
        content_types = {
            '.pdf': 'application/pdf',
            '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            '.txt': 'text/plain',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
        }
        return content_types.get(ext, 'application/octet-stream')


class StorageFactory:
    """Factory for creating storage service instances."""
    
    _instance: Optional[StorageService] = None
    
    @classmethod
    def get_storage(cls) -> StorageService:
        """Get storage service instance."""
        if cls._instance is None:
            storage_type = Config.STORAGE_TYPE.lower()
            
            if storage_type == "s3":
                cls._instance = S3StorageService()
            else:  # default to local
                cls._instance = LocalStorageService()
        
        return cls._instance


def get_storage_service() -> StorageService:
    """Get storage service instance."""
    return StorageFactory.get_storage()


def generate_file_path(user_id: int, document_name: str) -> str:
    """Generate standardized file path."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"documents/user_{user_id}/{timestamp}_{document_name}"
