#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 10:40:50 2020

@author: vinnythompson
"""

import pandas as pd
import numpy as np
import pickle
import unicodedata
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.wordnet import WordNetLemmatizer 
from expand_contractions import expandContractions
import nltk
import re
import string
import spacy

class NLPPipe:
   
    def __init__(self, vectorizer=TfidfVectorizer(), tokenizer=None, cleaning_function=None, 
                 stemmer=None, model=None, sw_list=None):
        """
        A class for pipelining our data in NLP problems. The user provides a series of 
        tools, and this class manages all of the training, transforming, and modification
        of the text data.
        ---
        Inputs:
        vectorizer: the model to use for vectorization of text data
        tokenizer: The tokenizer to use, if none defaults to split on spaces
        cleaning_function: how to clean the data, if None, defaults to the in built class
        """
        if not tokenizer:
            tokenizer = self.splitter
        if not cleaning_function:
            cleaning_function = self.clean_text
        if not sw_list:
            sw_list = nltk.corpus.stopwords.words('english')
            custom = ['doi', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december', 'date', 'issue', 'report', 'say', 'published', 'erratum', 'could', 'h', 'j', 'mr', 'w', 'e', 'c', 'r', 'g', 'f', 'p', 'l', 'b', 'ha', 'wa', 'publication', 'updated', 'correction', 'corrected', 'paper', 'journal', 'nature', 'article']
            for word in custom:
                sw_list.append(word)
        self.tokenizer = tokenizer
        self.stemmer = stemmer
        self.model = model
        self.cleaning_function = cleaning_function
        self.vectorizer = vectorizer
        self._is_fit = False 
        self.sw_list = sw_list
        self.spacy_model = spacy.load('en', parse=True, tag=True, entity=True)
        
    def lowercase(self, text):
        return text.lower()
    
    def remove_accents(self, text):
        return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
    
    def contractions(self, text):
        return expandContractions(text)
    
    def remove_urls(self, text):
        return re.sub(r'http\S+', '', text)
    
    def remove_special_chars(self, text):
        pattern = r'[^a-zA-z0-9.,!?/:;\"\'\s]'
        return re.sub(pattern, '', text)
    
    def remove_nums(self, text):
        pattern = r'[^a-zA-z.,!?/:;\"\'\s]'
        return re.sub(pattern, '', text)
    
    def remove_punct(self, text):
        return ''.join([char for char in text if char not in string.punctuation])
    
    def get_lemma(self, text):
        lemmatizer = WordNetLemmatizer() 
        return ' '.join([lemmatizer.lemmatize(word) for word in self.tokenizer.tokenize(text)])
        
    
    def remove_stopwords(self, text, tokenizer):
        tokens = tokenizer.tokenize(text)
        tokens = [token.strip() for token in tokens]
        t = [token for token in tokens if token.lower() not in self.sw_list]
        return ' '.join(t)
    
    def remove_whitespace(self, text):
        pattern = r'^\s*|\s\s*'
        return re.sub(pattern, ' ', text).strip()

    def splitter(self, text):
        """
        Default tokenizer that splits on spaces naively
        """
        return text.split(' ')
    
        
    def clean_text(self, df, tokenizer, stemmer, field = 'comment_text'):
        """
        A naive function to lowercase all works can clean them quickly.
        This is the default behavior if no other cleaning function is specified
        """
        cleaned_text = []
        df['clean_text'] = df[field].apply(lambda x: self.remove_accents(x))
        df['clean_text'] = df['clean_text'].apply(lambda x: self.lowercase(x))
        df['clean_text'] = df['clean_text'].apply(lambda x: self.contractions(x))
        df['clean_text'] = df['clean_text'].apply(lambda x: self.remove_urls(x))
        df['clean_text'] = df['clean_text'].apply(lambda x: self.remove_special_chars(x))
        df['clean_text'] = df['clean_text'].apply(lambda x: self.remove_nums(x))
        df['clean_text'] = df['clean_text'].apply(lambda x: self.remove_punct(x))
        if stemmer:
            cleaned_text = []
            for post in df['clean_text'].values:
                cleaned_words = []
                for word in tokenizer.tokenize(post):
                    cleaned_words.append(stemmer.stem(word))
                cleaned_text.append(' '.join(cleaned_words))
            df['clean_text'] = cleaned_text
        else:
            df['clean_text'] = df['clean_text'].apply(lambda x: self.get_lemma(x))
        df['clean_text'] = df['clean_text'].apply(lambda x: self.remove_stopwords(x, self.tokenizer))
        df['clean_text'] = df['clean_text'].apply(lambda x: self.remove_whitespace(x))
        return df
                
    
    def fit(self, df, cleaned=False):
        """
        Cleans the data and then fits the vectorizer with
        the user provided text
        """
        if cleaned:
            clean_df = df
        else:
            clean_df = self.cleaning_function(df, self.tokenizer, self.stemmer)
        self.vectorizer.fit(clean_df['clean_text'])
        self._is_fit = True
        
    def transform(self, df, cleaned=False):
        """
        Cleans any provided data and then transforms the data into
        a vectorized format based on the fit function. Returns the
        vectorized form of the data.
        """
        if not self._is_fit:
            raise ValueError("Must fit the models before transforming!")
        if type(df) != pd.core.frame.DataFrame:
            df = pd.DataFrame({'comment_text': df})
        if cleaned:
            clean_df = df
        else:
            clean_df = self.cleaning_function(df, self.tokenizer, self.stemmer)
        return self.vectorizer.transform(clean_df['clean_text'])
    
    def save_pipe(self, filename):
        """
        Writes the attributes of the pipeline to a file
        allowing a pipeline to be loaded later with the
        pre-trained pieces in place.
        """
        if type(filename) != str:
            raise TypeError("filename must be a string")
        pickle.dump(self.__dict__, open(filename+".mdl", 'wb'))
        
    def load_pipe(self, filename):
        """
        Writes the attributes of the pipeline to a file
        allowing a pipeline to be loaded later with the
        pre-trained pieces in place.
        """
        if type(filename) != str:
            raise TypeError("filename must be a string")
        if filename[-4:] != '.mdl':
            filename += '.mdl'
        self.__dict__ = pickle.load(open(filename, 'rb'))