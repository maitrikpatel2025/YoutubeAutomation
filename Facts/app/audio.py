import requests
from googletrans import Translator
ELEVENLABS_API_KEY = '7c5bca33e95b173be3ce2a59e2b538ec'

import pandas as pd

def read_from_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            print("Warning: The CSV file is empty.")
        return df
        
    except FileNotFoundError as e:
        print(f"An error occurred while trying to read the file: {e}")
        return None
        
    except pd.errors.EmptyDataError as e:
        print(f"No data: {e}")
        return None
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

read_df = read_from_csv('youtube_content.csv')
print(read_df)
english = read_df['Script'][0]



def translate_to_hindi(text):
    translator = Translator()
    result = translator.translate(text, src='en', dest='hi')
    return result.text


prompt = translate_to_hindi(english)
prompt = read_df['Script'][0]
headers = {
    'accept': 'audio/mpeg',
    'xi-api-key': ELEVENLABS_API_KEY,
    'Content-Type': 'application/json',
}
# Monolingual 
# eleven_multilingual_v1
json_data = {
    'text': prompt,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
    "stability": 1,
    "similarity_boost": 1
    }
}

#ZGp1FpJRAGdjsdTteiux
#xA4RZwBsm7G1ObG9JCAf = hindi
#vxXVT5NGeW0dlVj7IpcI fact
try:
    response = requests.post('https://api.elevenlabs.io/v1/text-to-speech/vxXVT5NGeW0dlVj7IpcI', headers=headers, json=json_data)
    response.raise_for_status()
except requests.exceptions.HTTPError as errh:
    print ("HTTP Error:", errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:", errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:", errt)
except requests.exceptions.RequestException as err:
    print ("Something went wrong", err)

if response.status_code == 200:
    try:
        with open('script_audio_hindi.mp3', 'wb') as f:
            f.write(response.content)
    except IOError as e:
        print(f"Error writing file: {e}")
else:
    print(f"Request failed with status code: {response.status_code}")
