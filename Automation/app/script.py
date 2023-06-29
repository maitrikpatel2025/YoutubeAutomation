import openai
import pandas as pd
import re
import time
import pandas as pd
import constant.defs as defs


def generate_youtube_prompt(idea,logger):
    logger.info(f"- Script Processor :  Input System Prompt Written Successfully")
    prompt = f"""
    Create a catchy title with relevant keywords and impactful words to enhance the click-through rate of the video. I'll provide you with the topic, and your task is to generate one compelling YouTube title for me.

    Following the title, write a 100-word SEO-optimized YouTube video description that won't be flagged by AI. The chosen keyword should be used in the first sentence of the description.

    Next, create 10 SEO-optimized hashtags. These should be in lowercase and without any spaces. Additionally, generate 35 SEO-optimized tags related to the video title. These tags should also be in lowercase and without spaces, separated by commas.

    Finally, conceptualize six creative image ideas based on the description. The images should be informative, detailed, and artistically modern. They should include elements of the cosmos like nebulas, stars, and galaxies in the background. The primary objective is to inspire and educate the audience while fostering a deeper appreciation of the context.
    Topic: {idea}
    Please adhere to the following structure and formatting:
    YOUTUBE TITLE:
    YOUTUBE DESCRIPTION:
    YOUTUBE HASTAGS:
    YOUTUBE TAGS:
    YOUTUBE IMAGES:
    1.
    2.
    3.
    4.
    5.
    6.

    The task needs to be completed in the English language.


    And when you are finished always display ‘I AM DONE WRITING’
    """
    logger.info(f"- Script Processor :  Input Prompt Written Successfully")
    return prompt

def process_response(response,logger):
    logger.info(f"- Script Processor :  Clean API Response")
    try:
        logger.info(f"- Script Processor :  Split The Text")
        text = response.replace("I AM DONE WRITING.", "")
        sections = re.split('YOUTUBE (.*?):', text)

        # Remove leading and trailing whitespaces
        # Create a dictionary with the section titles as keys and content as values
        content_dict = {sections[i]: sections[i + 1]
                        for i in range(1, len(sections)-1, 2)}

        # Convert the dictionary to a DataFrame
        df = pd.DataFrame([content_dict], columns=content_dict.keys())
        logger.info(f"- Script Processor :  Dictionary to a DataFrame")
        df.columns = ['Title', 'Description',
                      'Hastags', 'Tags', 'Image Ideas']
        logger.info(f"- Script Processor :  Output Title Description Hastags Tags Image Ideas Written Successfully")
        return df
    except Exception as e:
        logger.info(f"- Script Processor :  An error occurred: {e}")


def get_youtube_info(system_prompt, prompt,logger):
    logger.info(f"- Script Processor :  Starting API Connection Process.")
    try:
        logger.info(f"- Script Processor :  Loading API Credentials.")
        completion = openai.Completion.create(
            model="text-davinci-003",
            prompt=system_prompt + "\n" + prompt,
            temperature=0.7,
            max_tokens=3000,
            top_p=1,
        )

        if not completion:
            logger.info(f"- Script Processor :  Error: No Response from API.")
            raise ValueError("No response from the AI model.")
        
        response = completion.choices[0].text.strip()

        if not response or response == "I AM DONE WRITING.":
            logger.info(f"- Script Processor :  Error: Response from API is empty or incomplete.")
            raise ValueError("The AI model response is empty or incomplete.")
        
        logger.info(f"- Script Processor :  API Test Request Successful, Response Code: 200")
        logger.info(f"- Script Processor :  Output API Response Written Successfully")
        return response

    except Exception as e:
        logger.info(f"- Script Processor :  An error occurred: {str(e)}")


def generate_script(idea,logger):
    logger.info(f"- Script Processor :  Writing Out Script.")
    script= f"""
    Create a short, engaging voice-over script for a video on platforms like TikTok, or Instagram Reels. The script should begin with "Hello everyone" and tell an entertaining story based on a surprising, yet little-known scientific fact or statistic that has had a significant impact. 
    DON'T MAKE ME REPEAT MYSELF. I NEED A SCRIPT THAT'S MORE THAN 200 WORDS BUT LESS THAN 240 WORDS and be suitable for a general audience. Consider starting with a captivating introduction to grab the viewers' attention.
    Include the surprising scientific fact or statistic early on in the script. Add elements of curiosity and suspense to keep the audience engaged.
    Incorporate storytelling techniques to make the script more relatable and entertaining. Use simple language and avoid jargon to ensure accessibility.
    Focus on the impact of the scientific fact or statistic to emphasize its significance. Keep the script concise and avoid unnecessary details or tangents or shot details .
    {idea} 
    """
    system_prompt = defs.SYSTEM_PROMPT
    logger.info(f"- Script Processor :  Starting API Connection Process.")
    try:
        logger.info(f"- Script Processor :  Loading API Credentials.")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= system_prompt + "\n" + script,
            temperature=0.7,
            max_tokens=1500,
            top_p=1,
        )
        api_response = response.choices[0].text
        logger.info(f"- Script Processor :  API Test Request Successful, Response Code: 200")
        logger.info(f"- Script Processor :  Output API Response Written Successfully")
        return api_response
    except openai.error.RateLimitError:
        # Handle the rate limit error
        logger.info(f"- Script Processor :  API Rate limit exceeded. Retrying in 60 seconds...")
        time.sleep(60)  # Wait for 60 seconds
        return generate_script(idea)
    except openai.error.OpenAIError as e:
        # Handle other OpenAI errors
        logger.info(f"- Script Processor :  An error occurred: {e}")
        return None


def read_from_csv(file_path,logger):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            logger.info(f"- Script Processor :  Warning: The CSV file is empty.")
        logger.info(f"- Script Processor :  Read {file_path} Successfully")
        return df

    except FileNotFoundError as e:
        logger.info(f"- Script Processor :  An error occurred while trying to read the file: {e}")
        return None

    except pd.errors.EmptyDataError as e:
        logger.info(f"- Script Processor :  No data: {e}")
        return None

    except Exception as e:
        logger.info(f"- Script Processor :  An unexpected error occurred: {e}")
        return None


def save_to_csv(df, filepath,logger):
    try:
        if df.empty:
            logger.info(f"- Script Processor :  The DataFrame is empty.")
            raise ValueError("The DataFrame is empty.")

        df.to_csv(filepath, index=False)
        logger.info(f"- Script Processor :  {filepath} Data saved successfully.")

    except FileNotFoundError as e:
        logger.info(f"- Script Processor :  An error occurred while trying to save the file: {e}")

    except Exception as e:
        logger.info(f"- Script Processor :  An unexpected error occurred: {e}")

def create_dataframe(df, index):
    try:
        data = df['Image Ideas'][index]
        data = data.strip()
        list_items = re.split(r'\d+\.', data)

        list_items = [item.strip() for item in list_items if item.strip()]

        if not list_items:
            print(
                f"Warning: No valid 'Image Idea' data found for index {index}.")
            return None

        title = df['Title'][index]
        temp_df = pd.DataFrame(
            {'Title': [title]*len(list_items), 'Image Ideas': list_items})
        return temp_df

    except KeyError as e:
        print(f"An error occurred: {e}")
        return None

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def generate_image_prompt(description):
    system_prompt = defs.SYSTEM_PROMPT
    
    midjourney_prompt = f"""

    Your task is to create a single image prompt for a generative AI titled "Midjourney". This prompt will provide the AI with specific details to generate an image. They should include elements of the cosmos like nebulas, stars, and galaxies in the background. Here are the necessary steps and guidelines:
    {description}
    Avoid using the words "description" or ":" in any context.
    Each prompt must be written in a single line without pressing return.
    Prompt Components:
    [1] = An initial idea or concept
    [2] = An in-depth elaboration of [1] with specific imagery details
    [3] = A detailed account of the scene's environment
    [4] = An insightful description of the scene's mood, feelings, and atmosphere
    [5] = The style for [1] from the list: Photography, Illustration, watercolor, oil painting, comics, cinematic, 3D , digital illustration
    [6] = A description of how [5] will be executed, such as camera model and settings, painting materials, rendering engine settings, etc.

    Please adhere to the following structure and formatting:
    PROMPT:
    """
 
    try:
 
        midjourney_prompt_api = openai.Completion.create(
            model="text-davinci-003",
            prompt=system_prompt + "\n" + midjourney_prompt,
            temperature=0.7,
            max_tokens=1500,
            top_p=1,
        )
        midjourney_prompt_api_response = midjourney_prompt_api.choices[0].text
 
        return midjourney_prompt_api_response
    except openai.error.RateLimitError:
        # Handle the rate limit error
        print(f"- Script Processor :  API Rate limit exceeded. Retrying in 60 seconds...")
        time.sleep(60)  # Wait for 60 seconds
        return generate_image_prompt(description)
    except openai.error.OpenAIError as e:
        # Handle other OpenAI errors
        print(f"- Script Processor :  An error occurred: {e}")
        return None































# openai.api_key = "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"

# idea = input(f"your idea:")

# system_prompt = f""" 
# As an experienced YouTuber, keyword specialist, and copywriter with a deep understanding of Hindu mythology and various scientific fields, I will help you create engaging and relevant content that explores the intersection of these realms.

# We will delve into the symbolism embedded in the narratives of deities such as Brahma, Vishnu, Shiva, Lakshmi, and others, and the philosophical wisdom encapsulated in ancient scriptures like the Vedas, Upanishads, Bhagavad Gita, Ramayana, Mahabharata, and Puranas. Together, we will draw meaningful connections to modern scientific principles, incorporating scientific theories and hypotheses that might be intertwined with ancient Hindu texts.

# Keeping in mind YouTube's algorithm, here's a general approach to our narrative:

# User Engagement: We'll create captivating, curiosity-sparking content that encourages viewers to watch, like, comment, and share our videos. This engagement can help improve our algorithmic performance.

# Relevance: Our videos will be carefully curated to match the interests of our target audience, especially those intrigued by Hindu mythology and scientific fields.

# Personalization: We'll leverage machine learning capabilities to better understand our viewers' preferences and tailor our content to their interests.

# Retention and Completion Rate: We'll maintain a narrative that holds our viewers' interest, thereby increasing the chances of video completion and enhancing our retention rates.

# Recency: While we will strive to keep our content fresh and regularly updated, we'll also ensure that our timeless interpretations of ancient wisdom remain accessible and appealing.

# Creator Performance: Our track record of creating engaging and informative content will likely increase our chances of being recommended by the algorithm.

# Video Metadata: We'll incorporate accurate and relevant titles, descriptions, and tags to our videos to ensure they reach the right audience.

# In this way, we'll seamlessly weave together threads of ancient Hindu wisdom and modern scientific knowledge, creating a compelling narrative tapestry that engages, informs, and delights our viewers.
# """

# prompt = f"""
# Create a catchy title with relevant keywords and impactful words to enhance the click-through rate of the video. I'll provide you with the topic, and your task is to generate one compelling YouTube title for me.

# Following the title, write a 100-word SEO-optimized YouTube video description that won't be flagged by AI. The chosen keyword should be used in the first sentence of the description.

# Next, create 10 SEO-optimized hashtags. These should be in lowercase and without any spaces. Additionally, generate 35 SEO-optimized tags related to the video title. These tags should also be in lowercase and without spaces, separated by commas.

# Finally, conceptualize six creative image ideas based on the description. The images should be informative, detailed, and artistically modern. They should include elements of the cosmos like nebulas, stars, and galaxies in the background. The primary objective is to inspire and educate the audience while fostering a deeper appreciation of the context.
# Topic: {idea}
# Please adhere to the following structure and formatting:
# YOUTUBE TITLE:
# YOUTUBE DESCRIPTION:
# YOUTUBE HASTAGS:
# YOUTUBE TAGS:
# YOUTUBE IMAGES:
# 1.
# 2.
# 3.
# 4.
# 5.
# 6.

# The task needs to be completed in the English language.


# And when you are finished always display‘I AM DONE WRITING’
# """


# def generate_youtube_prompt(idea):
#     prompt = f"""
#     Create a catchy title with relevant keywords and impactful words to enhance the click-through rate of the video. I'll provide you with the topic, and your task is to generate one compelling YouTube title for me.

#     Following the title, write a 100-word SEO-optimized YouTube video description that won't be flagged by AI. The chosen keyword should be used in the first sentence of the description.

#     Next, create 10 SEO-optimized hashtags. These should be in lowercase and without any spaces. Additionally, generate 35 SEO-optimized tags related to the video title. These tags should also be in lowercase and without spaces, separated by commas.

#     Finally, conceptualize six creative image ideas based on the description. The images should be informative, detailed, and artistically modern. They should include elements of the cosmos like nebulas, stars, and galaxies in the background. The primary objective is to inspire and educate the audience while fostering a deeper appreciation of the context.
#     Topic: {idea}
#     Please adhere to the following structure and formatting:
#     YOUTUBE TITLE:
#     YOUTUBE DESCRIPTION:
#     YOUTUBE HASTAGS:
#     YOUTUBE TAGS:
#     YOUTUBE IMAGES:
#     1.
#     2.
#     3.
#     4.
#     5.
#     6.

#     The task needs to be completed in the English language.


#     And when you are finished always display ‘I AM DONE WRITING’
#     """
#     return prompt

# def process_response(response):
#     try:
#         text = response.replace("I AM DONE WRITING.", "")
#         sections = re.split('YOUTUBE (.*?):', text)

#         # Remove leading and trailing whitespaces
#         # Create a dictionary with the section titles as keys and content as values
#         content_dict = {sections[i]: sections[i + 1]
#                         for i in range(1, len(sections)-1, 2)}

#         # Convert the dictionary to a DataFrame
#         df = pd.DataFrame([content_dict], columns=content_dict.keys())

#         df.columns = ['Title', 'Description',
#                       'Hastag', 'Tags', 'Image Ideas']
#         return df
#     except Exception as e:
#         print(f"An error occurred: {e}")


# def get_youtube_info(system_prompt, prompt):
#     try:
#         completion = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=system_prompt + "\n" + prompt,
#             temperature=0.7,
#             max_tokens=3000,
#             top_p=1,
#         )

#         if not completion:
#             raise ValueError("No response from the AI model.")

#         response = completion.choices[0].text.strip()

#         if not response or response == "I AM DONE WRITING.":
#             raise ValueError("The AI model response is empty or incomplete.")
#         return response

#     except Exception as e:
#         print(f"An error occurred: {e}")


# def generate_script(idea):
#     script= f"""
#     Create a short, engaging voice-over script for a video on platforms like TikTok, or Instagram Reels. The script should begin with "Hello everyone" and tell an entertaining story based on a surprising, yet little-known scientific fact or statistic that has had a significant impact. 
#     DON'T MAKE ME REPEAT MYSELF. I NEED A SCRIPT THAT'S MORE THAN 200 WORDS BUT LESS THAN 240 WORDS and be suitable for a general audience. Consider starting with a captivating introduction to grab the viewers' attention.
#     Include the surprising scientific fact or statistic early on in the script. Add elements of curiosity and suspense to keep the audience engaged.
#     Incorporate storytelling techniques to make the script more relatable and entertaining. Use simple language and avoid jargon to ensure accessibility.
#     Focus on the impact of the scientific fact or statistic to emphasize its significance. Keep the script concise and avoid unnecessary details or tangents or shot details .
#     {idea} 
#     """
#     system_prompt = defs.SYSTEM_PROMPT
#     try:
#         midjourney_prompt_api = openai.Completion.create(
#             model="text-davinci-003",
#             prompt= system_prompt + "\n" + script,
#             temperature=0.7,
#             max_tokens=1500,
#             top_p=1,
#         )
#         midjourney_prompt_api_response = midjourney_prompt_api.choices[0].text

#         return midjourney_prompt_api_response
#     except openai.error.RateLimitError:
#         # Handle the rate limit error
#         print("Rate limit exceeded. Retrying in 60 seconds...")
#         time.sleep(60)  # Wait for 60 seconds
#         return generate_image_prompt(idea)
#     except openai.error.OpenAIError as e:
#         # Handle other OpenAI errors
#         print(f"An error occurred: {e}")
#         return None


# def read_from_csv(file_path):
#     try:
#         df = pd.read_csv(file_path)
#         if df.empty:
#             print("Warning: The CSV file is empty.")
#         return df

#     except FileNotFoundError as e:
#         print(f"An error occurred while trying to read the file: {e}")
#         return None

#     except pd.errors.EmptyDataError as e:
#         print(f"No data: {e}")
#         return None

#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return None


# def save_to_csv(df, filepath):
#     try:
#         if df.empty:
#             raise ValueError("The DataFrame is empty.")

#         df.to_csv(filepath, index=False)
#         print("Data saved successfully.")

#     except FileNotFoundError as e:
#         print(f"An error occurred while trying to save the file: {e}")

#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")


# def english_to_hindi(text):
#     translator = Translator(service_urls=['translate.google.com'])
#     try:
#         translation = translator.translate(text, src='en', dest='hi')
#         return translation.text
#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return None

# prompt = generate_youtube_prompt(idea)
# # Use the function
# response = get_youtube_info(system_prompt,prompt)
# print(response)
# print("\n\n\n")
# df = process_response(response)
# df['Script'] = generate_script(idea)
# df["Hindi Script"] = df['Script'].apply(english_to_hindi)
# # df.to_csv('youtube_info.csv', index=False)
# save_to_csv(df,'youtube_info.csv')
# read_df = read_from_csv('youtube_info.csv')


# def create_dataframe(df, index):
#     try:
#         data = df['Image Ideas'][index]
#         data = data.strip()
#         list_items = re.split(r'\d+\.', data)

#         list_items = [item.strip() for item in list_items if item.strip()]

#         if not list_items:
#             print(
#                 f"Warning: No valid 'Image Idea' data found for index {index}.")
#             return None

#         title = df['Title'][index]
#         temp_df = pd.DataFrame(
#             {'Title': [title]*len(list_items), 'Image Ideas': list_items})
#         return temp_df

#     except KeyError as e:
#         print(f"An error occurred: {e}")
#         return None

#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         return None


# dataframes = []

# # Loop through each row of the original DataFrame
# for i in range(0, len(read_df)):
#     # Process the row and append the resulting DataFrame to the list
#     temp_df = create_dataframe(read_df, i)
#     if temp_df is not None:
#         dataframes.append(temp_df)

# # Combine all the DataFrames in the list into a single DataFrame
# result_df = pd.concat(dataframes, ignore_index=True) if dataframes else print(
#     "No data to create a DataFrame.")


# def generate_image_prompt(description):
#     system_prompt = defs.SYSTEM_PROMPT
#     midjourney_prompt = f"""

#     Your task is to create a single image prompt for a generative AI titled "Midjourney". This prompt will provide the AI with specific details to generate an image. They should include elements of the cosmos like nebulas, stars, and galaxies in the background. Here are the necessary steps and guidelines:
#     {description}
#     Avoid using the words "description" or ":" in any context.
#     Each prompt must be written in a single line without pressing return.
#     Prompt Components:
#     [1] = An initial idea or concept
#     [2] = An in-depth elaboration of [1] with specific imagery details
#     [3] = A detailed account of the scene's environment
#     [4] = An insightful description of the scene's mood, feelings, and atmosphere
#     [5] = The style for [1] from the list: Photography, Illustration, watercolor, oil painting, comics, cinematic, 3D , digital illustration
#     [6] = A description of how [5] will be executed, such as camera model and settings, painting materials, rendering engine settings, etc.

#     Please adhere to the following structure and formatting:
#     PROMPT:
#     """
#     try:
#         midjourney_prompt_api = openai.Completion.create(
#             model="text-davinci-003",
#             prompt=system_prompt + "\n" + midjourney_prompt,
#             temperature=0.7,
#             max_tokens=1500,
#             top_p=1,
#         )
#         midjourney_prompt_api_response = midjourney_prompt_api.choices[0].text

#         return midjourney_prompt_api_response
#     except openai.error.RateLimitError:
#         # Handle the rate limit error
#         print("Rate limit exceeded. Retrying in 60 seconds...")
#         time.sleep(60)  # Wait for 60 seconds
#         return generate_image_prompt(description)
#     except openai.error.OpenAIError as e:
#         # Handle other OpenAI errors
#         print(f"An error occurred: {e}")
#         return None


# result_df['Prompt'] = result_df['Image Ideas'].apply(generate_image_prompt)
# result_df = result_df.applymap(lambda x: x.lstrip('prompt: ') if isinstance(x, str) else x)
# result_df = result_df.applymap(lambda x: x.lstrip('prompt : ') if isinstance(x, str) else x)
# result_df['Prompt'] = result_df['Prompt'].str.replace('\n', "")
# result_df['Prompt'] = result_df['Prompt'].str.replace('"', '')
# result_df['Prompt'] = result_df['Prompt'].str.replace('.', '')
# result_df['Prompt'] = result_df['Prompt'] + " --stylize 1000 --ar 9:16 --v 5"
# if not result_df.empty:
#     print(result_df)
# else:
#     print("No data to display.")

# save_to_csv(result_df, 'midjournry_prompt.csv')
