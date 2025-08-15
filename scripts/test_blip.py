#!/usr/bin/env python3
"""
Test script for BLIP image analysis features
Run individual BLIP model automation features
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.blip_service import BLIPService
import json
import argparse

# Sample image URLs for testing (you can replace with your own)
SAMPLE_IMAGES = {
    "turmeric": "https://images.unsplash.com/photo-1615485290382-441e4d049cb5?w=500",
    "lavender": "https://images.unsplash.com/photo-1611909482911-0d829a5bfa9e?w=500", 
    "essential_oils": "https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?w=500",
    "supplements": "https://images.unsplash.com/photo-1559181567-c3190ca9959b?w=500"
}

def test_image_analysis():
    """Test basic image analysis"""
    print("🔍 Testing Product Image Analysis...")
    
    service = BLIPService()
    
    test_cases = [
        {
            "name": "Turmeric Product",
            "image_source": SAMPLE_IMAGES["turmeric"],
            "source_type": "url"
        },
        {
            "name": "Lavender Essential Oil",
            "image_source": SAMPLE_IMAGES["lavender"],
            "source_type": "url"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['name']}")
        print(f"🌐 Source: {test_case['image_source']}")
        
        try:
            result = service.analyze_product_image(
                image_source=test_case['image_source'],
                source_type=test_case['source_type']
            )
            
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Analysis completed:")
                analysis = result.get('analysis', {})
                print(f"🔍 General: {analysis.get('general_description', 'N/A')}")
                print(f"📦 Product: {analysis.get('product_description', 'N/A')}")
                print(f"🎨 Color/Appearance: {analysis.get('color_appearance', 'N/A')}")
                print(f"📦 Packaging: {analysis.get('packaging', 'N/A')}")
                print(f"🤖 Model: {result.get('model', 'Unknown')}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def test_alt_text_generation():
    """Test SEO alt text generation"""
    print("\n🏷️ Testing Alt Text Generation...")
    
    service = BLIPService()
    
    test_cases = [
        {
            "name": "Essential Oils Collection",
            "image_source": SAMPLE_IMAGES["essential_oils"],
            "source_type": "url",
            "product_name": "Organic Essential Oil Set"
        },
        {
            "name": "Health Supplements",
            "image_source": SAMPLE_IMAGES["supplements"],
            "source_type": "url",
            "product_name": "Natural Vitamin Supplements"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test Case {i}: {test_case['name']}")
        print(f"🌐 Source: {test_case['image_source']}")
        
        try:
            result = service.generate_alt_text(
                image_source=test_case['image_source'],
                source_type=test_case['source_type'],
                product_name=test_case.get('product_name')
            )
            
            if "error" in result:
                print(f"❌ Error: {result['error']}")
            else:
                print(f"✅ Alt text generated:")
                alt_texts = result.get('alt_texts', [])
                recommended = result.get('recommended', 'N/A')
                
                print(f"🎯 Recommended: {recommended}")
                print(f"📝 All options ({len(alt_texts)}):")
                for j, alt_text in enumerate(alt_texts[:3], 1):  # Show first 3
                    print(f"   {j}. {alt_text}")
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")

def test_batch_analysis():
    """Test batch image analysis"""
    print("\n📦 Testing Batch Image Analysis...")
    
    service = BLIPService()
    
    # Prepare batch of images
    image_batch = [
        {
            "source": SAMPLE_IMAGES["turmeric"],
            "type": "url",
            "name": "turmeric_product"
        },
        {
            "source": SAMPLE_IMAGES["lavender"],
            "type": "url",
            "name": "lavender_oil"
        },
        {
            "source": SAMPLE_IMAGES["supplements"],
            "type": "url",
            "name": "supplement_bottles"
        }
    ]
    
    print(f"🔍 Processing {len(image_batch)} images...")
    
    try:
        result = service.batch_analyze_images(image_batch)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print(f"✅ Batch analysis completed:")
            print(f"📊 Processed: {result.get('processed', 0)}/{result.get('total', 0)}")
            print(f"❌ Failed: {result.get('failed', 0)}")
            
            # Show results for each image
            results = result.get('results', {})
            for name, analysis_result in results.items():
                print(f"\n📷 {name}:")
                if 'analysis' in analysis_result:
                    analysis = analysis_result['analysis']
                    print(f"   🔍 {analysis.get('general_description', 'N/A')[:100]}...")
                else:
                    print(f"   ❌ No analysis available")
            
            # Show any errors
            errors = result.get('errors', [])
            if errors:
                print(f"\n❌ Errors encountered:")
                for error in errors:
                    print(f"   • {error.get('image', 'Unknown')}: {error.get('error', 'Unknown error')}")
                
    except Exception as e:
        print(f"❌ Exception: {str(e)}")

def test_local_image():
    """Test with local image file (if available)"""
    print("\n💾 Testing Local Image Analysis...")
    
    # Look for sample images in the project
    sample_paths = [
        "../public/images/turmeric.jpg",
        "../public/images/essential.jpg",
        "sample_product.jpg",
        "test_image.jpg"
    ]
    
    service = BLIPService()
    local_image_found = False
    
    for path in sample_paths:
        if os.path.exists(path):
            local_image_found = True
            print(f"📁 Found local image: {path}")
            
            try:
                result = service.analyze_product_image(
                    image_source=path,
                    source_type="path"
                )
                
                if "error" in result:
                    print(f"❌ Error: {result['error']}")
                else:
                    print(f"✅ Local image analysis completed:")
                    analysis = result.get('analysis', {})
                    print(f"🔍 Description: {analysis.get('general_description', 'N/A')}")
                    
            except Exception as e:
                print(f"❌ Exception: {str(e)}")
            break
    
    if not local_image_found:
        print("📁 No local sample images found. Skipping local image test.")
        print("💡 To test with local images, place sample images in the project directory.")

def test_base64_image():
    """Test with base64 encoded image"""
    print("\n🔤 Testing Base64 Image Analysis...")
    
    # This is a minimal test - in practice you would have actual base64 image data
    print("💡 Base64 testing requires actual image data.")
    print("   To test this feature, provide a base64-encoded image string.")
    print("   Example: data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/...")

def main():
    """Main function to run tests"""
    parser = argparse.ArgumentParser(description='Test BLIP Image Analysis Features')
    parser.add_argument('--feature', choices=[
        'analysis', 'alt-text', 'batch', 'local', 'base64', 'all'
    ], default='all', help='Feature to test')
    
    args = parser.parse_args()
    
    print("🖼️ BLIP Image Analysis Testing")
    print("=" * 50)
    print("📝 Note: This requires internet connection for loading sample images")
    print("🤖 BLIP model will be downloaded on first run (may take some time)")
    print()
    
    try:
        if args.feature == 'all':
            test_image_analysis()
            test_alt_text_generation()
            test_batch_analysis()
            test_local_image()
            test_base64_image()
        elif args.feature == 'analysis':
            test_image_analysis()
        elif args.feature == 'alt-text':
            test_alt_text_generation()
        elif args.feature == 'batch':
            test_batch_analysis()
        elif args.feature == 'local':
            test_local_image()
        elif args.feature == 'base64':
            test_base64_image()
        
        print("\n✅ Testing completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
