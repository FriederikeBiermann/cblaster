.. cblaster documentation master file, created by
   sphinx-quickstart on Mon Nov 11 10:25:59 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

cblaster
====================================

Welcome to cblaster's documentation!

cblaster is a tool for identifying co-located hits in BLAST searches against
NCBI sequence databases. It leverages the NCBI's public APIs to facilitate fully
remote searches, requiring no setup of local search databases.

If you find ``cblaster`` helpful, please cite: 

::

	Gilchrist, C. L. M.; Booth, T. J.; Chooi, Y.-H. Cblaster: A Remote Search Tool for Rapid Identification and Visualisation of Homologous Gene Clusters. bioRxiv 2020, 2020.11.08.370601. https://doi.org/10.1101/2020.11.08.370601

To view an example of what cblaster can produce, click here_.

.. _here: /_static/example.html


Features
========

- Fully remote searches against public NCBI sequence databases
- One command to generate local search databases from many genomes
- Easy to use graphical user interface (GUI)
- Fully interactive visualisations


User guide
==========

.. toctree::
        
        guide/index


API Documentation
=================

Comprehensive documentation for all public API exposed by `cblaster`:

.. toctree::

        api/index


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
