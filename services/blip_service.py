"""
BLIP Image Captioning Service
Handles product image analysis and caption generation using Hugging Face BLIP model
"""
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests
import logging
from typing import Dict, Any, Optional
from config import Config
import io
import base64

logger = logging.getLogger(__name__)

class BLIPService:
    """Service class for BLIP image captioning operations"""
    
    def __init__(self):
        """Initialize BLIP service"""
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = None
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load BLIP model and processor"""
        try:
            logger.info(f"Loading BLIP model on {self.device}...")
            self.processor = BlipProcessor.from_pretrained(Config.BLIP_MODEL_NAME)
            self.model = BlipForConditionalGeneration.from_pretrained(Config.BLIP_MODEL_NAME)
            self.model.to(self.device)
            logger.info("BLIP model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading BLIP model: {str(e)}")
            raise
    
    def load_image_from_url(self, image_url: str) -> Image.Image:
        """
        Load image from URL
        
        Args:
            image_url: URL of the image
            
        Returns:
            PIL Image object
        """
        try:
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content)).convert('RGB')
            return image
        except Exception as e:
            logger.error(f"Error loading image from URL {image_url}: {str(e)}")
            raise
    
    def load_image_from_base64(self, base64_string: str) -> Image.Image:
        """
        Load image from base64 string
        
        Args:
            base64_string: Base64 encoded image
            
        Returns:
            PIL Image object
        """
        try:
            # Remove data URL prefix if present
            if base64_string.startswith('data:image'):
                base64_string = base64_string.split(',')[1]
            
            image_data = base64.b64decode(base64_string)
            image = Image.open(io.BytesIO(image_data)).convert('RGB')
            return image
        except Exception as e:
            logger.error(f"Error loading image from base64: {str(e)}")
            raise
    
    def load_image_from_path(self, image_path: str) -> Image.Image:
        """
        Load image from file path
        
        Args:
            image_path: Path to the image file
            
        Returns:
            PIL Image object
        """
        try:
            image = Image.open(image_path).convert('RGB')
            return image
        except Exception as e:
            logger.error(f"Error loading image from path {image_path}: {str(e)}")
            raise
    
    def generate_caption(self, image: Image.Image, 
                        conditional_text: str = None, 
                        max_length: int = 50) -> Dict[str, Any]:
        """
        Generate caption for image
        
        Args:
            image: PIL Image object
            conditional_text: Optional conditional text to guide caption generation
            max_length: Maximum length of generated caption
            
        Returns:
            Dict containing caption and metadata
        """
        try:
            if self.model is None or self.processor is None:
                raise RuntimeError("BLIP model not loaded")
            
            if conditional_text:
                # Conditional image captioning
                inputs = self.processor(image, conditional_text, return_tensors="pt").to(self.device)
            else:
                # Unconditional image captioning
                inputs = self.processor(image, return_tensors="pt").to(self.device)
            
            with torch.no_grad():
                out = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=5,
                    early_stopping=True,
                    do_sample=True,
                    temperature=0.7
                )
            
            caption = self.processor.decode(out[0], skip_special_tokens=True)
            
            # Clean up caption if it contains conditional text
            if conditional_text and caption.lower().startswith(conditional_text.lower()):
                caption = caption[len(conditional_text):].strip()
            
            result = {
                "caption": caption,
                "conditional_text": conditional_text,
                "model": Config.BLIP_MODEL_NAME,
                "device": self.device,
                "generated_at": "2025-08-14T19:18:38Z"
            }
            
            logger.info(f"Generated caption: {caption[:50]}...")
            return result
            
        except Exception as e:
            logger.error(f"Error generating caption: {str(e)}")
            return {"error": str(e)}
    
    def analyze_product_image(self, image_source: str, source_type: str = "url") -> Dict[str, Any]:
        """
        Analyze product image and generate detailed description
        
        Args:
            image_source: Image source (URL, path, or base64)
            source_type: Type of source ("url", "path", "base64")
            
        Returns:
            Dict containing detailed image analysis
        """
        try:
            # Load image based on source type
            if source_type == "url":
                image = self.load_image_from_url(image_source)
            elif source_type == "path":
                image = self.load_image_from_path(image_source)
            elif source_type == "base64":
                image = self.load_image_from_base64(image_source)
            else:
                raise ValueError(f"Unsupported source type: {source_type}")
            
            # Generate different types of captions
            analyses = {}
            
            # General description
            general_result = self.generate_caption(image)
            analyses["general_description"] = general_result.get("caption", "")
            
            # Product-focused description
            product_result = self.generate_caption(
                image, 
                conditional_text="This is a product image showing", 
                max_length=60
            )
            analyses["product_description"] = product_result.get("caption", "")
            
            # Color and appearance
            color_result = self.generate_caption(
                image, 
                conditional_text="The color and appearance of this product is", 
                max_length=40
            )
            analyses["color_appearance"] = color_result.get("caption", "")
            
            # Packaging and presentation
            packaging_result = self.generate_caption(
                image, 
                conditional_text="The packaging shows", 
                max_length=50
            )
            analyses["packaging"] = packaging_result.get("caption", "")
            
            # Generate comprehensive analysis
            result = {
                "analysis": analyses,
                "image_source": image_source if source_type != "base64" else "base64_data",
                "source_type": source_type,
                "model": Config.BLIP_MODEL_NAME,
                "device": self.device,
                "generated_at": "2025-08-14T19:18:38Z"
            }
            
            logger.info(f"Analyzed product image from {source_type}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing product image: {str(e)}")
            return {"error": str(e)}
    
    def generate_alt_text(self, image_source: str, source_type: str = "url", 
                         product_name: str = None) -> Dict[str, Any]:
        """
        Generate SEO-friendly alt text for product images
        
        Args:
            image_source: Image source
            source_type: Type of source
            product_name: Optional product name for context
            
        Returns:
            Dict containing alt text suggestions
        """
        try:
            # Get image analysis
            analysis = self.analyze_product_image(image_source, source_type)
            
            if "error" in analysis:
                return analysis
            
            # Extract key information
            general_desc = analysis["analysis"].get("general_description", "")
            product_desc = analysis["analysis"].get("product_description", "")
            color_appearance = analysis["analysis"].get("color_appearance", "")
            
            # Generate different alt text options
            alt_texts = []
            
            # Option 1: Product name + general description
            if product_name:
                alt_texts.append(f"{product_name} - {general_desc}")
                alt_texts.append(f"{product_name} {color_appearance}")
            
            # Option 2: Detailed product description
            alt_texts.append(product_desc)
            
            # Option 3: Color and appearance focused
            alt_texts.append(f"{color_appearance} {general_desc}")
            
            # Option 4: Simple and clean
            alt_texts.append(general_desc)
            
            # Clean up and filter alt texts
            clean_alt_texts = []
            for alt_text in alt_texts:
                if alt_text and len(alt_text.strip()) > 5:
                    # Limit to 125 characters for SEO best practices
                    clean_text = alt_text.strip()[:125]
                    if clean_text not in clean_alt_texts:
                        clean_alt_texts.append(clean_text)
            
            result = {
                "alt_texts": clean_alt_texts,
                "recommended": clean_alt_texts[0] if clean_alt_texts else "Product image",
                "product_name": product_name,
                "analysis_used": analysis["analysis"],
                "generated_at": "2025-08-14T19:18:38Z"
            }
            
            logger.info(f"Generated {len(clean_alt_texts)} alt text options")
            return result
            
        except Exception as e:
            logger.error(f"Error generating alt text: {str(e)}")
            return {"error": str(e)}
    
    def batch_analyze_images(self, image_batch: list) -> Dict[str, Any]:
        """
        Analyze multiple images in batch
        
        Args:
            image_batch: List of dicts containing image info
                        [{"source": "url/path/base64", "type": "url/path/base64", "name": "optional"}]
            
        Returns:
            Dict containing batch analysis results
        """
        try:
            results = {}
            errors = []
            
            for i, image_info in enumerate(image_batch):
                try:
                    source = image_info.get("source")
                    source_type = image_info.get("type", "url")
                    name = image_info.get("name", f"image_{i}")
                    
                    analysis = self.analyze_product_image(source, source_type)
                    results[name] = analysis
                    
                except Exception as e:
                    error_info = {
                        "image": image_info.get("name", f"image_{i}"),
                        "error": str(e)
                    }
                    errors.append(error_info)
                    logger.error(f"Error processing image {i}: {str(e)}")
            
            batch_result = {
                "results": results,
                "errors": errors,
                "processed": len(results),
                "failed": len(errors),
                "total": len(image_batch),
                "generated_at": "2025-08-14T19:18:38Z"
            }
            
            logger.info(f"Batch processed: {len(results)}/{len(image_batch)} images")
            return batch_result
            
        except Exception as e:
            logger.error(f"Error in batch analysis: {str(e)}")
            return {"error": str(e)}
