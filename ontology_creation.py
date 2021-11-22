import rdflib
import pandas as pd
# warnings.filterwarnings('ignore')

# g will be the knowledge graph
g = rdflib.Graph()
g.parse('./Data/RDF_Final.owl', format='xml')

# import csv files with the data
countries = pd.read_csv('./data/sql_processed/countries.csv', sep=',', header=0)
countries = countries.fillna("")

genres = pd.read_csv('./data/sql_processed/genres.csv', sep=',', header=0)
genres = genres.fillna("")

languages = pd.read_csv('./data/sql_processed/languages.csv', sep=',', header=0)
languages = languages.fillna("")

movies = pd.read_csv('./data/sql_processed/movies.csv', sep=',', header=0)
movies = movies.fillna("")

names = pd.read_csv('./data/sql_processed/names.csv', sep=',', header=0)
names = names.fillna("")

ratings = pd.read_csv('./data/sql_processed/ratings.csv', sep=',', header=0)
ratings = ratings.fillna("")

mapping_title_names = pd.read_csv('./data/sql_processed/mapping_title_names.csv', sep=',', header=0)
mapping_title_names = mapping_title_names.fillna("")

# add the data to the ontology


g.serialize(destination='./Data/Ontology/IMDB.owl', format='xml')
