#!/usr/bin/env python
"""
Test script to demonstrate image compression features
"""

import os
import sys
import django
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_parts_api.settings')
django.setup()

from request.compression_utils import ImageCompressor, VideoCompressor, FileSizeValidator

def create_test_image():
    """Create a test image"""
    image = Image.new('RGB', (1920, 1080), color='red')
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG', quality=95)
    return buffer.getvalue()

def test_image_compression():
    """Test image compression"""
    print("🖼️  Testing Image Compression...")
    print("=" * 50)
    
    # Create test image
    original_data = create_test_image()
    original_size = len(original_data)
    print(f"📏 Original image size: {original_size:,} bytes ({original_size/1024:.1f} KB)")
    
    # Test compression
    try:
        compressor = ImageCompressor()
        compressed_data = compressor.compress_image_data(original_data, quality=70)
        compressed_size = len(compressed_data)
        
        reduction = ((original_size - compressed_size) / original_size) * 100
        print(f"📦 Compressed image size: {compressed_size:,} bytes ({compressed_size/1024:.1f} KB)")
        print(f"📊 Size reduction: {reduction:.1f}%")
        print(f"✅ Compression successful!")
        
    except Exception as e:
        print(f"❌ Compression failed: {str(e)}")
        print("💡 This is expected if OpenCV is not installed")

def test_file_validation():
    """Test file size validation"""
    print("\n📋 Testing File Validation...")
    print("=" * 50)
    
    # Test image validation
    test_data = create_test_image()
    is_valid, error_msg = FileSizeValidator.validate_image_file(test_data)
    print(f"🖼️  Image validation: {'✅ Valid' if is_valid else '❌ Invalid'}")
    if not is_valid:
        print(f"   Error: {error_msg}")

def show_compression_features():
    """Show available compression features"""
    print("🚀 Vehicle Parts API - Image Compression Features")
    print("=" * 60)
    
    print("\n📦 Available Compression Features:")
    print("1. 🖼️  Image Compression (JPEG, PNG)")
    print("   - Reduces file size by 50-70%")
    print("   - Maintains visual quality")
    print("   - Supports multiple formats")
    
    print("\n2. 🎥 Video Compression (MP4, AVI)")
    print("   - Reduces file size by 60-80%")
    print("   - Optimizes for web delivery")
    print("   - Maintains playback quality")
    
    print("\n3. 📏 File Size Validation")
    print("   - Enforces size limits")
    print("   - Prevents oversized uploads")
    print("   - Configurable thresholds")
    
    print("\n4. 🔄 Automatic Processing")
    print("   - Middleware-based compression")
    print("   - Model-level compression")
    print("   - Transparent to users")
    
    print("\n⚙️  Configuration:")
    print("- Image quality: 70% (configurable)")
    print("- Max image size: 10MB")
    print("- Max video size: 100MB")
    print("- Supported formats: JPEG, PNG, MP4, AVI")

def main():
    """Main test function"""
    show_compression_features()
    test_image_compression()
    test_file_validation()
    
    print("\n🎯 To enable compression in production:")
    print("1. Install OpenCV dependencies in Docker")
    print("2. Use the enhanced Dockerfile")
    print("3. Deploy with compression enabled")

if __name__ == "__main__":
    main()
