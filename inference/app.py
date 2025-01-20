import streamlit as st
import pandas as pd
import joblib
import json
import os

from streamlit_searchbox import st_searchbox

base_dir = os.path.dirname(os.path.abspath(__file__)) 
model_dir = os.path.join(base_dir, '../model')

base_dataset = pd.read_csv(os.path.join(base_dir, '../dataset/anime.csv'))
# Made by mdavap
class Model:
    def __init__(self, type):
        self.base_path =  os.path.join(model_dir, type)
        self.files = os.listdir(self.base_path)

        self.binary = {}

        for file in self.files:
            file_name, file_extension = os.path.splitext(os.path.join(self.base_path, file))
            clean_file_name = os.path.basename(file_name)
            file_name = file_name + file_extension
            if file_extension == '.joblib':
                self.binary[clean_file_name] = joblib.load(file_name)
            else:
                with open(file_name, 'r') as file:
                    self.binary[clean_file_name] = json.load(file)

    def predict(self, input):
        model = [value for key, value in self.binary.items() if not 'encoder' in key][1]
        print(model)
        return model.predict(input)[0]
    
    def encode(self, input):
        for key, encoder in self.binary.items():
            if 'encoder' in key:
                column = key.split('_encoder')[0]
                target_column = input[column]
                input[column] = encoder.transform(target_column)
    
    def get_order(self):
        return self.binary['columns']


st.set_page_config('AniSuccess')
st.title('AniSuccess Capstone Project (mdavap)')

classification = Model('classification')
regression = Model('regression')


tab1, tab2 = st.tabs(["Predict Existing Anime", "Predict New Anime"])

with tab1:
    # Optimizaton for speed
    anime_titles = base_dataset['title'].tolist()

    def search_anime(searchterm: str) -> list:
        if not searchterm:
            return []
        
        searchterm = searchterm.lower()
        return [title for title in anime_titles if searchterm in title.lower()]

    selected_value = st_searchbox(
        search_anime,
        placeholder="Search Anime"
    )

    if selected_value:
        target_anime = base_dataset[base_dataset['title'] == selected_value].iloc[0]
        
        # Classification
        input_classification = {}
        for column in classification.get_order():
            input_classification[column] = 0

        for column in target_anime.keys():
            value = target_anime[column]

            if column in input_classification:
                # Fill in
                input_classification[column] = value
            elif column == 'studios' or column == 'genres':
                # One hot encoding studios or genres
                splitted = value.split(';')
                for key in splitted:
                    input_classification[key] = 1
        
        input_classification = pd.DataFrame([input_classification])

        # Label encoding
        classification.encode(input_classification)
        result_classification = classification.predict(input_classification)

        # Regression
        input_regression = {}
        for column in regression.get_order():
            input_regression[column] = 0

        for column in target_anime.keys():
            value = target_anime[column]

            if column in input_regression:
                # Fill in
                input_regression[column] = value
            elif column == 'studios' or column == 'genres':
                # One hot encoding studios or genres
                splitted = value.split(';')
                for key in splitted:
                    input_regression[key] = 1
                    
        input_regression = pd.DataFrame([input_regression])

        # Label encoding
        regression.encode(input_regression)
        result_regression = regression.predict(input_regression)

        st.markdown(f"""
                    # Prediction Result
                        - Success: {'Yes' if result_classification else 'No'}
                        - Score: {result_regression}
                    """)
