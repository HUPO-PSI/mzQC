__author__ = 'walzer'
import json
from datetime import datetime
from typing import List,Dict,Union,NewType,Any

#int
#str
#float
FloatVector = List[float]
IntVector = List[int]
StringVector = List[str]
FloatMatrix = List[FloatVector]
IntMatrix = List[IntVector]
StringMatrix = List[StringVector]
#Table = Dict[str,Union(FloatVector,IntVector,StringVector)]
Table = Dict[str,List]

class JsonSerialisable(object):
    mappings = dict()

    @classmethod
    def class_mapper(classself, d):
        for keys, cls in classself.mappings.items():
            if keys.issuperset(d.keys()):
                return cls(**d)
        else:
            import collections
            if {'__datetime__': None}.keys() == d.keys():
                return datetime.strptime(d['__datetime__'], '%Y-%m-%dT%H:%M:%S')
            else:
                raise ValueError('Unable to find a matching class for object: {d} (keys: {k})' .format(d=d,k=d.keys()))

    @classmethod
    def complex_handler(classself, Obj):
        if hasattr(Obj, '__dict__'):
            return Obj.__dict__
        elif isinstance(Obj, datetime):
             return {'__datetime__': Obj.replace(microsecond=0).isoformat()}
        else:
            raise TypeError('Object of type {ty} with value {val} is not JSON (de)serializable'.format(ty=type(Obj), val=repr(Obj)))

    @classmethod
    def register(classself, cls):
        classself.mappings[frozenset(tuple([attr for attr, val in cls().__dict__.items()]))] = cls
        return cls

    @classmethod
    def ToJson(classself, obj):
        return json.dumps(obj.__dict__, default=classself.complex_handler, indent=4)

    @classmethod
    def FromJson(classself, json_str):
        return json.loads(json_str, object_hook=classself.class_mapper)

@JsonSerialisable.register
class ControlledVocabulary(object):
    def __init__(self, ref: str="", name: str="", uri: str="", version: str=""):
        self.ref = ref  # not in schema
        self.name = name  # required
        self.uri = uri  # required
        self.version = version  # optional

@JsonSerialisable.register
class CvParameter(object):
    def __init__(self, cv_ref: str="", 
                       accession: str="", 
                       name: str="", 
                       description: str="", 
                       value: str="", 
                       unit: str=""):
        self.cvRef = cv_ref  # required
        self.accession = accession  # required "pattern": "^[A-Z]+:[0-9]{7}$"
        self.name = name  # required
        self.description = description  # optional, "pattern": "^[A-Z]+$"
        self.value = value  # optional
        self.unit = unit  # optional, IMO this should be accession only, not annother cvParam

@JsonSerialisable.register
class AnalysisSoftware(CvParameter):
    def __init__(self, cv_ref: str="", 
                       accession: str="", 
                       name: str="", 
                       description: str="", 
                       value: str="", 
                       unit: str="", 
                       version: str = "", 
                       uri: str = ""):
        super().__init__(cv_ref, accession, description, value, unit)  # optional, this will set None to optional omitted arguments
        self.version = version  # required
        self.uri = uri  # required

@JsonSerialisable.register
class InputFiles(object):
    def __init__(self, location: str = "", 
                    name: str = "", 
                    file_format: CvParameter = None, 
                    file_properties: List[CvParameter] = None):
        self.location = location  # required , uri
        self.name = name  # required , string (doubles as internal and external ref anchor?)
        self.file_format = file_format  # required , cvParam
        self.file_properties = [] if file_properties is None else file_properties  # optional, cvParam, at least one item

@JsonSerialisable.register
class MetaDataParameters(object):
    def __init__(self, 
                    file_provenance: str="", 
                    input_files: List[InputFiles] = None, 
                    analysis_software: List[AnalysisSoftware]=None, 
                    cv_params: List[CvParameter] = None
                ):
        self.file_provenance = file_provenance  # not in schema
        self.input_files =  [] if input_files is None else input_files  # required
        self.analysis_software = [] if analysis_software is None else analysis_software  # required
        self.cv_params = [] if cv_params is None else cv_params  # not in schema, IMO should be in there
    # schema: at least one input_file in input_files
    # schema: at least one analysis_software in analysis_software 

@JsonSerialisable.register
class QualityMetric(object):
    def __init__(self, cv_ref: str="", 
                    accession: str="", 
                    name: str="", 
                    value: Union[int,str,float,IntVector,StringVector,FloatVector,IntMatrix,StringMatrix,FloatMatrix,Table]=None,
                    unit: str=""):
        self.cv_ref = cv_ref
        self.accession = accession
        self.name = name
        self.value = Union[int,str,float,IntVector,StringVector,FloatVector,IntMatrix,StringMatrix,FloatMatrix,Table] if value is None else value
    # schema: is cvParam object 
    # schema: do we allow no-value metrics? cvParam value attribute is optional

@JsonSerialisable.register
class BaseQuality(object):
    def __init__(self, metadata: MetaDataParameters=None, 
                    quality_metrics: List[QualityMetric]=None):
        self.metadata = metadata  # required
        self.quality_metrics = [] if quality_metrics is None else quality_metrics  # reuired,
    # schema: at least one item in quality_metrics

@JsonSerialisable.register
class RunQuality(BaseQuality):
    pass

@JsonSerialisable.register
class SetQuality(BaseQuality):
    pass
    
@JsonSerialisable.register
class MzQcFile(object):
    def __init__(self, creationtime: datetime = datetime.now(), version: str = "0.0.11",  
                    run_qualities: List[RunQuality]=None, 
                    set_qualities: List[SetQuality]=None, 
                    controlled_vocabularies: List[ControlledVocabulary]=None 
                    ):
        # self.schemaLocation = "/home/walzer/psi/qcML-development/schema/v0_0_10/qcML_0_0_10.xsd"
        self.creationtime = datetime.now() if creationtime is None else creationtime  # not in schema, IMO should be
        self.version = version
        self.run_qualities = [] if run_qualities is None else run_qualities
        self.set_qualities = [] if set_qualities is None else set_qualities
        self.controlled_vocabularies = [] if controlled_vocabularies is None else controlled_vocabularies  # required
    # schema: at least one cv in controlled_vocabularies
    # schema: at least one of run_qualities or set_qualities
    # schema: at least one item in run_qualities or set_qualities


