Fighting the Resistance: Predicting Antibiotic Susceptibility in Meningitis-Causing Pathogens

*Abstract*

Antimicrobial resistance (AMR) poses a significant global health threat, endangering
millions worldwide. In response, machine learning (ML) algorithms have emerged as
promising tools for predicting the antibiotic resistance profiles of pathogenic organisms.
This study aims to evaluate the effectiveness of various ML models in predicting antibiotic
resistance in four bacterial pathogens associated with meningitis: Neisseria meningitidis,
Streptococcus pneumoniae, Streptococcus agalactiae, and Escherichia coli. Each pathogen was
tested against three specific antibiotics using three ML models: logistic regression, multi-layer perceptron (MLP), and extreme gradient boosting (XGBoost). A total of 27 models
were evaluated, followed by feature importance analyses for each. The results reveal that
XGBoost consistently outperformed logistic regression and MLP. Strong alignment was
observed between logistic regression and XGBoost in identifying well-established resis-
tance determinants across antibiotics, while MLP persistently contributed complementary
insights by highlighting alternative genomic markers potentially associated with complex,
non-linear, or less characterized resistance mechanisms. These findings underscore the
potential of using ML approaches to enhance the accuracy and interpretability of antibi-
otic resistance prediction, ultimately supporting improved clinical decision-making and
antimicrobial stewardship.

\*How to run the experiment\*

To run this experiment, I recommend creating a new conda environment and install all the requirements using the requirements.txt file. 

To avoid dependencies and compatibility issues, all bionformatics tools employed for this experiment were used through Docker images. Thus, to run this experiment, Docker needs to be installed beforehand. Important to note is that this experiment was conducted on a MacOS machine and the following intructions are not guaranteed to work well on other operating systems. In fact, it is strongly advised to not use a Windows machine in bioinformatics analyses, such as this one. 

The following images are necessary to be pulled from Docker: 
    staphb/prokka
    staphb/panaroo
    staphb/snp-sites
    staphb/iqtree
    quay.io/biocontainers/rgi:6.0.3--pyha8f3691_0
    quay.io/biocontainers/mlst:2.9--h7b50bb2_6

Once the conda environment is activated and Docker is installed and opened, a docker image can be pulled with the following command: docker pull image_name.

This experiment consists of multiple steps: preprocessing, training, and visualizations. 
For data preprocessing, the following bioinformatics tools are used:
    Prokka -- to annotate the raw genomic data;
    Panaroo -- to compute and analyze the pan-genome of each bacteria;
    SNP-sites -- to compute the single nucleotide polymorphism, based on the core gene alignenment (computed by Panaroo);
    IQtree -- to compute the phylogenetic trees of each group of strains;
    iTOL -- to visualize the phylogenetic trees;
    mlst -- to compute the sequence typing;
    RGI -- to construct the target variable. 
The following .py files need to be run so that the data preprocessing is completed:
    pangenome_SP.py -- this file reorganizes the genomes of Streptococcus pneumoniae downloaded from NCBI, uses Prokka to annotate the genomes, and uses  Panaroo to compute and analyze the pan-genome;
    pangenome_SA.py -- this is similar to pangenome_SP.py, performing the same pipeline on genomes of Streptococcus agalactie;
    pangenome_NM.py -- this is similar to pangenome_SP.py, performing the same pipeline on genomes of Neisseria meningiditis;
    pangenome_Ecoli.py -- this is similar to pangenome_SP.py, performing the same pipeline on genomes of Escherichia coli;
    
    get_snps.py -- employs SNP-sites to compute the SNPs using the core gene alignments of each bacteria;

    get_mlst.py -- runs MLST on Prokka-annotated .fna files to get the sequence typing of  each genome;

    get_trees.py -- employs IQtree to compute the phylogenetic tree of each group of genomes; it outputs four ".treefile" files which can be firther used on iTOL website to visualize the phylogenetic trees;

    rgi_SP.py -- uses the RGI tool to compute the target variable (the resistance/susceptibility labels) for Streptococcus pneumoniae; it uses the protein sequences that were computed by Prokka (.faa files);
    rgi_SA.py -- similar to rgi_SP.py, computing the resistance labels of genomes of Streptococcus agalactie;
    rgi_NM.py --  similar to rgi_SP.py, computing the resistance labels of genomes of Neisseria meningiditis;
    rgi_Ecoli.py --  similar to rgi_SP.py, computing the resistance labels of genomes of Escherichia coli.

For training the models, run the following Jupyter Notebooks:
    LG_SA.ipynb -- includes training, testing, and results visualizations of logistic regression on Streptococcus agalactiae;
    LG_SP.ipynb -- includes training, testing, and results visualizations of logistic regression on Streptococcus pneumoniae;
    LG_Ecoli.ipynb -- includes training, testing, and results visualizations of logistic regression on Escherichia coli;
    MLP_SA.ipynb -- includes training, testing, and results visualizations of multilayer perceptron on Streptococcus agalactiae;
    MLP_SP.ipynb -- includes training, testing, and results visualizations of multilayer perceptron on Streptococcus pneumoniae;
    MLP_Ecoli.ipynb -- includes training, testing, and results visualizations of multilayer perceptron on Escherichia coli;
    XGBoost_SA.ipynb -- includes training, testing, and results visualizations of XGBoost on Streptococcus agalactiae;
    XGBoost_SP.ipynb -- includes training, testing, and results visualizations of XGBoost on Streptococcus pneumoniae;
    XGBoost_Ecoli.ipynb -- includes training, testing, and results visualizations of XGBoost on Escherichia coli;

For visualizations, the following files can be run:
    visualization_gene_matrices.py -- creates a heatmap of the gene presence-absence matrix of each group of genomes, so it outputs four heatmaps


For more support on running the the bioinformatics tools, check the following sources:
    Prokka -- https://github.com/tseemann/prokka 
    Panaroo -- https://gthlab.au/panaroo/#/
    SNP-sites -- https://sanger-pathogens.github.io/snp-sites/
    IQtree -- https://github.com/iqtree/iqtree2
    iTOL -- https://itol.embl.de/;
    mlst -- https://github.com/tseemann/mlst;
    RGI -- https://github.com/arpcard/rgi.
