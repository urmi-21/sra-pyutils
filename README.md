# sra-pyutils
Wrapper around NCBI eutils to easily search SRA

## Prerequisites
* Python 3
* eutils

Optionally, create a conda environment to handle dependencies

```
conda create -n srapyutils python=3.7
conda activate srapyutils
conda install -c bioconda entrez-direct 
```

## Examples

### Fetch SRA metadata by ids
```
python fetchbyid.py sampleids sampleout.tsv
```
