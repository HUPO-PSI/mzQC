# Software

The following are the initial software implementations supporting the mzQC
format.

Core libraries:

- [pymzqc](https://github.com/MS-Quality-Hub/pymzqc): Python library to create, process, and validate mzQC files.
It includes a Python object model, (de-)serialisation functions, syntactic validation, and semantic validation of mzQC files.
- [jmzqc](https://github.com/MS-Quality-Hub/jmzqc): Java library to create, process, and validate mzQC files.
It includes a Java object model, (de-)serialisation functions, syntactic validation, and semantic validation of mzQC files.
- [rmzqc](https://github.com/MS-Quality-Hub/rmzqc): R library to create, process, and validate mzQC files.
It includes a R object model, (de-)serialisation functions, syntactic validation, and semantic validation of mzQC files. In development.

If you are looking for a home to your QC software or library, check out [MS-Quality-Hub](https://github.com/MS-Quality-Hub). All the above libraries have their development home there and some other very useful repositories.

Metrics generating software:

- [OpenMS](https://github.com/OpenMS/OpenMS): Open-source software C++ library for LC/MS data management and analyses.
- [PTXQC](https://github.com/cbielow/PTXQC): An R package for creation of QC reports from MaxQuant results and OpenMS mzTab files.
- [QCCalculator](https://github.com/bigbio/qccalculator): Python tool for base QC metric calculation from mzML, mzIdentML, and MaxQuant input files.
- [Yamato / SwaMe / Prognosticator](https://github.com/PaulBrack/Yamato): SWATH-MS QC metrics generation tools.
