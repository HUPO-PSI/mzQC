__author__ = 'bittremieux, walzer'
import json
import os
import urllib.request
from typing import Dict, List, Set, Union
from MZQCFile import MzQcFile, BaseQuality, RunQuality, SetQuality, QualityMetric
from itertools import chain

import jsonschema
from pronto import Ontology, Term, TermList
from jsonschema.exceptions import ValidationError

class SemanticError(ValidationError):
    """Base class for exceptions in this module."""
    pass

class SemanticCheck(object):
    def __init__(self, version: str=""):
        self.version = version  
            # with open(filename) as json_in:
                # Syntactic validation of the mzQC file against the JSON schema.
                # instance = json.load(json_in)
                # version = instance['mzQC']['version'].replace('.', '_')

    def _get_cv_parameters(self, val: object):
        if hasattr(val, 'cv_ref'):
            yield val
        elif isinstance(val, List):
            for v in val:
                yield from self._get_cv_parameters(v)
        else:
            for attr, value in vars(val).items():
                yield from self._get_cv_parameters(value)

    def _inputFileConsistency(self, qualities: Union[
                                    List[RunQuality],
                                    List[SetQuality]]):
        for quality in qualities:
            file_names : List[str] = list()
            for input_file in quality.metadata.input_files:
                # filename and location
                infilo = os.path.splitext(
                    os.path.basename(input_file.location))[0]
                if input_file.name != infilo:
                    raise SemanticError(f'Inconsistent file name and location: {input_file.name}/{infilo}')
                # check duplicates 
                if input_file.name not in file_names:
                    file_names.append(input_file.name)
                else:
                    raise SemanticError('Duplicate inputFile: {n}'.format(n=input_file.name))

    def validate(self, mzqc: MzQcFile):
        # Semantic validation of the JSON file.
        # Load the mzqc file specific ontologies
        cvs: Dict[str, TermList] = dict()
        for cv in mzqc.controlled_vocabularies:
            try:
                cvs[cv.ref] = Ontology(cv.uri, False) 
            except:
                SemanticError(f'Failed to load cv {cv.name} from {cv.uri}. Does {cv.ref} exist?')
        
        # For all cv terms involved:
        for cv_parameter in self._get_cv_parameters(mzqc):
            # Verify that cvRefs are valid.
            if cv_parameter.cvRef not in cvs.keys():
                raise SemanticError(f'Unknown CV reference <{cv_parameter.cv_ref}> in ' 
                                    f'element `{str(type(cv_parameter))}`')

            # Verify that the term exists in the CV.
            cv_term = cvs[cv_parameter.cvRef].get(cv_parameter.accession)
            if cv_term is None:
                raise SemanticError(f'Term {cv_parameter.name} not found in CV <{cv_parameter.cvRef}>')

            # Verify that the term name is correct.
            elif cv_parameter.name != cv_term.name:
                raise SemanticError(
                    f'Incorrect name for CV term {cv_parameter.accession}: '
                    f'"{cv_parameter.name}" != "{cv_term.name}"')

        # Regarding metadata, verify that input files are consistent and unique.
        self._inputFileConsistency(mzqc.run_qualities)
        self._inputFileConsistency(mzqc.set_qualities)

        # For all metrics (which are basing on cv type)
        #run_and_set_quality_collection: List[BaseQuality] = list()
        #for run_or_set_quality in run_and_set_quality_collection:
        if "Proteomics Standards Initiative Quality Control Ontology" not in [cv.name for cv in cvs.values()]:
            raise SemanticError(f'Quality Control Ontology missing!')
        else:
            keys = [filter( lambda x: cvs[x].name == "Proteomics Standards Initiative Quality Control Ontology", cvs )]
            if len(keys) != 1:
                SemanticError('More than one QC CV.')
            else:    
                qc_ref = keys[0]
            metric_cvs: List[Term] = cvs[qc_ref]["QC:4000001"].rchildren()
            
        for run_or_set_quality in chain(mzqc.run_qualities,mzqc.set_qualities):
            # Verify that quality metrics are unique within a run/setQuality.
            accessions: Set[str] = set()
            for quality_metric in run_or_set_quality.quality_metrics:
                if quality_metric.accession not in accessions:
                    accessions.add(quality_metric.accession)
                else:
                    raise ValidationError(f'Duplicate quality metric: '
                                          f'accession = {quality_metric.accession}')

                # Verify that quality_metric actually is of metric type/relationship?
                cv_term = cvs[quality_metric.cvRef].get(quality_metric.accession)
                if cv_term is None or cv_term not in metric_cvs:
                    raise SemanticError(f'Non-metric CV used in metric context.')