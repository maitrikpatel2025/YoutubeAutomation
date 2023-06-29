from googletrans import Translator
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

def save_to_csv(df,filepath):
    try:
        if df.empty:
            raise ValueError("The DataFrame is empty.")
            
        df.to_csv(filepath, index=False)
        print("Data saved successfully.")
        
    except FileNotFoundError as e:
        print(f"An error occurred while trying to save the file: {e}")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def english_to_hindi(text):
    translator = Translator(service_urls=['translate.google.com'])
    try:
        translation = translator.translate(text, src='en', dest='hi')
        return translation.text
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


read_df = read_from_csv('youtube_info.csv')

# Example usage

try:
    read_df["Hindi Script"] = read_df['Script'].apply(english_to_hindi)
    save_to_csv(read_df,'youtube_info.csv')
    if read_df["Hindi Script"][0]:
        print("Hindi translation:", read_df["Hindi Script"][0])
    else:
        print("Failed to translate the text.")
except Exception as e:
    print(f"An error occurred: {e}")
