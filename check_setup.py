import requests
import os
import sys

def check_health():
    try:
        # Check if Ollama is running and model is available
        import ollama
        client = ollama.Client()
        models = client.list()
        
        # Handle different response formats
        model_list = []
        if hasattr(models, 'models'):
            model_list = models.models
        elif isinstance(models, dict) and 'models' in models:
            model_list = models['models']
        else:
            model_list = models if isinstance(models, list) else []
            
        model_names = []
        for m in model_list:
            if hasattr(m, 'model'):
                model_names.append(m.model)
            elif isinstance(m, dict):
                model_names.append(m.get('name', '') or m.get('model', ''))
            else:
                model_names.append(str(m))
        
        target_model = "qwen2.5-coder:3b"
        if any(target_model in name for name in model_names):
            print(f"✅ Model found: {target_model}")
        else:
            print(f"❌ Model {target_model} NOT found in Ollama list: {model_names}")
            
        # Check imports
        import google.generativeai
        print("✅ google-generativeai installed")
        
        print("✅ Setup verification complete!")
        
    except Exception as e:
        print(f"❌ Setup verification failed: {e}")

if __name__ == "__main__":
    check_health()
