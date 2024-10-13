Source code for "Who's the GOAT? Sports Rankings and Data-driven Random Walks on the Symmetric Group," by Gian-Gabriel P. Garcia and J. Carlos Martínez Mori, arXiv 2409.12107, 2024.

The main execution file is main.py, which invokes:
  - helper.py, which pre-processes publicly available data compiled by GitHub user JeffSackmann
  - walker.py, which executes the data-driven random walk

The post-processing files are:
  - poset.py, which uses the output of main.py to build a poset
  - hasse.py, which uses the output of poset.py to prepare a Hasse diagram
  - extension.py, which uses the output of poset.py to prepare linear extensions and a figure of average ranks
  - scatter.py, which uses the output of extension.py to prepare a matrix of scatter plots of average ranks

The directories contain all figures and almost all outputs, with the exception of the ATP at cutoff 20 (which can be reproduced using this source code, but was too heavy to make available here directly).
