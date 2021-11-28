# LaWebDeDatos2021
This is a repository for the final project of the course La Web de Datos at the Universidad de Chile for the spring semester 2021.

## Data
The data used in this project was downloaded from https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset. The download consisted of 4 csv files:
<ul>
  <li>names.csv: Dataset containing information on cast members with personal attributes such as birth details, death details, height, spouses, children, etc.</li>
  <li>movies.csv: Dataset containing movies with attributes such as movie description, average rating, number of votes, genre, etc.</li>
  <li>ratings.csv: Dataset containing rating details from demographic perspective</li>
  <li>title_principals.csv: Dataset containing cast members' roles in movies with attributes such as IMDb title id, IMDb name id, order of importance in the movie, role, and characters played</li>
</ul>

## Preprocessing
In order to convert the data into a RDF format, some preprocesssing steps were necessary.

### names.csv
This file contains information on cast members. Within the preprocessing, unnecessary columns were deleted. Furthermore, the columns *place_of_death* and *place_of_birth* were separated into two columns each, *country_of_death* and *city_of_death* (*country_of_birth* and *city_of_birth*, respectively).

### movies.csv
This file contains information on movies. Within the preprocessing, we mainly dealt with the columns *country*, *genre* and *language*. These columns contained comma separated lists of (potentially) multiple values. Hence, for each of these columns we created a separate mapping table with a column *imdb_title_id* and the other respective column. In these mapping tables, the *imdb_title_id* could appear multiple times (in multiple rows), depending on the number of entries for the respective column. The mapping tables can be found in the folder *./data/preprocessed*.

### ratings.csv
For the file containing the ratings, no specific preprocessing steps were necessary.

### title_principles.csv
For the file containing the mapping between movies and cast members and their roles, no specific preprocessing steps were necessary.

### Primary and Foreign Keys
As one further step of preprocessing, we loaded all files into a local Postgres instance. We then created a mapping between the different tables defining primary and foreign keys (*imdb_title_id* and *imdb_name_id*) and eliminated all entries where the primary key to a foreign key column entry did not exist. This way, we prevented errors when populating the ontology later on.
The final preprocessed files can be found in the folder *./data/sql_preprocessed/*

## Ontology Creation
The ontology was created using WebProtégé. We decided against using existing namespaces and prefixes and define everything ourselves. The created ontology can be found in the folder *./ontology*, the file is named *WebDeDatos_IMDb.ttl*.

## Populating the Ontology
Populating the ontology was done with the notebook *ontology_population.ipynb*. We ran the notebook on Google Colab because we had difficulties with the package rdflib locally.
The final populated ontology is unfortunately too large for GitHub, here you can download the file: https://studentkit-my.sharepoint.com/:u:/g/personal/ucevw_student_kit_edu/ESfaEEs32ERHqBBZ71wpKuMBr0Hd_y2UGXEQdGaPOJJUqw?e=0JQpou

