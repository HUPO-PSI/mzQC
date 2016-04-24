#Welcome to the PSI-QC working group repository.

##Focus and Purpose of the working group
The PSI-QC working group is composed of academic, government, and industry researchers, software developers, journal representatives, and instrument manufacturers. The main goal of the PSI-QC working group is to define a community data format and associated controlled vocabulary terms, facilitating data exchange and archiving of mass spectrometry derived quality control metrics.
Current projects of the PSI-QC working group are:
 - The qcML format, which has been developed as a standardized format for the exchange, transmission, and archiving of quality control metrics derived from mass spectrometry.
 - Controlled Vocabulary development: controlled vocabulary terms are developed in common with the PSI-MS and PSI-PI groups.
 
##The Repository
The repository facilitates the collaborative work 
 
###Structure of the repository
Folder structure is organized by function. There are three main development folders for:
 - The Schema development
 - The CV development
 - The Specification Document development
 In addition, there are folders for deprecated stuff and advanced documentation.
 
####Schema development
This folders substructure is by version. Each version should contain the following:
 - Its folder name corresponding to the version
 - The schema XSD file 
 - A folder for images to be contained in the documentation process (e.g. schema visualisation)
 - A folder for examples qcML files

####Specification Document development
This folder should contain the text files containing the Specification Document content. These should be plain text files with Markdown. Markdown can be easily edited and formatted with a plethora of tools, not least with the GitHub built in editor. Markdown is easily converted to .pdf, .docx, etc. Most importantly it allows content version control and GitHub rendering.
 
####CV development
This folder should contain a OBO file with the representation of QC metrics. The file shall be hierarchically structured and in plain text. Additionally, there should be a documentation file, with detailed explanation of the cv terms, examples, visualizations and/or script snippets to calculate the metrics.

##Contribute
You are welcome to contribute. The easiest way is to file an issue within GitHub. If you want to propose changes, follow the Git workflow (described here).