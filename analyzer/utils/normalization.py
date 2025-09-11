import re
import unicodedata
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

class Normalization:
    def normalize_content(self, user_input: str) -> list:
        try:
            text = self.lower_content(user_input)
            text = self.remove_accents(text)
            text = self.strip_punctuation(text)
            text = self.remove_whitespace(text)
            tokens = self.tokenize_string(text)
            clean_tokens = self.remove_stopwords(tokens)
            return clean_tokens
        except Exception as error:
            print(f'An error occurred during full normalization: {error}')
            return []

    def lower_content(self, user_input: str) -> str:
        try:
            return user_input.lower()
        except Exception as error:
            print(f'An error occured during lowering content process: {error}')

    def strip_punctuation(self, user_input: str) -> str:
        try:
            return re.sub(r'[^\w\s]', '', user_input)
        except Exception as error:
            print(f'An error occured during punctuation stripping process: {error}')
    
    def remove_accents(self, user_input: str) -> str:
        try:
            normalized = unicodedata.normalize('NFD', user_input)
            return ''.join(char for char in normalized if unicodedata.category(char) != 'Mn')
        except Exception as error:
            print(f'An error occured during accents removal process: {error}')

    
    def tokenize_string(self, user_input: str) -> str:
        try: 
            return re.findall(r'\w+', user_input)
        except Exception as error:
            print(f'An error occured during string tokenization process: {error}')
            
    def remove_whitespace(self, user_input: str) -> str:
        try:
            return user_input.strip()
        except Exception as error:
            print(f'An error occured during whitespace removal process: {error}')

    def remove_stopwords(self, tokens: list) -> list:
        try:
            stop_words = set(stopwords.words('english'))
            return [word for word in tokens if word not in stop_words]
        except Exception as error:
            print(f'An error occurred during stopword removal: {error}')
