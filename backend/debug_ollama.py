import ollama
import json

try:
    client = ollama.Client(host='http://localhost:11434')
    models = client.list()
    print(f"Type: {type(models)}")
    print(f"Raw: {models}")
    
    if hasattr(models, 'models'):
        print("Has .models attribute")
        for m in models.models:
            print(f"Model: {m.model}")
            
except Exception as e:
    print(f"Error: {e}")
