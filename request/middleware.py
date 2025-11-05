"""
Middleware for automatic file compression
Handles compression of uploaded files before they reach the views
"""

import logging
from django.core.files.uploadedfile import UploadedFile
from django.core.files.base import ContentFile
from .utils.compression_utils import (
    ImageCompressor, 
    VideoCompressor, 
    FileSizeValidator
)

logger = logging.getLogger(__name__)


class FileCompressionMiddleware:
    """
    Middleware to automatically compress uploaded files
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process request before it reaches the view
        if request.method == 'POST' and request.FILES:
            request = self._compress_uploaded_files(request)
        
        response = self.get_response(request)
        return response
    
    def _compress_uploaded_files(self, request):
        """
        Compress uploaded files based on field names
        """
        try:
            # Process each uploaded file
            for field_name, uploaded_file in request.FILES.items():
                if not isinstance(uploaded_file, UploadedFile):
                    continue
                
                # Determine compression type based on field name
                if 'vehicle_image' in field_name.lower():
                    compressed_file = self._compress_vehicle_image(uploaded_file)
                    if compressed_file:
                        request.FILES[field_name] = compressed_file
                
                elif 'part_image' in field_name.lower():
                    compressed_file = self._compress_part_image(uploaded_file)
                    if compressed_file:
                        request.FILES[field_name] = compressed_file
                
                elif 'part_video' in field_name.lower():
                    compressed_file = self._compress_part_video(uploaded_file)
                    if compressed_file:
                        request.FILES[field_name] = compressed_file
                
                # Generic image compression for other image fields
                elif uploaded_file.content_type and uploaded_file.content_type.startswith('image/'):
                    compressed_file = self._compress_generic_image(uploaded_file)
                    if compressed_file:
                        request.FILES[field_name] = compressed_file
                
                # Generic video compression for other video fields
                elif uploaded_file.content_type and uploaded_file.content_type.startswith('video/'):
                    compressed_file = self._compress_generic_video(uploaded_file)
                    if compressed_file:
                        request.FILES[field_name] = compressed_file
        
        except Exception as e:
            logger.error(f"File compression middleware error: {str(e)}")
            # Continue with original files if compression fails
        
        return request
    
    def _compress_vehicle_image(self, uploaded_file):
        """Compress vehicle image with specific settings"""
        try:
            # Validate file first
            is_valid, error_msg = FileSizeValidator.validate_image_file(uploaded_file)
            if not is_valid:
                logger.warning(f"Vehicle image validation failed: {error_msg}")
                return None
            
            # Compress with vehicle-specific settings
            compressed_file = ImageCompressor.compress_image(
                uploaded_file, 
                image_type='vehicle',
                max_size_mb=2.0
            )
            
            logger.info(f"Vehicle image compressed: {uploaded_file.size} -> {compressed_file.size} bytes")
            return compressed_file
            
        except Exception as e:
            logger.error(f"Vehicle image compression failed: {str(e)}")
            return None
    
    def _compress_part_image(self, uploaded_file):
        """Compress part image with specific settings"""
        try:
            # Validate file first
            is_valid, error_msg = FileSizeValidator.validate_image_file(uploaded_file)
            if not is_valid:
                logger.warning(f"Part image validation failed: {error_msg}")
                return None
            
            # Compress with part-specific settings
            compressed_file = ImageCompressor.compress_image(
                uploaded_file, 
                image_type='part',
                max_size_mb=1.5
            )
            
            logger.info(f"Part image compressed: {uploaded_file.size} -> {compressed_file.size} bytes")
            return compressed_file
            
        except Exception as e:
            logger.error(f"Part image compression failed: {str(e)}")
            return None
    
    def _compress_part_video(self, uploaded_file):
        """Compress part video with specific settings"""
        try:
            # Validate file first
            is_valid, error_msg = FileSizeValidator.validate_video_file(uploaded_file)
            if not is_valid:
                logger.warning(f"Part video validation failed: {error_msg}")
                return None
            
            # Compress with video-specific settings
            compressed_file = VideoCompressor.compress_video(
                uploaded_file,
                max_size_mb=10.0
            )
            
            logger.info(f"Part video compressed: {uploaded_file.size} -> {compressed_file.size} bytes")
            return compressed_file
            
        except Exception as e:
            logger.error(f"Part video compression failed: {str(e)}")
            return None
    
    def _compress_generic_image(self, uploaded_file):
        """Compress generic image files"""
        try:
            # Validate file first
            is_valid, error_msg = FileSizeValidator.validate_image_file(uploaded_file)
            if not is_valid:
                logger.warning(f"Generic image validation failed: {error_msg}")
                return None
            
            # Compress with default settings
            compressed_file = ImageCompressor.compress_image(
                uploaded_file, 
                image_type='part',  # Use part settings as default
                max_size_mb=2.0
            )
            
            logger.info(f"Generic image compressed: {uploaded_file.size} -> {compressed_file.size} bytes")
            return compressed_file
            
        except Exception as e:
            logger.error(f"Generic image compression failed: {str(e)}")
            return None
    
    def _compress_generic_video(self, uploaded_file):
        """Compress generic video files"""
        try:
            # Validate file first
            is_valid, error_msg = FileSizeValidator.validate_video_file(uploaded_file)
            if not is_valid:
                logger.warning(f"Generic video validation failed: {error_msg}")
                return None
            
            # Compress with default settings
            compressed_file = VideoCompressor.compress_video(
                uploaded_file,
                max_size_mb=15.0
            )
            
            logger.info(f"Generic video compressed: {uploaded_file.size} -> {compressed_file.size} bytes")
            return compressed_file
            
        except Exception as e:
            logger.error(f"Generic video compression failed: {str(e)}")
            return None


class CompressionStatsMiddleware:
    """
    Middleware to track compression statistics
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.stats = {
            'images_compressed': 0,
            'videos_compressed': 0,
            'total_bytes_saved': 0,
            'compression_errors': 0
        }
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add compression stats to response headers (for debugging)
        if hasattr(request, '_compression_stats'):
            response['X-Images-Compressed'] = str(request._compression_stats.get('images', 0))
            response['X-Videos-Compressed'] = str(request._compression_stats.get('videos', 0))
            response['X-Bytes-Saved'] = str(request._compression_stats.get('bytes_saved', 0))
        
        return response
    
    def get_stats(self):
        """Get compression statistics"""
        return self.stats.copy()
    
    def reset_stats(self):
        """Reset compression statistics"""
        self.stats = {
            'images_compressed': 0,
            'videos_compressed': 0,
            'total_bytes_saved': 0,
            'compression_errors': 0
        }
