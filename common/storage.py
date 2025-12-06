"""
Custom storage backends for DigitalOcean Spaces
"""
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class DigitalOceanSpacesStorage(S3Boto3Storage):
    """
    Custom storage backend for DigitalOcean Spaces
    """
    default_acl = 'public-read'
    file_overwrite = False
    
    def __init__(self, *args, **kwargs):
        kwargs['endpoint_url'] = getattr(settings, 'AWS_S3_ENDPOINT_URL', None)
        kwargs['region_name'] = getattr(settings, 'AWS_S3_REGION_NAME', None)
        super().__init__(*args, **kwargs)

