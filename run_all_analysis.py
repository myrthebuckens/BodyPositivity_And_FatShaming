# Importing all needed modules
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import csv
from collections import Counter
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import seaborn as sb
import pandas as pd 


def preprocess_data(tsv_file, language):
    """
    Fuction preprocess the text of the articles from the dataset.
    Prints the authors of the articles and how often they occur in the dataset.
    :param tsv_file: tsv_file containing google news articles
    :param language: the language of the articles in the tsv_file
    :type tsv_file: string with path to file
    :type language: string 
    :returns: filtered_tokens dictionary 
    """
    
    with open (tsv_file, 'r', encoding = 'utf-8') as infile:
        news_content = csv.reader(infile, delimiter='\t',quotechar='|')

        publisher_list = []
        title_list = []
        raw_text = []
        tokenized_articles = []
        filtered_tokens = []
        all_sentences = []
        
        for row in news_content:  

        # Getting text from articles
            text = row[6]
            raw_text.append(text)
            tokenized_text = word_tokenize(text)
            tokenized_articles.append(tokenized_text)
        
            

        # Filtering the tokens on stopwords, punctuation and non-alpha characters
        punctuations = '''!()-[]{};:‘'"«”\,<>./?@#$%^&*Ⓒ_~'''
        
        for articles in tokenized_articles:
            for tokens in articles: 
                if language == 'NL':
                    tokens = tokens.lower()
                    if tokens not in stopwords.words("dutch") and tokens not in punctuations and tokens.isalpha():
                        filtered_tokens.append(tokens)
                        
                if language == 'DE':
                    if tokens not in stopwords.words("german") and tokens not in punctuations and tokens.isalpha():
                        filtered_tokens.append(tokens)
                        
    return filtered_tokens, tokenized_articles, raw_text 

def getting_basic_statistics(tsv_file, filtered_tokens, raw_text):
    """
    Function to obtain basic statistics on the articles in the dataset.
    :param tsv_file: tsv_file containing google news articles
    :param filtered_tokens: the filtered tokens from the articles
    :param raw text: the unprocessed text from the articles
    :type tsv_file: 
    
    """
    with open (tsv_file, 'r', encoding = 'utf-8') as infile:
        news_content = csv.reader(infile, delimiter='\t',quotechar='|')

        publisher_list = []
        title_list = []
        article_lengths = []
        all_sentences = []
        sentence_lengths = []
        
        article_count = 0      
        for row in news_content:  
                # Getting the publishers for the articles
                publisher = row[2]
                publisher_list.append(publisher)
                
                # Getting the titles for the articles
                title = row[4]
                title_list.append(title)
                
                text = row[6]
                if len(text) > 1:
                    article_count += 1
                
        # The lengths of each article
        for articles in raw_text:
            sentences = sent_tokenize(articles)
            all_sentences.append(sentences)
            article_lengths.append(len(articles))
            
        # The mean sentence length
        for sentences in all_sentences:
            length = len(sentences)
            sentence_lengths.append(length)
        mean_sentence_length = sum(sentence_lengths)/len(sentence_lengths)   
        
            
        # Getting type/token ratio
        filtered_tokens_dict = Counter(filtered_tokens)
        n_types = len(filtered_tokens_dict.keys())
        n_tokens = sum(filtered_tokens_dict.values())
        tt_ratio = n_types/n_tokens    
        mean_length = sum(article_lengths)/len(article_lengths)        
        
        # Getting the frequencies for the publishers 
        freq_publishers = Counter(publisher_list)
        amount_publishers = len(freq_publishers.keys())
        
        
        print('The list with all publishers is: ', freq_publishers, '\n')
        print('The amount of different publishers is: ', amount_publishers, '\n')
        print('The mean length of the articles is:', mean_length, '\n')
        print('The type/token ratio is: ', tt_ratio, '\n')
        print('The number of articles in total is', article_count)
        print('The mean sentence length is:', mean_sentence_length)
        
        

def top20_most_frequent_tokens(filtered_tokens, language):
    """
    Function that collects the twenty most used tokens from the data. 
    :param filtered_tokens: preprocessed tokens from the data
    :type filtered_tokens: dictionary
    Prints a dictionary with the most freqent tokens after preprocessing.
    """
        
    # Getting top 20 of most frequent tokens
    filtered_tokens_dict = Counter(filtered_tokens)

    top = list()
    top_20 = []
    for token in sorted(filtered_tokens_dict, key = filtered_tokens_dict.get, reverse=True):
        top.append([token, filtered_tokens_dict[token]])
    top_20 = top[:20]
        
           
    # Printing statistics 
    print('The top twenty most used tokens for', language, 'are:', top_20, '\n')


def comparing_annotations(language, terms):
    """
    Function that compares annotations between two annotators and adds the annotation label and the article title to a list when the
    annotations are the same. The articles with the label 'OFF' are taken out because they are not informative regarding the topic.
    Returns a list with tuples with article title and annotation label. 
    :param language: the language of the articles
    :param terms: the terms that occur in the articles
    :type language: string
    :type terms: list     
    """
    
    print('The language that the following statistics are on is:', language)
    agree_list = []
    
    for term in terms:
        document_a1 = 'data/annotations/annotationsheet'+ language + '_' + term + '_a1.tsv'
        document_a2 = 'data/annotations/annotationsheet'+ language + '_' + term + '_a2.tsv'
        
    
        with open(document_a1, 'r', encoding = 'utf-8') as f1, open(document_a2, 'r', encoding = 'utf-8') as f2:
            anno_a1 = csv.reader(f1, delimiter='\t',quotechar='|')
            next(anno_a1) # Next skips the first row, which is the header. 
            anno_a2 = csv.reader(f2, delimiter='\t',quotechar='|')
            next(anno_a2)
            
            for row_a1, row_a2 in zip(anno_a1, anno_a2):
                
                annotation_a1 = row_a1[3]
                annotation_a2 = row_a2[3]
                article_title = row_a1[1]
                
                if annotation_a1 == annotation_a2 and annotation_a1 != 'OFF':
                    agree_list.append((article_title, annotation_a1))
                    
    return agree_list
            
def getting_title_sentiment(agree_list): 
    """
    Function that generates sentiment labels on the article titles using Vader multi sentiment analysis. Prints dictionaries for the
    three sentiments positive, neutral and negative with frequencies for how often they occur for the different annotations. 
    :param agree_list: tuples with article title and annotation for different articles
    :type agree_list: list 
    """
    
    stats_list = []
    
    analyzer = SentimentIntensityAnalyzer()
    
    for title, annotation in agree_list: 
        sentiment_score = analyzer.polarity_scores(title)
        
        # Defining labels for the different scores 
        if sentiment_score['compound'] < -0.35:
            sentiment_label = 'neg'
        elif sentiment_score['compound'] > 0.35:
            sentiment_label = 'pos'
        else: 
            sentiment_label = 'neu'

        stats_dict = dict()
        stats_dict['title'] = title
        stats_dict['annotation'] = annotation
        stats_dict['sentiment'] = sentiment_label
        
        stats_list.append(stats_dict)
        
    pos_list = []
    neu_list = []
    neg_list = []
    
    # Counting how often the sentiments occur with the annotations 
    for dicts in stats_list: 
        if dicts['sentiment'] == 'pos':
            pos_list.append(dicts['annotation'])
        elif dicts['sentiment'] == 'neu':
            neu_list.append(dicts['annotation'])
        elif dicts['sentiment'] == 'neg':
            neg_list.append(dicts['annotation'])
    
    pos_dict = Counter(pos_list)
    print('the annotation labels with title sentiment positive:', pos_dict)
    
    neu_dict = Counter(neu_list)
    print('the annotation labels with title sentiment neutral:', neu_dict)
    
    neg_dict = Counter(neg_list)
    print('the annotation labels with title sentiment negative:', neg_dict)
    
    all_sentiments_dict = dict()
    all_sentiments_dict['pos'] = pos_dict
    all_sentiments_dict['neu'] = neu_dict
    all_sentiments_dict['neg'] = neg_dict
    
    print('all sentiments:', all_sentiments_dict)
    
    return all_sentiments_dict 
    
def create_heatmap_for_sentiment_and_annotation(all_sentiments_dict):
    """
    Function that generates a heatmap with annotations from a dictionary. 
    :param all_sentiments_dict: data for heatmap
    :type all_sentiments_dict: dict 
    :returns: heatmap
    """
    
    df = pd.DataFrame.from_dict(all_sentiments_dict)
    heatmap = sb.heatmap(df, cmap="vlag", annot=True, cbar_kws={'orientation': 'vertical'})
    
    return heatmap
    

def main(argv = None): 
    
    if argv is None:
        argv = sys.argv
    
    tsv_file = argv[1]
    language = argv[2]
    terms = argv[3]
    
    filtered_tokens, tokenized_articles, raw_text = preprocess_data(tsv_file, language)
    getting_basic_statistics(tsv_file, filtered_tokens, raw_text)
    top20_most_frequent_tokens(filtered_tokens, language)
    agree_list = comparing_annotations(language, terms)
    all_sentiments_dict = getting_title_sentiment(agree_list)
    create_heatmap_for_sentiment_and_annotation(all_sentiments_dict)
    
    
terms_NL = [' vrouw ', ' man ', ' gewicht ']
argv_NL = ['python', 'data/data_NL.tsv', 'NL', terms_NL]
main(argv_NL)

terms_DE = [' Frau ', ' Mann ', ' Gewicht ']
argv_DE = ['python', 'data/data_DE.tsv', 'DE', terms_DE]
main(argv_DE)
    
    
    
           
        
                
