# Software

The following are the initial software implementations supporting the mzQC
format.

Core libraries:

- [mzqc-pylib](https://github.com/bigbio/mzqc-pylib): Python library to process
and validate mzQC files. It includes a Python object model, (de-)serialisation
functions, syntactic validation, and semantic validation of mzQC files.

Metrics generating software:

- [OpenMS](https://github.com/OpenMS/OpenMS): Open-source software C++ library
for LC/MS data management and analyses.
- [PTXQC](https://github.com/cbielow/PTXQC): An R package for creation of QC
reports from MaxQuant results and OpenMS mzTab files.
- [QCCalculator](https://github.com/bigbio/qccalculator): Python tool for base
QC metric calculation from mzML, mzIdentML, and MaxQuant input files.
- [Yamato / SwaMe / Prognosticator](https://github.com/PaulBrack/Yamato):
SWATH-MS QC metrics generation tools.
