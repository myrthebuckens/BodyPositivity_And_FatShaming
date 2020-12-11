#Importing functions
import pandas as pd
import glob
import os.path
from itertools import combinations
from sklearn.metrics import cohen_kappa_score, confusion_matrix


def evaluate_annotations(terms, language):
    """
    Function that evaluates the annotations of annotator a and annotator b.
    Prints agreement percentage, Cohen's kappa and the confusion matrix for each term and language.
    :param terms: the terms that occur in the annotated articles 
    :param language: the language of the articles
    :type terms: list 
    :type language: string
    """

    # The categories used in the annotation task 
    categories = ["RAT", "EMO", "FAC", "OFF"]

    for term in terms:
        print('The agreement on the term',term, language, 'is:')
        annotations = {}

        # Read in the data
        for sheet in glob.glob("data/annotations/annotationsheet"+ language + "_" + term +"*.tsv"):
            filename, extension = os.path.basename(sheet).split(".")
            prefix, term, annotator = filename.split("_")

            # Read in annotations
            annotation_data = pd.read_csv(sheet, sep="\t", header=0, keep_default_na=False)
            annotations[annotator] = annotation_data["Annotation"]

        # Defining the annotators
        annotators = annotations.keys()
        
        for annotator_a, annotator_b in combinations(annotators, 2):
            agreement = [anno1 == anno2 for anno1, anno2 in zip(annotations[annotator_a], annotations[annotator_b])]

            percentage = sum(agreement)/len(agreement)

            #inter-annotator agreement 
            print("Percentage Agreement: %.2f" %percentage)

            #Cohen's kappa 
            kappa = cohen_kappa_score(annotations[annotator_a], annotations[annotator_b], labels=categories)
            print("Cohen's Kappa: %.2f" %kappa)
            confusions = confusion_matrix(annotations[annotator_a], annotations[annotator_b], labels=categories)

            # Generating the confusion matrix
            pandas_table = pd.DataFrame(confusions, index=categories)
            markdown_table = pandas_table.to_markdown()
            print(markdown_table)

                    
terms_nl = [" man ", " vrouw ", " gewicht "]                  
evaluate_annotations(terms_nl, 'NL')

terms_de = [" Mann ", " Frau ", " Gewicht "]
evaluate_annotations(terms_de, 'DE')