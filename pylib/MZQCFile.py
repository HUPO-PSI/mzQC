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
    mappings = Dict[Any,Any]

    @classmethod
    def class_mapper(classself, d):
        for keys, cls in classself.mappings.items():
            if keys.issuperset(d.keys()):
                return cls(**d)
        else:
            # Raise exception instead of silently returning None
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
    def __init__(self, id: str="", name: str="", uri: str="", version: str=""):
        self.id = id
        self.name = name
        self.uri = uri  # uri obviously
        self.version = version  # optional

@JsonSerialisable.register
class CvParam(object):
    def __init__(self, cv_ref: str="", 
                       accession: str="", 
                       name: str="", 
                       description: str="", 
                       value: str="", 
                       unit: str=""):
        self.cv_ref = cv_ref  # required
        self.accession = accession  # required "pattern": "^[A-Z]+:[0-9]{7}$"
        self.name = name  # required
        self.description = description  # "pattern": "^[A-Z]+$"
        self.value = value
        self.unit = unit  # IMO this should be accession only, not annother cvParam

	# "unit": {
	# 	"description": "A CV element describing the unit of the parameter value.",
	# 	"anyOf": [
	# 		{
	# 			"$ref": "#/definitions/cvParameter"
	# 		},
	# 		{
	# 			"type": "array",
	# 			"minItems": 1,
	# 			"items": {
	# 				"$ref": "#/definitions/cvParameter"
	# 			}
	# 		}
	# 	]
	# }

@JsonSerialisable.register
class AnalysisSoftware(CvParam):
    def __init__(self, cv_ref: str="", 
                       accession: str="", 
                       name: str="", 
                       description: str="", 
                       value: str="", 
                       unit: str="", 
                       version: str = "", 
                       uri: str = ""):
        super().__init__(cv_ref, accession, description, value, unit)
        self.version = version  # 
        self.uri = uri  # required

	# "analysisSoftware": {
	# 	"description": "Software tool(s) used to generate the QC metrics.",
	# 	"type": "array",
	# 	"minItems": 1,
	# 	"items": {
	# 		"allOf": [
	# 			{
	# 				"$ref": "#/definitions/cvParameter"
	# 			},
	# 			{
	# 				"properties": {
	# 					"version": {
	# 						"description": "Version number of the software tool.",
	# 						"type": "string"
	# 					},
	# 					"uri": {
	# 						"description": "Publicly accessible URI of the software tool.",
	# 						"type": "string",
	# 						"format": "uri"
	# 					}
	# 				},
	# 				"required": ["version", "uri"]
	# 			}
	# 		]
	# 	}

@JsonSerialisable.register
class InputFiles(object):
    def __init__(self, location: str = "", 
                    name: str = "", 
                    file_format: CvParam = None, 
                    file_properties: List[CvParam] = None):
        self.location = location  # required , uri
        self.name = name  # required , string (doubles as internal and external ref anchor?)
        self.file_format = file_format  # required , cvParam
        self.file_properties = [] if file_properties is None else file_properties  # cvParam

@JsonSerialisable.register
class MetaDataParameters(object):
    def __init__(self, file_provenance: str="", 
                    input_files: List[InputFiles] = None, 
                    analysis_software: AnalysisSoftware=None, 
                    cv_params: List[CvParam] = None):
        self.file_provenance = file_provenance  # not in schema
        self.input_files =  [] if input_files is None else input_files
        self.analysis_software = analysis_software
        self.cv_params = [] if cv_params is None else cv_params  # not in schema
    # SHOULD have at least one input file ot property raw/peak file

@JsonSerialisable.register
class QualityMetric(object):
    def __init__(self, id: str="", 
                    cv_ref: str="", 
                    accession: str="", 
                    name: str="", 
                    value: Union[int,str,float,IntVector,StringVector,FloatVector,IntMatrix,StringMatrix,FloatMatrix,Table]=None):
        self.id = id
        self.cv_ref = cv_ref
        self.accession = accession
        self.name = name
        self.value = [] if value is None else value

@JsonSerialisable.register
class BaseQuality(object):
    def __init__(self, id: str="", 
                    metadata: MetaDataParameters=None, 
                    quality_metrics: List[QualityMetric]=None):
        self.id = id
        self.metadata = metadata
        self.quality_metrics = [] if quality_metrics is None else quality_metrics  # "minItems": 1

@JsonSerialisable.register
class RunQuality(BaseQuality):
    pass

@JsonSerialisable.register
class SetQuality(BaseQuality):
    pass
    
@JsonSerialisable.register
class MzQcFile(object):
    def __init__(self, name: str="", 
                    version: str="",  
                    run_qualities: List[RunQuality]=None, 
                    set_qualities: List[SetQuality]=None, 
                    controlled_vocabularies: List[ControlledVocabulary]=None, 
                    creationtime: datetime=None):
        self.name = name
        # self.schemaLocation = "/home/walzer/psi/qcML-development/schema/v0_0_10/qcML_0_0_10.xsd"
        # self.xmlns = "http://www.w3.org/2001/XMLSchema-instance"
        self.version = "0.0.11"
        self.creationtime = datetime.now() if creationtime is None else creationtime
        self.run_qualities = [] if run_qualities is None else run_qualities
        self.set_qualities = [] if set_qualities is None else set_qualities
        self.controlled_vocabularies = [] if controlled_vocabularies is None else controlled_vocabularies


