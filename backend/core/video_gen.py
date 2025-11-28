import google.generativeai as genai
from google.generativeai import types
import os
import base64
import time

class VideoGenerator:
    def __init__(self):
        # Initialize Gemini for Veo video generation
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.has_api_key = True
        else:
            self.has_api_key = False

    def generate(self, prompt: str, duration: int = 8, aspect_ratio: str = "16:9", 
                 reference_image: bytes = None) -> dict:
        """
        Generates a video using Google Veo 3.1.
        
        Args:
            prompt: Text description of the video
            duration: Video duration in seconds (default: 8)
            aspect_ratio: Video aspect ratio - "16:9", "9:16", "1:1", "4:3", "3:4" (default: "16:9")
            reference_image: Optional reference image bytes for image-to-video generation
        
        Returns:
            dict with 'operation_id' and 'status'
        """
        if not self.has_api_key:
            return {"error": "Gemini API key not configured"}
        
        try:
            print(f"🎬 Generating video with Google Veo 3.1...")
            print(f"   Prompt: {prompt}")
            print(f"   Duration: {duration}s")
            print(f"   Aspect Ratio: {aspect_ratio}")
            
            # Prepare config
            config = {
                "aspect_ratio": aspect_ratio,
                "person_generation": "allow_adult"
            }
            
            # Add reference image if provided
            if reference_image:
                config["reference_images"] = [reference_image]
            
            # Generate video using Veo 3.1 API
            operation = genai.Client().models.generate_videos(
                model="veo-3.1-generate-preview",
                prompt=prompt,
                config=config
            )
            
            print(f"✅ Video generation started!")
            print(f"   Operation ID: {operation.name}")
            print(f"   This may take a few minutes...")
            
            return {
                "operation_id": operation.name,
                "status": "processing",
                "message": "Video generation in progress. Use check_video_status() to monitor."
            }
                
        except Exception as e:
            print(f"❌ Google Veo failed: {e}")
            return {"error": str(e)}
    
    def check_status(self, operation_id: str) -> dict:
        """
        Check the status of a video generation operation.
        
        Args:
            operation_id: The operation ID returned from generate()
        
        Returns:
            dict with 'status', 'progress', and 'video_url' (if complete)
        """
        if not self.has_api_key:
            return {"error": "Gemini API key not configured"}
        
        try:
            # Get operation status
            operation = genai.Client().operations.get(operation_id)
            
            if operation.done:
                # Video is ready
                if operation.response:
                    video_data = operation.response.generated_videos[0]
                    
                    # Convert to base64 data URL
                    video_bytes = video_data.video
                    video_str = base64.b64encode(video_bytes).decode()
                    
                    print(f"✅ Video generation complete!")
                    
                    return {
                        "status": "complete",
                        "video_url": f"data:video/mp4;base64,{video_str}",
                        "duration": len(video_bytes) / (1024 * 1024)  # Size in MB
                    }
                else:
                    return {"status": "failed", "error": "No video in response"}
            else:
                # Still processing
                progress = getattr(operation.metadata, 'progress_percent', 0) if hasattr(operation, 'metadata') else 0
                
                return {
                    "status": "processing",
                    "progress": progress,
                    "message": f"Video generation {progress}% complete"
                }
                
        except Exception as e:
            print(f"❌ Status check failed: {e}")
            return {"error": str(e)}

video_gen = VideoGenerator()
