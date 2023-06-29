

import constant.defs as defs
from infrastructure.logwrapper import LogWrapper
from script import generate_youtube_prompt,get_youtube_info,generate_script,generate_image_prompt,process_response,save_to_csv,read_from_csv,create_dataframe
import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
import logging
import os
import sys
import requests
import urllib.request
from tkinter import PhotoImage
from PIL import Image, ImageTk
from io import BytesIO
import pandas as pd 
import logging
import os
from api_key import key
import threading


LOG_FORMAT = "%(asctime)s\t\t%(message)s"
DEFAULT_LEVEL = logging.DEBUG
LOG_PATH = './logs'
mode = ["Light", "Dark", "System"]
scaling = ["80%", "90%", "100%", "110%", "120%"]
system_prompt = defs.SYSTEM_PROMPT

# class LogWrapper:

#     PATH = './logs'

#     def __init__(self,name, mode="w"):
#         self.create_directory()
#         self.filename = f"{LogWrapper.PATH}/{name}.log"
#         self.logger = logging.getLogger(name)
#         self.logger.setLevel(DEFAULT_LEVEL)

#         file_handler = logging.FileHandler(self.filename, mode=mode)
#         formatter =  logging.Formatter(LOG_FORMAT,datefmt='%Y-%m-%d %H:%M:%S')

#         file_handler.setFormatter(formatter)
#         self.logger.addHandler(file_handler)

#         self.logger.info(f"LogWrapper init() {self.filename}")


#     def create_directory(self):
#         if not os.path.exists(LogWrapper.PATH):
#             os.makedirs(LogWrapper.PATH)
class TextHandler(logging.Handler):
    def __init__(self, textbox):
        logging.Handler.__init__(self)
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        self.textbox.configure(state='normal')
        self.textbox.insert(tk.END, msg + "\n")
        self.textbox.configure(state='disabled')
        self.textbox.see(tk.END)

DEFAULT_LEVEL = logging.DEBUG
class OpenAIGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")

        self.title('Divine Artistry AI')
        self.geometry("1100x700")
        self.resizable(True, True)

        self._create_widgets()
        self._configure_layout()
        self._create_logger()
    
    def _create_widgets(self):
        # create sidebar frame with widgets
        self.sidebar_frame = ctk.CTkFrame(self, width=140, corner_radius=0)


        # create tabview
        self.tabview = ctk.CTkTabview(self, width=300)
        self.tabview.add("script")
        self.tabview.add("audio")
        self.tabview.add("video")
        self.tabview.add("Midjourney")


    
        self.prompt_entry = ctk.CTkTextbox(
            self.tabview.tab('script'), width=250, height=100)

        self.textbox = ctk.CTkTextbox(
            self, width=250, height=200, state="disabled")
        # GUI LABEL
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, text="Divine Artistry AI", font=ctk.CTkFont(size=20, weight="bold"))
        # GUI Button
        self.generate_button = ctk.CTkButton(
            self.tabview.tab('script'), text="Generate Script", command=self.generate_response)

        self.quit_button = ctk.CTkButton(
            self.sidebar_frame, text="Quit app", command=self.quit_app, fg_color='Red')

        # Window customization
        self.appearance_mode_label = ctk.CTkLabel(
            self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=9, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=mode, command=self.change_appearance_mode_event)

        self.scaling_label = ctk.CTkLabel(
            self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=11, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = ctk.CTkOptionMenu(
            self.sidebar_frame, values=scaling, command=self.change_scaling_event)

        self.generate_button.bind("<Return>", self.generate_response)
        self.quit_button.bind("<Escape>", self.quit_app)

    def _configure_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.logo_label.grid(row=0, column=0, padx=20, pady=20, sticky='n')
        # Tab view
        self.tabview.tab("script").grid_columnconfigure(
            1, weight=5)  # configure grid of individual tabs
        self.tabview.tab("audio").grid_columnconfigure(1, weight=5)
        self.tabview.tab("video").grid_columnconfigure(1, weight=5)
        self.tabview.tab("Midjourney").grid_columnconfigure(1, weight=5)
        self.tabview.grid(row=0, column=1, padx=20, pady=20, sticky="n")
        # Sidebar
        self.sidebar_frame.grid(row=0, column=0, rowspan=7, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(7, weight=1)


        self.scaling_optionemenu.grid(row=12, column=0, sticky="n")
        self.appearance_mode_optionemenu.grid(
            row=10, column=0)
        # Main bar
        self.prompt_entry.grid(row=0, column=2, padx=(
            25, 25), pady=(25, 0),  sticky="new")
        self.generate_button.grid(row=1, column=2, padx=20, pady=20)
        self.textbox.grid(row=1, column=1, padx=(
            5, 5), pady=(5, 5), sticky="nsew")
        self.quit_button.grid(row=13, column=0, padx=20, pady=10)
    
    def _create_logger(self):
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        self.logger = logging.getLogger('OpenAIGUI')
        self.logger.setLevel(DEFAULT_LEVEL)
        
        file_handler = logging.FileHandler(f"{LOG_PATH}/OpenAIGUI.log")
        formatter =  logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        text_handler = TextHandler(self.textbox)
        text_handler.setFormatter(formatter)
        self.logger.addHandler(text_handler)

    def long_running_function(self):
        try:  # Start of try block to catch exceptions
            idea = self.prompt_entry.get("1.0", "end")
            self.logger.info(f"Your TOPIC : {idea}")
            self.logger.info(f"----------------------------")
            self.logger.info(f"- Script Processor : Started")
            
            self.logger.info(f"- Script Processor : Input Topic Loaded Successfully")
            prompt = generate_youtube_prompt(idea,self.logger)
            response = get_youtube_info(system_prompt, prompt,self.logger)
            df = process_response(response,self.logger)
            df['Script'] = generate_script(idea,self.logger)
            save_to_csv(df,'youtube_content.csv',self.logger)
            read_df = read_from_csv('youtube_content.csv',self.logger)

            dataframes = []
            for i in range(0, len(read_df)):
                temp_df = create_dataframe(read_df, i)
                if temp_df is not None:
                    dataframes.append(temp_df)

            result_df = pd.concat(dataframes, ignore_index=True) if dataframes else print(
                "No data to create a DataFrame.")
            result_df['Prompt'] = result_df['Image Ideas'].apply(generate_image_prompt)
            result_df = result_df.applymap(lambda x: x.lstrip('prompt: ') if isinstance(x, str) else x)
            result_df = result_df.applymap(lambda x: x.lstrip('prompt : ') if isinstance(x, str) else x)
            result_df['Prompt'] = result_df['Prompt'].str.replace('\n', "")
            result_df['Prompt'] = result_df['Prompt'].str.replace('"', '')
            result_df['Prompt'] = result_df['Prompt'].str.replace('.', '')
            result_df['Prompt'] = result_df['Prompt'] + " --stylize 1000 --ar 9:16 --v 5"
            save_to_csv(result_df,'midjournry_prompt.csv',self.logger)
            self.logger.info(f"- Script Processor : Compeleted")
            self.logger.info(f"----------------------------")
        except Exception as e:  # Catch all exceptions
            self.logger.error(f"Error in generate_response: {str(e)}")  # Log the error message

    def generate_response(self):
        threading.Thread(target=self.long_running_function).start()


    def change_appearance_mode_event(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        ctk.set_widget_scaling(new_scaling_float)



    def clear_prompt(self):
        self.prompt_entry.delete(0, tk.END)
        self.textbox.delete(0, tk.END)

    def quit_app(self):
        self.destroy()
    


if __name__ == '__main__':
    app = OpenAIGUI()
    app.mainloop()