import json, os, requests
from dotenv import load_dotenv

# API Key
load_dotenv()
API_KEY_INSIGHT = os.getenv("API_KEY_INSIGHT")

# InSight URL
insightResponse = requests.get(f'https://api.nasa.gov/insight_weather/?api_key={API_KEY_INSIGHT}&feedtype=json&ver=1.0')
insightResponse.raise_for_status()
insightData = json.loads(insightResponse.text)
print(insightData)
