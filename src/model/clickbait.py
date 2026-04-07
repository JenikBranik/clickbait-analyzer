import pickle
import pandas as pd
import warnings
from pathlib import Path


class Clickbait:
    def __init__(self):
        self._binaries_dir = Path(__file__).resolve().parent.parent / 'data'
        self._ml_dir = Path(__file__).resolve().parent / 'ml'
        self.buzzwords = ['děsivé ','peklo', 'otevřeně', 'ukázala', 'slzách', 'drama', 'odhalena', 'přiznání', 'detaily', 'šokující', 'hvězda']
        self.model = None
        self.model_medium = None
        self.label_encoder = None
        self._validate_and_load_models()

    def _validate_and_load_models(self):
        """
        Method for validating paths and loading the serialized Random Forest model.
        :raises FileNotFoundError: if the binaries directory or required files do not exist
        :raises OSError: if files are corrupted or cannot be loaded
        """
        if not self._ml_dir.is_dir():
            raise FileNotFoundError(f"Missing ml directory: {self._ml_dir}")

        model_path = self._ml_dir / 'randomforestmodel.pkl'
        model_medium_path = self._binaries_dir / 'randomforestmediummodel.pkl'
        encoder_path = self._binaries_dir / 'mediumlabelencoder.pkl'

        if not model_path.is_file():
            raise FileNotFoundError(f"Missing required model file: {model_path}")

        print(f"Loading AI models from: {self._ml_dir} and {self._binaries_dir} ...")

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(model_medium_path, 'rb') as f:
                    self.model_medium = pickle.load(f)
                with open(encoder_path, 'rb') as f:
                    self.label_encoder = pickle.load(f)
        except Exception as e:
            raise OSError(f"Failed to load AI models: {e}")

    def _count_words(self, text):
        """
        Method counting total words in the provided text
        :param text: headline text
        :return: integer count of words
        """
        if not isinstance(text, str):
            text = str(text)
        return len(text.split())

    def _calc_upper_ratio(self, text):
        """
        Method calculating the ratio of uppercase letters to total length
        :param text: headline text
        :return: float representing the ratio (0.0 to 1.0)
        """
        if not isinstance(text, str):
            text = str(text)
        if len(text) == 0:
            return 0.0
        upper_chars = sum(1 for c in text if c.isupper())
        return round(upper_chars / len(text), 3)

    def _has_buzzword(self, text):
        """
        Method counting the total occurrences of buzzwords
        :param text: headline text
        :return: integer representing the total amount of buzzwords found
        """
        if not isinstance(text, str):
            text = str(text)
        text_lower = text.lower()
        score = 0
        for word in self.buzzwords:
            if word in text_lower:
                score += 1
        return score

    def _contains_number(self, text):
        """
        Method checking if the text contains any digits
        :param text: headline text
        :return: 1 if digit is present, else 0
        """
        if not isinstance(text, str):
            text = str(text)
        for char in text:
            if char.isdigit():
                return 1
        return 0

    def analyze_headline(self, text):
        """
        Main predictive method that prepares text and feeds it into the RandomForest
        :param text: headline string from the user input
        :return: boolean (is_clickbait) and float (probability percentage)
        :raises ValueError: if input text is empty or invalid
        """
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Input text must be a non-empty string")

        features = pd.DataFrame({
            'Word_Count': [self._count_words(text)],
            'Upper_Ratio': [self._calc_upper_ratio(text)],
            'Has_Buzzword': [self._has_buzzword(text)],
            'Contains_Number': [self._contains_number(text)],
            'Comma_Count': [text.count(',')],
            'Exclamation_Count': [text.count('!')],
            'Question_Count': [text.count('?')]
        })

        chance = self.model.predict_proba(features)[0][1]

        is_clickbait = bool(chance > 0.5)
        percent = round(chance * 100, 1)

        medium_pred_idx = self.model_medium.predict(features)[0]
        medium = self.label_encoder.inverse_transform([medium_pred_idx])[0]

        return is_clickbait, percent, medium
