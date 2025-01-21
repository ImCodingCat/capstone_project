import streamlit as st
import pandas as pd
import joblib
import json
import os

base_dir = os.path.dirname(os.path.abspath(__file__)) 
model_dir = os.path.join(base_dir, '../model')
cache_path = os.path.join(base_dir, 'cache.json') # Containing genre list and studio list

base_dataset = pd.read_csv(os.path.join(base_dir, '../dataset/anime.csv'))

with open(cache_path, 'r') as file:
    cache_json = json.load(file)
    genre_list = cache_json[0]
    studio_list = cache_json[1]


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
        for key, model in self.binary.items():
            if not 'encoder' in key and not 'columns' in key:
                return model.predict(input)[0]
        return 0
    
    def encode(self, input):
        for key, encoder in self.binary.items():
            if 'encoder' in key:
                column = key.split('_encoder')[0]
                target_column = input[column]
                input[column] = encoder.transform(target_column)

    def get_categorical(self):
        categorical = {}
        for key, encoder in self.binary.items():
            if 'encoder' in key:
                column = key.split('_encoder')[0]
                classes = encoder.classes_
                categorical[column] = classes

        return categorical

    
    def get_order(self):
        return self.binary['columns']


st.set_page_config('AniSuccess', "👍")
st.title('AniSuccess Capstone Project (mdavap)')

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

classification = Model('classification')
regression = Model('regression')


tab1, tab2 = st.tabs(["Predict Existing Anime", "Predict New Anime"])

with tab1:
    st.markdown("# Input existing anime")

    # Optimizaton for speed
    anime_titles = base_dataset['title'].tolist()
    selected_value = st.selectbox('Search Anime', anime_titles)

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

with tab2:
    st.markdown("# Predict new anime")
    
    input_prediction = {}
    categorical_list = classification.get_categorical()
    categorical_list['genres'] = genre_list
    categorical_list['studios'] = studio_list

    col1, col2 = st.columns(2)

    with col1:
        st.text("Please input your categorical value")
        for key, value in categorical_list.items():
            input_prediction[key] = st.selectbox(f'Please input your anime "{key}"', value)

    with col2:
        st.text("Please input your numerical value")
        limit_integer = pow(2, 32) # 32 bit

        input_prediction['episodes'] = st.slider('How many Episodes? ', 0, 100)
        input_prediction['score'] = st.slider('How many do you think you will get score? (leave zero if you dont know)', 0.0, 10.0)
        input_prediction['scored_by'] = st.number_input('How many do you think you will get scoredby? (leave zero if you dont know)', 0, limit_integer)
        input_prediction['popularity'] = st.number_input('How many do you think you will get popularity? (leave zero if you dont know)', 0, limit_integer)
        input_prediction['favorites'] = st.number_input('How many do you think you will get favorites? (leave zero if you dont know)', 0, limit_integer)
        input_prediction['members'] = st.number_input('How many do you think you will get members? (leave zero if you dont know)', 0, limit_integer)

    
    if st.button('Predict'):
        # Classification
        input_classification = {}
        for column in classification.get_order():
            input_classification[column] = 0

        for column in input_prediction.keys():
            value = input_prediction[column]

            if column in input_classification:
                # Fill in
                input_classification[column] = value
            elif column == 'studios' or column == 'genres':
                # One hot encoding studios or genres
                input_classification[value] = 1
        
        input_classification = pd.DataFrame([input_classification])

        # Label encoding
        classification.encode(input_classification)
        result_classification = classification.predict(input_classification)

        # Regression
        input_regression = {}
        for column in regression.get_order():
            input_regression[column] = 0

        for column in input_prediction.keys():
            value = input_prediction[column]

            if column in input_regression:
                # Fill in
                input_regression[column] = value
            elif column == 'studios' or column == 'genres':
                # One hot encoding studios or genres
                input_regression[value] = 1

        input_regression = pd.DataFrame([input_regression])

        # Label encoding
        regression.encode(input_regression)
        result_regression = regression.predict(input_regression)

        st.markdown(f"""
                    # Prediction Result
                        - Success: {'Yes' if result_classification else 'No'}
                        - Score: {result_regression}
                    """)


        
