import requests
import json
import os
from datetime import datetime

API_KEY = os.getenv("TOMTOM_API_KEY")
LAT, LON = 28.6273, 77.3725
DATA_FILE = "traffic_data_history.jsonl"

def collect():
    url = f"https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json"
    params = {'key': API_KEY, 'point': f'{LAT},{LON}', 'unit': 'KMPH'}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()['flowSegmentData']
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "current_speed": data['currentSpeed'],
            "free_flow": data['freeFlowSpeed'],
            "confidence": data['confidence']
        }
        
        # Append to the file
        with open(DATA_FILE, "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"Data collected at {entry['timestamp']}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    collect()