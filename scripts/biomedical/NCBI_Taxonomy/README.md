# Importing NCBI Taxonomy Data

## Table of Contents

1. [About the Dataset](#about-the-dataset)
    1. [Download URL](#download-url)
    2. [Database Overview](#database-overview)
    3. [Schema Overview](#schema-overview)
       1. [New Schema](#new-schema)
       2. [dcid Generation](#dcid-generation)
       3. [enum Generation](#enum-generation)
       4. [Edges](#edges)
    4. [Notes and Caveats](#notes-and-caveats)
    5. [License](#license)
    6. [Dataset Documentation and Relevant Links](#dataset-documentation-and-relevant-links)
2. [About the Import](#about-the-import)
    1. [Artifacts](#artifacts)
    2. [Import Procedure](#import-procedure)
    3. [Test](#test)


## About the Dataset

NCBI Taxonomy "consists of a curated set of names and classifications for all of the source organisms represented in the International Nucleotide Sequence Database Collaboration (INSDC). The NCBI Taxonomy database contains a list of names that are determined to be nomenclaturally correct or valid (as defined according to the different codes of nomenclature), classified in an approximately phylogenetic hierarchy (depending on the level of knowledge regarding phylogenetic relationships of a given group) as well as a number of names that exist outside the jurisdiction of the codes. That is, it focuses on nomenclature and systematics, rather than documenting the description of taxa." Furthermore, NCBI Taxonomy "includes organism names and classifications for every sequence in the nucleotide and protein sequence databases of the INSDC. It provides a framework for clustering elements within other domains of NCBI web pages, for internal linking between domains of the Entrez system and for linking out to taxon-specific external resources on the web and relevant publications. It is also the standard nomenclature and classification repository for the INSDC that comprises of GenBank, the European Molecular Biology Laboratory (EMBL) and DNA Data Bank of Japan (DDBJ)."

### Download URL

NCBI Taxonomy data can be downloaded from the National Center for Biotechnology Information (NCBI) Assembly database using their FTP Site
1. [ncbi_taxdump](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.tar.Z). 
2. [ncbi_taxcat](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/taxcat.tar.gz).

### Database Overview

"NCBI Taxonomy distinguishes between formal and informal names. Formal names are declared based on rules laid down in four relevant codes of nomenclature (although other codes do exist). These are the International Code of Nomenclature for algae, fungi, and plants (ICNafp), the International Code of Nomenclature of Prokaryotes (ICNP) and the International Code of Zoological Nomenclature (ICZN). The viruses are governed by the International Code of Virus Classification and Nomenclature (ICVCN, also referred to as the ICTV Code). Informal names follow internal rules that are dictated by practical considerations outside of the Codes. For example, names lacking species epithets are commonly applied to GenBank records."

In this import we include information from the `ncbi_taxcat` and the following files downloaded from the ftp backend from `ncbi_taxdump`:
* divisions.dmp
* names.dmp
* host.dmp
* nodes.dmp
* categories.dmp

### Schema Overview

##### Classes

* Taxon 
    * Thing -> BiomedicalEntity -> BiologicalEntity -> GenomeAnnotation -> Taxon
  
##### Properties

* Taxon
    * abbreviaion 
    * biologicalHost
    * citation
    * commonName
    * genBankName
    * hasInheritedDivsion
    * ncbiBlastName
    * ncbiTaxId
    * scientificName
    * specializationOf
    * synonym
    * taxonDivision
    * taxonRank
    * taxonTopLevelCategory
  
##### Enumerations

 * TaxonTopLevelCategoryEnum

##### Enumeartions Generated By Script

* BiologicalTaxonomicDivisionEnum
* BiologicalTaxonomicRankEnum
* BiologicalTaxonomicRankBiotype

#### dcid Generation

The data for each entry in NCBI Taxonomy was stored as a Taxon entity. The dcid for these entities was generated by adding the prefix "bio/" to the scientific name for the Taxon in which the scientific name was reperesented in pascal case and text in <> was connected by an "_" (e.g. scientifc name Bacteria <Bacteria> for ncbi tax id "2" was represented as "bio/Bacteria_Bacteria").

#### enum Generation

The schema for the BiologicalTaxonomicDivisionEnum, and BiologicalHostEnum, and BiologicalTaxonomicRankEnum are autogenerated by `format_ncbi_taxonomy.py`.

A sample auto generated schema file saves at [ncbi_taxonomy_schema_enum.mcf](/scripts/biomedical/NCBI_Taxonomy/test_data/expected_output/ncbi_taxonomy_schema_enum.mcf) for reference

#### Edges

The edges, or links, in this import are between Taxon nodes that are related in parent-child relationships within the taxonomic heirachry. The dcid of a parent Taxon node is stored in the property "parentTaxon". For example, a node of taxon rank of Species will be linked to the relevant Taxon node of rank Genus.

### Notes and Caveats

* Data Consistency and Quality: 
    
    Rank Changes: Taxonomic classifications are subject to change, necessitating regular data refreshes. The NCBI Taxonomy database is on a daily refresh.
    
    Data Included in Biomedical Data Commons: Please note that in this import the files included from NCBI Taxonomy include `ncbi_taxcat` and a subset of files from `ncbi_taxdump`: `divisions.dmp`, `names.dmp`, `host.dmp`, nodes.dmp`, and `categories.dmp`

### License

This data is from an NIH human genome unrestricted-access data repository and made accessible under the [NIH Genomic Data Sharing (GDS) Policy](https://osp.od.nih.gov/scientific-sharing/genomic-data-sharing/).

### Dataset Documentation and Relevant Links

More information about the NCBI Taxonomy database can be found [here](https://www.ncbi.nlm.nih.gov/books/NBK53758/). Additional information is contained in [Schoch et al. 2020](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7408187/).

## About the import

### Artifacts

#### Scripts

##### Bash Scripts

- [download.sh](download.sh) downloads the most recent release of the NCBI Taxonomy data.
- [run.sh](run.sh) creates new taxonomy enum mcf and converts data into formatted CSV for import of data using categories.dmp, division.dmp, host.dmp, names.dmp & nodes.dmp files from download location
- [tests.sh](tests.sh) runs standard tests on CSV + tMCF pairs to check for proper formatting.

##### Python Scripts

- [format_ncbi_taxonomy.py](scripts/format_ncbi_taxonomy.py) creates the taxonomy enum mcf and formatted CSV files.
- [format_ncbi_taxonomy_test.py](scripts/format_ncbi_taxonomy.py) unittest script to test standard test cases on taxonomy enum mcf.

#### tMCFs

- [ncbi_taxonomy.tmcf](tMCFs/ncbi_taxonomy.tmcf) contains the tmcf mapping to the csv of taxonomy.

### Import Procedure

Download the most recent versions of NCBI Taxonomy data:

```bash
sh download.sh
```

Generate the enum schema MCF & formatted CSV:

```bash
sh run.sh
```

### Tests

The first step of `tests.sh` is to downloads Data Commons's java -jar import tool, storing it in a `tmp` directory. This assumes that the user has Java Runtime Environment (JRE) installed. This tool is described in Data Commons documentation of the [import pipeline](https://github.com/datacommonsorg/import/). The relases of the tool can be viewed [here](https://github.com/datacommonsorg/import/releases/). Here we download version `0.1-alpha.1k` and apply it to check our csv + tmcf import. It evaluates if all schema used in the import is present in the graph, all referenced nodes are present in the graph, along with other checks that issue fatal errors, errors, or warnings upon failing checks. Please note that empty tokens for some columns are expected as this reflects the original data. The imports create the Virus nodes that are then refrenced within this import. This resolves any concern about missing reference warnings concerning these node types by the test.

To run tests:

```bash
sh tests.sh
```

This will generate an output file for the results of the tests on each csv + tmcf pair

### Sample Data

This sample [dataset](/scripts/biomedical/NCBI_Taxonomy/test_data) is a representative subset of the larger dataset. It was selected using stratified sampling to ensure that it covers most of the of scenarios in the data cleaning functionality This can be used for testing purpose.

The sample input and output data are located at the following links:

Input data: [input_link](test_data/input)
Output data: [output_link](test_data/expected_output)
