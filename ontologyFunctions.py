import rdflib
import pandas as pd
from rdflib.namespace import RDF, RDFS
from rdflib import Literal
import numpy as np
import warnings

# prefixes of all ontologies you will be using in your KG
ontology = rdflib.Namespace("http://transraz")
addressbook = rdflib.Namespace("http://transraz/addressbook")
transraz = rdflib.Namespace("http://transraz/addressbook/")
vcard = rdflib.Namespace("http://www.w3.org/2006/vcard/ns#")
schema = rdflib.Namespace("http://schema.org/")
dbo = rdflib.Namespace("http://www.dbpedia.org/ontology/")


def addPersonsToOntology(g, df):
    # iterate
    for i in range(0, len(df.IRI)):

        # Add the Person entities with the label full name for each pers
        g.add((addressbook[df.IRI[i]], RDF.type, vcard.Individual))
        if df.fullname[i] != "":
            g.add((addressbook[df.IRI[i]], RDFS.label, Literal(df.fullname[i])))
        if df.firstnameabbr[i] != "":
            g.add((addressbook[df.IRI[i]], transraz.abbreviatedName, Literal(df.firstnameabbr[i])))
        if df.firstname[i] != "":
            g.add((addressbook[df.IRI[i]], vcard.givenName, Literal(df.firstname[i])))
        if df.lastname[i] != "":
            g.add((addressbook[df.IRI[i]], vcard.familyName, Literal(df.lastname[i])))
        if df.civilrights[i] != "":
            if df.civilrights[i] == True:
                g.add((addressbook[df.IRI[i]], transraz.civilRights, Literal(True)))
            else:
                g.add((addressbook[df.IRI[i]], transraz.civilRights, Literal(False)))

        if df.beruf_IRI[i] != "":
            g.add((addressbook[df.beruf_IRI[i]], RDF.type, schema.Occupation))

            # if the Occupation name is not empty we take it as a label
            if df.occupation[i] != "":
                g.add((addressbook[df.beruf_IRI[i]], RDFS.label, Literal(df.occupation[i])))
            # else if the Occupation abbreviation is not empty we take it as a label
            elif df.occupationabbr[i] != "":
                g.add((addressbook[df.beruf_IRI[i]], RDFS.label, Literal(df.occupationabbr[i])))
                g.add((addressbook[df.beruf_IRI[i]], transraz.abbreviatedName, Literal(df.occupationabbr[i])))

            g.add((addressbook[df.IRI[i]], schema.hasOccupation, addressbook[df.beruf_IRI[i]]))

        # Add address entities with the label address_IRI
        j = 0
        while j < 3:
            if df["address_" + str(j) + "_IRI"][i] != "":
                g.add((addressbook[df["address_" + str(j) + "_IRI"][i]], RDF.type, vcard.Address))
                g.add((addressbook[df.IRI[i]], vcard.hasAddress, addressbook[df["address_" + str(j) + "_IRI"][i]]))
                g.add((addressbook[df["address_" + str(j) + "_IRI"][i]], RDFS.label,
                       Literal(df['fulladdress_' + str(j)][i])))
                if df["floor_" + str(j)][i] != "":
                    g.add((addressbook[df["address_" + str(j) + "_IRI"][i]], transraz.floor,
                           Literal(df["floor_" + str(j)][i])))
                if df["partofhouse_" + str(j)][i] == "H":
                    g.add((addressbook[df["address_" + str(j) + "_IRI"][i]], transraz.yard, Literal("Hinterhaus")))
                if df["housenumber_" + str(j)][i] != "":
                    g.add((addressbook[df["address_" + str(j) + "_IRI"][i]], transraz.buildingNumber,
                           Literal(df["housenumber_" + str(j)][i])))

                # Add Street to Address
                if df["street_" + str(j) + "_IRI"][i] != "":
                    g.add((addressbook[df["street_" + str(j) + "_IRI"][i]], RDF.type, dbo.Street))
                    g.add((addressbook[df["street_" + str(j) + "_IRI"][i]], RDFS.label,
                           Literal(df["streetname_" + str(j)][i])))
                    g.add((addressbook[df["address_" + str(j) + "_IRI"][i]], vcard.hasStreetAddress,
                           addressbook[df["street_" + str(j) + "_IRI"][i]]))
            j += 1
    return g

def addCompaniesToOntology(g, dfCompanies):
    for i in range(0, len(dfCompanies.IRI)):

        # Add the Organization entities with the label full name for each pers
        g.add((addressbook[dfCompanies.IRI[i]], RDF.type, vcard.Organization))
        # Add Company Name
        if dfCompanies.companyname[i] != "":
            g.add((addressbook[dfCompanies.IRI[i]], vcard.organizationName, Literal(dfCompanies.companyname[i])))
        # Add Company Type
        if dfCompanies.companytype[i] != "":
            g.add((addressbook[dfCompanies.IRI[i]], transraz.industry, Literal(dfCompanies.companytype[i])))
        # Add Civil Rights
        if dfCompanies.civilrights[i] != "":
            if dfCompanies.civilrights[i] == True:
                g.add((addressbook[dfCompanies.IRI[i]], transraz.civilRights, Literal(True)))
            else:
                g.add((addressbook[dfCompanies.IRI[i]], transraz.civilRights, Literal(False)))

        # Add Owners, either by using existing entries or by creating a new one
        j = 0
        while j < 4:
            if dfCompanies["owner_" + str(j) + "_IRI"][i] != "":
                # Add the Person entities with the label full name for each pers
                persIRI = dfCompanies["owner_" + str(j) + "_IRI"][i]
                g.add((addressbook[persIRI], RDF.type, vcard.Individual))
                if dfCompanies["owner_" + str(j) + "_fullname"][i] != "":
                    g.add((addressbook[persIRI], RDFS.label, Literal(dfCompanies["owner_" + str(j) + "_fullname"][i])))
                if dfCompanies["owner_" + str(j) + "_firstname_abbr"][i] != "":
                    g.add((addressbook[persIRI], transraz.abbreviatedName,
                           Literal(dfCompanies["owner_" + str(j) + "_firstname_abbr"][i])))
                if dfCompanies["owner_" + str(j) + "_firstname"][i] != "":
                    g.add((addressbook[persIRI], vcard.givenName,
                           Literal(dfCompanies["owner_" + str(j) + "_firstname"][i])))
                if dfCompanies["owner_" + str(j) + "_lastname"][i] != "":
                    g.add((addressbook[persIRI], vcard.familyName,
                           Literal(dfCompanies["owner_" + str(j) + "_lastname"][i])))
                g.add((addressbook[persIRI], dbo.owningOrganisation, addressbook[dfCompanies.IRI[i]]))
                g.add((addressbook[dfCompanies.IRI[i]], transraz.ownedBy, addressbook[persIRI]))
            j += 1

        # Adresses
        j = 0
        while j < 6:
            if dfCompanies["address_" + str(j) + "_IRI"][i] != "":
                # Add new Address Entry if not existent beforehand
                tempIndex = dfCompanies["address_" + str(j) + "_IRI"][i]
                g.add((addressbook[tempIndex], RDF.type, vcard.Address))
                g.add((addressbook[dfCompanies.IRI[i]], vcard.hasAddress, addressbook[tempIndex]))
                g.add((addressbook[tempIndex], RDFS.label, Literal(dfCompanies["fulladdress_" + str(j)][i])))
                if dfCompanies["floor_" + str(j)][i] != "":
                    g.add((addressbook[tempIndex], transraz.floor, Literal(dfCompanies["floor_" + str(j)][i])))
                if dfCompanies["partofhouse_" + str(j)][i] == "H":
                    g.add((addressbook[tempIndex], transraz.yard, Literal("Hinterhaus")))
                if dfCompanies["housenumber_" + str(j)][i] != "":
                    g.add((addressbook[tempIndex], transraz.buildingNumber,
                           Literal(dfCompanies["housenumber_" + str(j)][i])))

                # Add Street to Address
                if dfCompanies["street_" + str(j) + "_IRI"][i] != "":
                    tempStrIndex = dfCompanies["street_" + str(j) + "_IRI"][i]
                    g.add((addressbook[tempStrIndex], RDF.type, dbo.Street))
                    g.add((addressbook[tempStrIndex], RDFS.label, Literal(dfCompanies["streetname_" + str(j)][i])))
                    g.add((addressbook[tempIndex], vcard.hasStreetAddress, addressbook[tempStrIndex]))
            j += 1
    return g


def addCompaniesWOownerToOntology(g, dfCompaniesWOOwner):
    for i in range(0, len(dfCompaniesWOOwner.IRI)):

        # Add the Organization entities with the label full name for each pers
        g.add((addressbook[dfCompaniesWOOwner.IRI[i]], RDF.type, vcard.Organization))
        # Add Company Name
        if dfCompaniesWOOwner.companyname[i] != "":
            g.add((addressbook[dfCompaniesWOOwner.IRI[i]], vcard.organizationName,
                   Literal(dfCompaniesWOOwner.companyname[i])))
        # Add Company Type
        if dfCompaniesWOOwner.companytype[i] != "":
            g.add(
                (addressbook[dfCompaniesWOOwner.IRI[i]], transraz.industry, Literal(dfCompaniesWOOwner.companytype[i])))
        # Add Civil Rights
        if dfCompaniesWOOwner.civilrights[i] != "":
            if dfCompaniesWOOwner.civilrights[i] == True:
                g.add((addressbook[dfCompaniesWOOwner.IRI[i]], transraz.civilRights, Literal(True)))
            else:
                g.add((addressbook[dfCompaniesWOOwner.IRI[i]], transraz.civilRights, Literal(False)))

        # Adresses
        j = 0
        while j < 14:
            if dfCompaniesWOOwner["address_" + str(j) + "_IRI"][i] != "":
                # Add new Address Entry if not existent beforehand
                tempIndex = dfCompaniesWOOwner["address_" + str(j) + "_IRI"][i]
                g.add((addressbook[tempIndex], RDF.type, vcard.Address))
                g.add((addressbook[dfCompaniesWOOwner.IRI[i]], vcard.hasAddress, addressbook[tempIndex]))
                g.add((addressbook[tempIndex], RDFS.label, Literal(dfCompaniesWOOwner["fulladdress_" + str(j)][i])))
                if dfCompaniesWOOwner["floor_" + str(j)][i] != "":
                    g.add((addressbook[tempIndex], transraz.floor, Literal(dfCompaniesWOOwner["floor_" + str(j)][i])))
                if dfCompaniesWOOwner["partofhouse_" + str(j)][i] == "H":
                    g.add((addressbook[tempIndex], transraz.yard, Literal("Hinterhaus")))
                if dfCompaniesWOOwner["housenumber_" + str(j)][i] != "":
                    g.add((addressbook[tempIndex], transraz.buildingNumber,
                           Literal(dfCompaniesWOOwner["housenumber_" + str(j)][i])))

                # Add Street to Address
                if dfCompaniesWOOwner["street_" + str(j) + "_IRI"][i] != "":
                    tempStrIndex = dfCompaniesWOOwner["street_" + str(j) + "_IRI"][i]
                    g.add((addressbook[tempStrIndex], RDF.type, dbo.Street))
                    g.add(
                        (addressbook[tempStrIndex], RDFS.label, Literal(dfCompaniesWOOwner["streetname_" + str(j)][i])))
                    g.add((addressbook[tempIndex], vcard.hasStreetAddress, addressbook[tempStrIndex]))
            j += 1
    return g