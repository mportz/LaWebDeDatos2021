import rdflib
import pandas as pd
#warnings.filterwarnings('ignore')

from Scripts.Functions import ontologyFunctions as OF


def run():
	#g will be your existing knowledge graph
	g = rdflib.Graph()
	g.parse('./Data/RDF_Final.owl', format='xml')


	#your excel data files
	df = pd.read_csv('./Data/Ontology/personsSpellCorrectedForOntology.csv', 'personsSpellCorrected', delimiter=";")
	dfCompanies = pd.read_csv('./Data/Ontology/companiesSpellCorrectedForOntology.csv', 'companiesSpellCorrected', delimiter=";")
	dfCompaniesWOOwner = pd.read_csv('./Data/Ontology/companiesWOownerSpellCorrectedForOntology.csv', 'companiesSpellCorrected', delimiter=";")
	dfCompanies = dfCompanies.fillna("")
	dfCompaniesWOOwner = dfCompaniesWOOwner.fillna("")
	df=df.fillna("")

	g = OF.addPersonsToOntology(g, df)
	g = OF.addCompaniesToOntology(g, dfCompanies)
	g = OF.addCompaniesWOownerToOntology(g, dfCompaniesWOOwner)

	g.serialize(destination='./Data/Ontology/RDF_IncIndividuals.owl', format='xml')
