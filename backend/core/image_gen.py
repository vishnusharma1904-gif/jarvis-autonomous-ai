import google.generativeai as genai
import os
import base64
import io
from PIL import Image as PILImage

class ImageGenerator:
    def __init__(self):
        # Initialize Gemini for prompt enhancement AND native image generation
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            # Gemini 2.5 Flash for prompt enhancement
            self.enhancer_model = genai.GenerativeModel('gemini-2.0-flash-exp')
            # Gemini 2.5 Flash Image for actual generation (Nano Banana)
            self.image_model = genai.GenerativeModel('gemini-2.5-flash-image')
        else:
            self.enhancer_model = None
            self.image_model = None

    def enhance_prompt(self, user_prompt: str) -> str:
        """
        Use Gemini AI to enhance the user's prompt for better image generation.
        Transforms simple prompts into detailed, artistic descriptions.
        """
        if not self.enhancer_model:
            return user_prompt
        
        try:
            enhancement_request = f"""Transform this image prompt into a detailed, artistic description suitable for AI image generation.
Add artistic style, lighting, composition details, and atmosphere. Keep it concise but vivid.

User prompt: "{user_prompt}"

Enhanced prompt (ONE sentence, max 150 words):"""
            
            response = self.enhancer_model.generate_content(enhancement_request)
            enhanced = response.text.strip()
            
            print(f"Original: {user_prompt}")
            print(f"Enhanced: {enhanced}")
            
            return enhanced
        except Exception as e:
            print(f"Prompt enhancement failed: {e}")
            return user_prompt

    def generate(self, prompt: str, width: int = 1024, height: int = 1024, 
                 seed: int = None, model: str = "gemini-2.5-flash-image", enhance: bool = True) -> str:
        """
        Generates an image using Gemini 2.5 Flash Image (Nano Banana).
        
        Args:
            prompt: Text description of the image
            width: Image width (default: 1024)
            height: Image height (default: 1024)
            seed: Random seed for reproducibility (optional)
            model: Model variant (default: "gemini-2.5-flash-image")
            enhance: Whether to use AI to enhance the prompt (default: True)
        
        Returns:
            Base64 data URL of the generated image
        """
        if not self.image_model:
            print("⚠️ Gemini API key not configured, using fallback")
            return self._fallback_pollinations(prompt, width, height, seed)
        
        # Enhance prompt with Gemini AI if enabled
        if enhance and self.enhancer_model:
            prompt = self.enhance_prompt(prompt)
        
        try:
            # Generate image using Gemini 2.5 Flash Image
            print(f"🎨 Generating image with Gemini 2.5 Flash Image (Nano Banana)...")
            
            response = self.image_model.generate_content(
                f"Generate an image: {prompt}",
                generation_config=genai.GenerationConfig(
                    # Gemini 2.5 Flash Image specific config
                    temperature=1.0,
                    top_p=0.95,
                    top_k=40,
                    max_output_tokens=8192,
                )
            )
            
            # Extract image from response
            # Gemini 2.5 Flash Image returns image data in the response
            if response.candidates and response.candidates[0].content.parts:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        # Image data is in inline_data
                        image_data = part.inline_data.data
                        mime_type = part.inline_data.mime_type
                        
                        # Convert to base64 data URL
                        img_str = base64.b64encode(image_data).decode()
                        data_url = f"data:{mime_type};base64,{img_str}"
                        
                        print(f"✅ Image generated successfully with Gemini 2.5 Flash Image!")
                        return data_url
            
            # If no image found in response, fallback
            print("⚠️ No image in Gemini response, using fallback")
            return self._fallback_pollinations(prompt, width, height, seed)
                
        except Exception as e:
            print(f"❌ Gemini 2.5 Flash Image failed: {e}")
            print("   Falling back to Pollinations.ai...")
            return self._fallback_pollinations(prompt, width, height, seed)
    
    def _fallback_pollinations(self, prompt: str, width: int, height: int, seed: int = None) -> str:
        """Fallback to Pollinations.ai if Gemini fails."""
        import urllib.parse
        
        encoded_prompt = urllib.parse.quote(prompt)
        
        # Build parameters for high quality
        params = [
            f"width={width}",
            f"height={height}",
            "model=turbo",
            "nologo=true",
            "enhance=true"
        ]
        
        if seed is not None:
            params.append(f"seed={seed}")
        
        param_string = "&".join(params)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?{param_string}"
        
        print(f"✅ Fallback image URL generated with Pollinations")
        return image_url

image_gen = ImageGenerator()
