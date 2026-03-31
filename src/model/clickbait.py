import pickle
import numpy as np
import pandas as pd

from pathlib import Path
from tensorflow.keras.models import load_model


class Clickbait:
    def __init__(self):
        """
        Constructor initializes the buzzword dictionary and triggers model loading.
        Path resolution is handled automatically relative to this file's location.
        """
        self._binaries_dir = Path(__file__).resolve().parent / 'ml'
        self.buzzwords = {word: 1 for word in ['děsivé ','peklo', 'otevřeně', 'ukázala', 'slzách', 'drama', 'odhalena', 'přiznání', 'detaily', 'šokující']}
        self.model = None
        self.vectorizer = None
        self.scaler = None
        self._validate_and_load_models()

    def _validate_and_load_models(self):
        """
        Method for validating paths and loading serialized Machine Learning models.
        :raises FileNotFoundError: if the binaries directory or required files do not exist
        :raises OSError: if files are corrupted or cannot be loaded
        """
        if not self._binaries_dir.is_dir():
            raise FileNotFoundError(f"Missing models directory: {self._binaries_dir}")

        model_path = self._binaries_dir / 'muj_model.keras'
        vectorizer_path = self._binaries_dir / 'vectorizer.dat'
        scaler_path = self._binaries_dir / 'scaler.dat'

        for file_path in (model_path, vectorizer_path, scaler_path):
            if not file_path.is_file():
                raise FileNotFoundError(f"Missing required model file: {file_path}")

        print(f"Loading AI models from: {self._binaries_dir} ...")

        try:
            self.model = load_model(str(model_path))

            with open(vectorizer_path, 'rb') as f:
                self.vectorizer = pickle.load(f)

            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
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

    def _calculate_buzzword_score(self, text):
        """
        Method computing the emotional score based on predefined buzzwords
        :param text: headline text
        :return: integer representing the total buzzword weight score
        """
        if not isinstance(text, str):
            text = str(text)
        text_lower = text.lower()
        score = 0
        for word, weight in self.buzzwords.items():
            if word in text_lower:
                score += weight
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
        Main predictive method that prepares text and feeds it into the Neural Network
        :param text: headline string from the user input
        :return: boolean (is_clickbait) and float (probability percentage)
        :raises ValueError: if input text is empty or invalid
        """
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Input text must be a non-empty string")

        num_features = pd.DataFrame({
            'Word_Count': [self._count_words(text)],
            'Upper_Ratio': [self._calc_upper_ratio(text)],
            'Comma_Count': [text.count(',')],
            'Exclamation_Count': [text.count('!')],
            'Question_Count': [text.count('?')],
            'Has_Buzzword': [self._calculate_buzzword_score(text)],
            'Contains_Number': [self._contains_number(text)]
        })

        text_vec = self.vectorizer.transform([text]).toarray()
        num_scaled = self.scaler.transform(num_features)

        final_input = np.hstack((text_vec, num_scaled))

        chance = self.model.predict(final_input, verbose=0)[0][0]

        is_clickbait = bool(chance > 0.5)
        percent = round(chance * 100, 1)

        return is_clickbait, percent