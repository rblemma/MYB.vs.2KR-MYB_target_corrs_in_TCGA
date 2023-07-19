# README #

### A snakmake pipeline for computing spearrman correlations between MYB expression and expression of 2KR-MYB target genes from [PMID:xxx](https://doi.org/10.1016/j.jbc.2023.105062) among three TCGA cancer cohorts ###
- TCGA cancer cohort LAML-US
- TCGA cancer cohort BRCA-US and
- TCGA cancer cohort COAD-US

### How do I get set up? ###

* clone the repo by typing

```
git clone git@bitbucket.org:rblemma/myb.vs.2kr-myb_target_corrs_in_tcga.git

### Dependencies ###
- Snakemkae >= 3.5
- R version 4.0.2

### How to run tests ###
- Type the following from the `results` folder
- you can increase the number of cores you want to use by assigning a number to the -j parameter. The following command uses 1 core

```
snakemake -j 1
```

### Who do I talk to? ###

* Roza Berhanu Lemma (rozaberhanu@gmail.com)
