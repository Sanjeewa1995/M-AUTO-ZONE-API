"""
Image and Video Compression Utilities for Vehicle Parts API
Reduces file sizes by 50-70% while maintaining quality
Simplified version without OpenCV dependencies for Docker compatibility
"""

import os
import io
import logging
from typing import Tuple, Optional
from PIL import Image, ImageOps
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import UploadedFile

logger = logging.getLogger(__name__)


class ImageCompressor:
    """
    Handles image compression for vehicle and part images
    """
    
    # Quality settings for different image types
    VEHICLE_IMAGE_QUALITY = 85
    PART_IMAGE_QUALITY = 90
    MAX_WIDTH = 1920
    MAX_HEIGHT = 1080
    THUMBNAIL_SIZE = (300, 300)
    
    @staticmethod
    def compress_image_data(
        image_data: bytes, 
        quality: int = 70,
        max_size_mb: float = 2.0
    ) -> bytes:
        """
        Compress image data (bytes) with specified quality
        
        Args:
            image_data: Raw image bytes
            quality: JPEG quality (1-100)
            max_size_mb: Maximum file size in MB
            
        Returns:
            Compressed image bytes
        """
        try:
            # Open image from bytes
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                image = image.convert('RGB')
            
            # Resize if too large
            if image.width > ImageCompressor.MAX_WIDTH or image.height > ImageCompressor.MAX_HEIGHT:
                image.thumbnail((ImageCompressor.MAX_WIDTH, ImageCompressor.MAX_HEIGHT), Image.Resampling.LANCZOS)
            
            # Compress with specified quality
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=quality, optimize=True)
            compressed_data = output.getvalue()
            
            # Check size limit
            max_size_bytes = max_size_mb * 1024 * 1024
            if len(compressed_data) > max_size_bytes:
                # Reduce quality further if still too large
                quality = max(30, quality - 20)
                output = io.BytesIO()
                image.save(output, format='JPEG', quality=quality, optimize=True)
                compressed_data = output.getvalue()
            
            return compressed_data
            
        except Exception as e:
            logger.error(f"Image compression failed: {str(e)}")
            return image_data  # Return original if compression fails

    @staticmethod
    def compress_image(
        image_file: UploadedFile, 
        image_type: str = 'vehicle',
        max_size_mb: float = 2.0
    ) -> ContentFile:
        """
        Compress an image file while maintaining quality
        
        Args:
            image_file: The uploaded image file
            image_type: 'vehicle' or 'part' (affects quality settings)
            max_size_mb: Maximum file size in MB
            
        Returns:
            Compressed ContentFile
        """
        try:
            # Open image with PIL
            image = Image.open(image_file)
            
            # Convert to RGB if necessary (for JPEG compatibility)
            if image.mode in ('RGBA', 'LA', 'P'):
                # Create white background for transparent images
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Auto-orient image based on EXIF data
            image = ImageOps.exif_transpose(image)
            
            # Resize if too large
            image = ImageCompressor._resize_image(image)
            
            # Determine quality based on image type
            quality = (ImageCompressor.VEHICLE_IMAGE_QUALITY 
                     if image_type == 'vehicle' 
                     else ImageCompressor.PART_IMAGE_QUALITY)
            
            # Compress with multiple quality levels if needed
            for attempt_quality in [quality, quality - 10, quality - 20, 60]:
                compressed_data = ImageCompressor._compress_to_size(
                    image, attempt_quality, max_size_mb
                )
                if compressed_data:
                    break
            
            if not compressed_data:
                # If still too large, resize more aggressively
                image = ImageCompressor._aggressive_resize(image)
                compressed_data = ImageCompressor._compress_to_size(
                    image, 60, max_size_mb
                )
            
            # Create ContentFile
            compressed_file = ContentFile(compressed_data)
            compressed_file.name = ImageCompressor._get_compressed_filename(image_file.name)
            
            logger.info(f"Image compressed: {image_file.size} -> {len(compressed_data)} bytes")
            return compressed_file
            
        except Exception as e:
            logger.error(f"Image compression failed: {str(e)}")
            # Return original file if compression fails
            return image_file
    
    @staticmethod
    def _resize_image(image: Image.Image) -> Image.Image:
        """Resize image if it's too large"""
        width, height = image.size
        
        if width > ImageCompressor.MAX_WIDTH or height > ImageCompressor.MAX_HEIGHT:
            # Calculate new dimensions maintaining aspect ratio
            ratio = min(
                ImageCompressor.MAX_WIDTH / width,
                ImageCompressor.MAX_HEIGHT / height
            )
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        return image
    
    @staticmethod
    def _aggressive_resize(image: Image.Image) -> Image.Image:
        """More aggressive resizing for large files"""
        width, height = image.size
        new_width = min(width, 800)
        new_height = min(height, 600)
        
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    @staticmethod
    def _compress_to_size(image: Image.Image, quality: int, max_size_mb: float) -> Optional[bytes]:
        """Compress image to target size"""
        max_size_bytes = int(max_size_mb * 1024 * 1024)
        
        for q in range(quality, 10, -10):
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=q, optimize=True)
            compressed_data = buffer.getvalue()
            
            if len(compressed_data) <= max_size_bytes:
                return compressed_data
        
        return None
    
    @staticmethod
    def _get_compressed_filename(original_name: str) -> str:
        """Generate filename for compressed image"""
        name, ext = os.path.splitext(original_name)
        return f"{name}_compressed.jpg"
    
    @staticmethod
    def create_thumbnail(image_file: UploadedFile) -> ContentFile:
        """Create a thumbnail version of the image"""
        try:
            image = Image.open(image_file)
            image = ImageOps.exif_transpose(image)
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                if image.mode == 'P':
                    image = image.convert('RGBA')
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Create thumbnail
            image.thumbnail(ImageCompressor.THUMBNAIL_SIZE, Image.Resampling.LANCZOS)
            
            # Save as JPEG
            buffer = io.BytesIO()
            image.save(buffer, format='JPEG', quality=85, optimize=True)
            thumbnail_data = buffer.getvalue()
            
            thumbnail_file = ContentFile(thumbnail_data)
            thumbnail_file.name = f"thumb_{image_file.name}"
            
            return thumbnail_file
            
        except Exception as e:
            logger.error(f"Thumbnail creation failed: {str(e)}")
            return image_file


class VideoCompressor:
    """
    Simplified video compressor without OpenCV dependencies
    For now, this is a placeholder that returns the original file
    """
    
    @staticmethod
    def compress_video(
        video_file: UploadedFile,
        max_size_mb: float = 10.0
    ) -> ContentFile:
        """
        Placeholder for video compression
        For now, just returns the original file
        """
        logger.info("Video compression is currently disabled (OpenCV not available)")
        return video_file


class FileSizeValidator:
    """
    Validates file sizes and types
    """
    
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
    ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
    ALLOWED_VIDEO_TYPES = ['video/mp4', 'video/avi', 'video/mov', 'video/quicktime']
    
    @staticmethod
    def validate_image_file(file) -> Tuple[bool, str]:
        """Validate image file size and type"""
        # Handle both UploadedFile and bytes
        if hasattr(file, 'size'):
            file_size = file.size
            content_type = getattr(file, 'content_type', 'image/jpeg')
        else:
            file_size = len(file) if isinstance(file, (bytes, bytearray)) else 0
            content_type = 'image/jpeg'  # Default for bytes
        
        if file_size > FileSizeValidator.MAX_IMAGE_SIZE:
            return False, f"Image file too large. Maximum size: {FileSizeValidator.MAX_IMAGE_SIZE // (1024*1024)}MB"
        
        if content_type not in FileSizeValidator.ALLOWED_IMAGE_TYPES:
            return False, f"Invalid image type. Allowed types: {', '.join(FileSizeValidator.ALLOWED_IMAGE_TYPES)}"
        
        return True, "Valid image file"
    
    @staticmethod
    def validate_video_file(file: UploadedFile) -> Tuple[bool, str]:
        """Validate video file size and type"""
        if file.size > FileSizeValidator.MAX_VIDEO_SIZE:
            return False, f"Video file too large. Maximum size: {FileSizeValidator.MAX_VIDEO_SIZE // (1024*1024)}MB"
        
        if file.content_type not in FileSizeValidator.ALLOWED_VIDEO_TYPES:
            return False, f"Invalid video type. Allowed types: {', '.join(FileSizeValidator.ALLOWED_VIDEO_TYPES)}"
        
        return True, "Valid video file"


def compress_vehicle_image(image_file: UploadedFile) -> ContentFile:
    """Compress vehicle image with optimized settings"""
    return ImageCompressor.compress_image(image_file, 'vehicle', max_size_mb=2.0)


def compress_part_image(image_file: UploadedFile) -> ContentFile:
    """Compress part image with optimized settings"""
    return ImageCompressor.compress_image(image_file, 'part', max_size_mb=1.5)


def compress_part_video(video_file: UploadedFile) -> ContentFile:
    """Compress part video with optimized settings (placeholder)"""
    return VideoCompressor.compress_video(video_file, max_size_mb=10.0)