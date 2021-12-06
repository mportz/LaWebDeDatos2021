```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ns1: <http://localhost:3030/drive/MyDrive/WebDeDatos/ontology/>
PREFIX owl: <http://www.w3.org/2002/07/owl#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
```

1. Who are the most known actors or actresses to have 0 children.

```
SELECT DISTINCT ?name
WHERE
{
  SELECT ?name (?mean*xsd:float(?votes) AS ?score)
  WHERE {
    ?movie rdfs:label ?title ; ns1:WebDeDatos_IMDb.ttlIMDbRating ?rating.
    ?actor ns1:WebDeDatos_IMDb.ttlactsIn ?movie ; rdfs:label ?name ;
    ns1:WebDeDatos_IMDb.ttlchildren ?children.
    ?rating ns1:WebDeDatos_IMDb.ttlmeanRating ?mean ; ns1:WebDeDatos_IMDb.ttlnumberOfRatings ?votes
    {
      SELECT ?movie 
      WHERE {
          ?movie a ns1:WebDeDatos_IMDb.ttlMovie ; ns1:WebDeDatos_IMDb.ttlyearPublished ?year. 
          FILTER(?year > "1970"^^xsd:int && ?year < "2000"^^xsd:int)
      }
      LIMIT 100000

    }
    FILTER(?children = "0")
  }
  ORDER BY DESC(?score)
}
```

2. What are the most frequent collaborations between actors/actresses

```
SELECT ?name1 ?name2 (COUNT(*) AS ?count)
WHERE {
  ?movie rdfs:label ?title.
  ?actor1 ns1:WebDeDatos_IMDb.ttlactsIn ?movie ; rdfs:label ?name1.
  ?actor2 ns1:WebDeDatos_IMDb.ttlactsIn ?movie ; rdfs:label ?name2.    
  {
    SELECT ?movie 
    WHERE {
      ?movie a ns1:WebDeDatos_IMDb.ttlMovie ; ns1:WebDeDatos_IMDb.ttlyearPublished ?year. 
      FILTER(?year > "1970"^^xsd:int && ?year < "2000"^^xsd:int)
    }
    LIMIT 100000

  }
  FILTER(?name1 < ?name2)
}
GROUP BY ?name1 ?name2
ORDER BY DESC(?count)
```

3. Movies in which the director has a native language different than the one that is spoken on screen.

```
SELECT ?director_country ?language ?title
WHERE {
  
  ?movie rdfs:label ?title ; ns1:WebDeDatos_IMDb.ttllanguage ?language.
  ?director ns1:WebDeDatos_IMDb.ttldirected ?movie ; rdfs:label ?name1 ; 
  ns1:WebDeDatos_IMDb.ttlcountry_of_birth ?director_country.
  {
    SELECT ?movie 
    WHERE {
      ?movie a ns1:WebDeDatos_IMDb.ttlMovie ; ns1:WebDeDatos_IMDb.ttlyearPublished ?year. 
      FILTER(?year > "1970"^^xsd:int && ?year < "2020"^^xsd:int)
    }
    LIMIT 100000

  }
  FILTER((?director_country = "Chile" && ?language = "German") || (?director_country = "Germany" && ?language = "Spanish"))
}
```

