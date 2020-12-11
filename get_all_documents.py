#Importing needed functions for data crawling

#TO OVERWRITE THE EXCISTING FILES, CHANGE THE LANGUGE STRINGS BELOW TO UPPERCASE NL AND DE 

language_dutch = 'nl'
language_german = 'de'


from util_html import *

def extract_metadata_googlenews(article, base_url):
    """
    Function that extracts metadata from google news articles. 
    Returns the date, time, publisher, title and article url from each article.
    :param article: an article extracted from google news 
    :param base_url: the base_url from the article
    :type article: string
    :type base_url: string
    
    :returns: strings date, time, publisher, title, article_url 
    """
    # Extract the publication date
    time = article.find('time')
    if time:
        datetime = time.get('datetime')
        date, time = datetime.split("T")
    else:
        date = ""
        time = ""
        
    # Discover the structure in the data
    technical_data, title_html, publisher_html = article.find_all('a')
        
    # Extract meta data
    publisher = publisher_html.contents[0]
    title = title_html.contents[0]
    url = title_html.get('href')        
        
    # The URL is a redirect from the Google page. To create the original URL: 
    article_redirect = base_url + url
    article_url = requests.get(article_redirect).url
        
    return date, time, publisher, title, article_url


def writing_data_to_tsv(outputfile, topics, language):
    """
    Function that extracts the articles and metadata from google news articles and writes this to a tsv file.
    :param outputfile: outputfile where the data is written to
    :param topics: the topics that have to occur in the articles
    :param language: the language of the articles
    :type outputfile: string with path to file
    :type topics: list with the topics of the articles
    :type language: string 
    """
    with open(outputfile, "w", encoding= 'utf-8') as f:
        
        # Writing header to file 
        f.write("Publication Date\tTime\tPublisher\tAuthor\tTitle\tURL\tText\n")
        print('Creating file and extracting data... This might take some time!')
        
        for topic in topics: 
            
            # Converting the topic to a searchable query for the articles
            query = topic.lower()
            full_query = "?q={0}&gl={1}".format(query, language)
            base_url = "http://news.google.com/"
            query_url = (base_url + full_query)
            query_content = url_to_html(query_url)
            articles = query_content.find_all('article')
        
            for i, article in enumerate(articles):

                # Extract metadata
                date, time, publisher, title, article_url = extract_metadata_googlenews(article, base_url)

                # Extract content
                article_content = url_to_html(article_url)
                author = parse_author(article_content)
                content = parse_news_text(article_content)

                # Removing the new lines so that the articles are saved as strings 
                content = content.replace("\n", "")
                content = content.replace("\t", "")

                # We want the fields to be separated by tabulators (\t)
                output = "\t".join([date, time, publisher, author, title, article_url, content])
                f.write(output +"\n")
                


def main(argv=None):
    
    if argv is None:
        argv = sys.argv
    
    language = argv[1]
    topics = argv[2]
    outputfile = "data/data_"+language+".tsv"
    
    writing_data_to_tsv(outputfile, topics, language)
    

topics_nl = ['fatshaming+vrouw', 'fatshaming+man', 'body positivity+vrouw', 'body positivity+man']
argv_1 = ['python', language_dutch, topics_nl]
main(argv_1)
print('Done with the first language!')

topics_de = ['fatshaming+Frau', 'fatshaming+Mann', 'body positivity+Frau', 'body positivity+Mann']
argv_2 = ['python', language_german, topics_de]
main(argv_2)
print('Done with the second language! Go check out your data.')
