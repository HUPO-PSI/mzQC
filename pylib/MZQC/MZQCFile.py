__author__ = 'walzer'
import json
import operator
from datetime import datetime
from typing import List,Dict,Union,Any,Tuple

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
    mappings: Dict[str, Any] = dict()

    @classmethod
    def class_mapper(classself, d):
        maxcls: Any = None
        exmax: int = 0 
        for keys, cls in classself.mappings.items():
            if keys.issuperset(d.keys()):
                nx = len(set(d.keys()).intersection(set(keys)))
                if nx > exmax:
                    maxcls = cls
                    exmax = nx
        
        if maxcls != None:
            return maxcls(**d)
        else:
            if {'creationDate': None}.keys() == d.keys():
                return datetime.strptime(d['creationDate'], '%Y-%m-%dT%H:%M:%S')
            else:
                # raise ValueError('Unable to find a matching class for object: {d} (keys: {k})' .format(d=d,k=d.keys()))
                return d

    @classmethod
    def complex_handler(classself, obj):
        if hasattr(obj, '__dict__'):
            return {k:v for k,v in obj.__dict__.items() if v is not None and v is not ""}

        elif isinstance(obj, datetime):
             return obj.replace(microsecond=0).isoformat()
        else:
            raise TypeError('Object of type {ty} with value {val} is not JSON (de)serializable'.format(ty=type(obj), val=repr(obj)))

    @classmethod
    def register(classself, cls):
        classself.mappings[frozenset(tuple([attr for attr, val in cls().__dict__.items()]))] = cls
        return cls

    @classmethod
    def ToJson(classself, obj, readability=0):
        if readability==0:
            return json.dumps(obj.__dict__, default=classself.complex_handler)
        elif readability == 1:
            return json.dumps(obj.__dict__, default=classself.complex_handler, indent=2, cls=MzqcJSONEncoder)
        else:
            return json.dumps(obj.__dict__, default=classself.complex_handler, indent=4)

    # N.B.: for this to work the class init variables must be same name as the corresponding member attributes (self.)
    @classmethod
    def FromJson(classself, json_str):
        j = json.loads(json_str, object_hook=classself.class_mapper)
        return rectify(j)

def rectify(obj):
    static_list_typemap = {'runQualities': RunQuality, 'setQualities': SetQuality, 'controlledVocabularies': ControlledVocabulary, 
            'qualityMetrics': QualityMetric, 'inputFiles': InputFile, 'analysisSoftware': AnalysisSoftware, 'fileProperties': CvParameter}
    static_singlet_typemap = {'fileFormat': CvParameter, 'metadata': MetaDataParameters}
    if hasattr(obj, '__dict__'):
        for k,v in obj.__dict__.items():
            if k in static_list_typemap.keys():
                v = [rectify((static_list_typemap[k])(**i.__dict__ if hasattr(i, '__dict__') else i)) for i in v]
            elif k in static_singlet_typemap.keys():
                k = rectify((static_singlet_typemap[k])(**v.__dict__ if hasattr(v, '__dict__') else v))
    return obj


class MzqcJSONEncoder(json.JSONEncoder):
  def iterencode(self, o, _one_shot=False):
    indent_level = 0
    value_scope = False
    for s in super(MzqcJSONEncoder, self).iterencode(o, _one_shot=_one_shot):
        if value_scope and indent_level == 0 and s.startswith('}'):
            value_scope = False
        elif s.startswith('"value"'):
            value_scope = True
        if 0 < indent_level:
            s = s.replace('\n', '').rstrip().lstrip()
            if s.startswith(','):
                s = ',' + s[1:].lstrip()
        if s.startswith('[') and value_scope:
            indent_level += 1
        if s.endswith(']') and value_scope:
            indent_level -= 1
            s = s.replace(']', '\n'+' '*self.indent*6+']').rstrip()
        yield s


class jsonobject(object):
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, __class__):
            # TODO find difference in keys and check whether they are None or "" in the other or vice versa
            snn = [k for k,v in self.__dict__.items() if (not v == None and not v == "")]
            onn = [k for k,v in other.__dict__.items() if (not v == None and not v == "")]
            if set(snn) == set(onn):
                return all([self.__getattribute__(attr) == other.__getattribute__(attr) for attr in self.__dict__.keys()])
        return False

@JsonSerialisable.register
class ControlledVocabulary(jsonobject):
    def __init__(self, ref: str="", name: str="", uri: str="", version: str=""):
        self.ref = ref  # not in schema
        self.name = name  # required
        self.uri = uri  # required
        self.version = version  # optional

@JsonSerialisable.register
class CvParameter(jsonobject):
    def __init__(self, cvRef: str="", 
                       accession: str="", 
                       name: str="", 
                       description: str="", 
                       value: Union[int,str,float,IntVector,StringVector,FloatVector,IntMatrix,StringMatrix,FloatMatrix,Table, None]=None,
                       unit: str=""):
        self.cvRef = cvRef  # required
        self.accession = accession  # required "pattern": "^[A-Z]+:[0-9]{7}$"
        self.name = name  # required
        self.description = description  # optional, "pattern": "^[A-Z]+$"
        self.value = value  # optional
        self.unit = unit  # optional, IMO this should be accession only, not annother cvParam

@JsonSerialisable.register
class AnalysisSoftware(CvParameter):
    def __init__(self, cvRef: str="", 
                       accession: str="", 
                       name: str="", 
                       description: str="", 
                       value: str="", 
                       unit: str="", 
                       version: str = "", 
                       uri: str = ""):
        super().__init__(cvRef, accession, name, description, value, unit)  # optional, this will set None to optional omitted arguments
        self.version = version  # required
        self.uri = uri  # required

@JsonSerialisable.register
class InputFile(jsonobject):
    def __init__(self, location: str = "", 
                    name: str = "", 
                    fileFormat: CvParameter = None, 
                    fileProperties: List[CvParameter] = None):
        self.location = location  # required , uri
        self.name = name  # required , string (doubles as internal and external ref anchor?)
        self.fileFormat = fileFormat  # required , cvParam
        self.fileProperties = [] if fileProperties is None else fileProperties  # optional, cvParam, at least one item

@JsonSerialisable.register
class MetaDataParameters(jsonobject):
    def __init__(self, 
                    # fileProvenance: str="", 
                    # cv_params: List[CvParameter] = None ,
                    inputFiles: List[InputFile] = None, 
                    analysisSoftware: List[AnalysisSoftware]=None 
                ):
        # self.fileProvenance = fileProvenance  # not in schema
        # self.cv_params = [] if cv_params is None else cv_params  # not in schema, IMO should be in there
        self.inputFiles =  [] if inputFiles is None else inputFiles  # required
        self.analysisSoftware = [] if analysisSoftware is None else analysisSoftware  # required
        
    # schema: at least one input_file in input_files
    # schema: at least one analysis_software in analysis_software 

@JsonSerialisable.register
class QualityMetric(CvParameter):
    pass
    # def __init__(self, cvRef: str="", 
    #                 accession: str="", 
    #                 name: str="", 
    #                 description: str="", 
    #                 value: Union[int,str,float,IntVector,StringVector,FloatVector,IntMatrix,StringMatrix,FloatMatrix,Table, None]=None,  # here we could clamp down on allowed value types
    #                 unit: str=""):
    #     super().__init__(cvRef, accession, name, description, value, unit)  # optional, this will set None to optional omitted arguments
    # schema: is cvParam object 
    # schema: do we allow no-value metrics? cvParam value attribute is optional
    # implementation: this is a different object class because we want to make semantical distinctions between pure metrics and generic CvParams

@JsonSerialisable.register
class BaseQuality(jsonobject):
    def __init__(self, metadata: MetaDataParameters=None, 
                    qualityMetrics: List[QualityMetric]=None):
        self.metadata = metadata  # required
        self.qualityMetrics = [] if qualityMetrics is None else qualityMetrics  # reuired,
    # schema: at least one item in quality_metrics

@JsonSerialisable.register
class RunQuality(BaseQuality):
    pass

@JsonSerialisable.register
class SetQuality(BaseQuality):
    pass
    
@JsonSerialisable.register
class MzQcFile(jsonobject):
    def __init__(self, creationDate: Union[datetime,str] = datetime.now().replace(microsecond=0), version: str = "0.0.11",  
                    runQualities: List[RunQuality]=None, 
                    setQualities: List[SetQuality]=None, 
                    controlledVocabularies: List[ControlledVocabulary]=None 
                    ):
        self.creationDate = datetime.strptime(creationDate, '%Y-%m-%dT%H:%M:%S') if isinstance(creationDate, str) else creationDate  # not in schema, IMO should be
        self.version = version
        self.runQualities = [] if runQualities is None else runQualities
        self.setQualities = [] if setQualities is None else setQualities
        self.controlledVocabularies = [] if controlledVocabularies is None else controlledVocabularies  # required
    # schema: at least one cv in controlled_vocabularies
    # schema: at least one of run_qualities or set_qualities
    # schema: at least one item in run_qualities or set_qualities


