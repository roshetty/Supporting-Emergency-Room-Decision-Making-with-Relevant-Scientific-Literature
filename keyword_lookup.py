# command line
# python3 keyword_lookup.py /Users/lfspurr/Downloads/NLP_final_project_data/summaries_2015A.txt  /Users/lfspurr/Downloads/NLP_final_project_data/pmc-01/00/ MESH_KEYWORDS.csv

import nltk
from nltk.corpus import stopwords
import sys
import glob
import os
import csv

# read in summaries
input_file = sys.argv[1]
#'/Users/lfspurr/Downloads/NLP_final_project_data/summaries_2015A.txt'

with open(input_file ,'r') as f:
    content = f.readlines()

# remove newline characters from the end of each line
summaries = [x.strip() for x in content]

# choose a directory that contains the article files
directory = sys.argv[2]

# choose the input medical ontology
input_ontology = sys.argv[3]

# import the ontology as a list and transform the list to be uniformly lowercase
with open(input_ontology, 'r') as o:
    reader = csv.reader(o)
    ontology = list(reader)
    ont_str = [''.join(item) for item in ontology]
    ont_final = [x.lower() for x in ont_str]

# choose which common/stop words to ignore
stop_words = set(stopwords.words('english'))
remove_words = list()
remove_words.append('A')
remove_words.extend(('a', ',', '.', 'male', 'female', 'presents', 'The', 'the',
'history', 'boy', 'girl', ''))

# create a list of keywords to lookup in the articles
# remove stopwords and the common words specified above
# use partial matches
keywords = list()
for summary in summaries:
    tokens = nltk.word_tokenize(summary)
    tokens = [x.lower() for x in tokens]
    tokens_no_stopwords = [w for w in tokens if w not in stop_words]
    tokens_no_stopwords = [w for w in tokens_no_stopwords if w not in remove_words]
    #line_keywords = [w for w in tokens_no_stopwords if w in ont_str] # doesn't work well, need to get partial matches
    #line_keywords = [w for w in tokens_no_stopwords if any(x.startswith(w) for x in ont_str)] # slightly better
    line_keywords = [w for w in tokens_no_stopwords if any(w in string for string in ont_final)]

    keywords.append(list(set(line_keywords)))


# set the directory to the one specified in the standard input
os.chdir(directory)

# create an empty list of relevant articles
relevant_articles = dict()

#test file
input_summary = keywords[1]
count = 0


for fi in glob.glob('*.nxml'):
    with open(fi) as f:
        contents = f.read()
    count = 0
    for token in input_summary:
        if token in contents:
            count += 1
    if count > 2: # subject to change, but don't want to add a bunch of useless articles
        relevant_articles[fi] = count

def keywithmaxval(dictionary):
     v = list(dictionary.values())
     k = list(dictionary.keys())
     return k[v.index(max(v))]

print(summaries[1])
max_val = keywithmaxval(relevant_articles)
print(relevant_articles)
print(max_val)
print(relevant_articles.get(max_val))
