This folder contains the following files and subfolders: 

- subfolderfolder data: 
    *data_DE.tsv, a tsv_file with the collected articles and metadata on the articles in German.
    *data_NL.tsv, a tsv_file with the collected articles and metadata on the articles in Dutch.
    
    - subfolder annotations:
        *all annotations files for German and Dutch, on the terms weight, woman and man translated in German and Dutch.
        The document folders are informative on the language and the term. a1 stands for annotator 1 (Eva den Uijl), 
        a2 stands for annotator 2 (Myrthe Buckens).

*Annotation_guidelines.docx, the guidelines according to which the annotations are conducted. 

*get_all_documents.py, code to extract all documents from GoogleNews. Note that since the original articles are extracted on the 16th of November, 2020, the code will extract different documents since there is no option to enter a beginning and end date. To avoid that the data on which the experiment is conducted gets overwritten, this file will write a new data extraction to data/data_de.tsv or data/data_nl.tsv (depending on the language), with lowercase letters instead of uppercase letters. If you would like to extract new data and run all the other code, change the language_dutch and language_german strings from lowercase letters to uppercase letters in get_all_documents.py (indicated at the top of the file)

*requirements.txt, this file contains a list with all modules needed to run all the code. 

*run_all_analysis.py, this file contains all code to run all analysis that are conducted for the experiment. It will write the results of the analysis to your command screen. You can read upon these statistics on our blog, 'Body Positivity and Fat Shaming'.

*utils_html.py, this file contains helper codes for get_all_document.py to extract GoogleNews documents from a html source. 