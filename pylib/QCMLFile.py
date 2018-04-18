__author__ = 'walzer'
import json
from datetime import datetime


class JsonSerialisable(object):
    mappings = dict()

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
class QualityMetric(object):
        def __init__(self, id: str="", cv_ref: str="", accession: str="", name: str="", value: str=""):
            self.id = id
            self.cv_ref = cv_ref
            self.accession = accession
            self.name = name
            self.value = value


@JsonSerialisable.register
class MetaDataParameters(object):
        def __init__(self, file_provenance: str=""):
            self.file_provenance = file_provenance


@JsonSerialisable.register
class RunQuality(object):
    def __init__(self, id: str="", meta_data_parameters: MetaDataParameters=None, quality_metric: [QualityMetric]=None):
        self.id = id
        self.meta_data_parameters = meta_data_parameters
        self.quality_metric = [] if quality_metric is None else quality_metric


@JsonSerialisable.register
class QCMLFile(object):
    def __init__(self, name: str="", run_qualities: [RunQuality]=None, when: datetime=None):
        self.name = name
        # self.schemaLocation = "/home/walzer/psi/qcML-development/schema/v0_0_10/qcML_0_0_10.xsd"
        # self.xmlns = "http://www.w3.org/2001/XMLSchema-instance"
        # self.version = "0.0.10"
        self.when = datetime.now() if when is None else when
        self.run_qualities = run_qualities


# class QCMLEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, datetime):
#             return {'__datetime__': o.replace(microsecond=0).isoformat()}
#         return {'__{}__'.format(o.__class__.__name__): o.__dict__}
#
#     @staticmethod
#     def decode_object(o):
#         if '__QCMLFile__' in o:
#             f = QCMLFile(None)
#             f.__dict__.update(o['__QCMLFile__'])
#             return f
#         elif '__datetime__' in o:
#             return datetime.strptime(o['__datetime__'], '%Y-%m-%dT%H:%M:%S')
#         return o

    # f1 = QCMLFile('f1')
    # f1.data['fileSize'] = 137943558124
    # f2 = QCMLFile('EGAF00001160354')
    # f2.data['159542023740']
    # dump = json.dumps([f1,f2], indent=4, cls=QCMLEncoder)
    # deserialized = json.loads(dump, object_hook=QCMLEncoder.decode_object)

#http://json.org/example.html
#https://www.xml.com/pub/a/2006/05/31/converting-between-xml-and-json.html

# hc = "/home/walzer/psi/pyOpenMSqc/handcrafted_json2.qcML"
# with open(hc) as f:
#     ds = json.loads(f.read())
# with open(hc) as f:
#     deserialized = json.loads(f.read(), object_hook=QCMLFile.QCMLEncoder.decode_object)


import QCMLFile as qc
qc1 = qc.QualityMetric("name123")
qc2 = qc.QualityMetric("id123", "MS", "MS:123", "name123", "123")
qc3 = qc.QualityMetric("id345", "MS", "MS:345", "name345", 1)
qc4 = qc.QualityMetric("id345", "MS", "MS:345", "name345", "{'UO_0000106':[4.34,7.86,7.67,5.26]}")
mp = qc.MetaDataParameters("file.raw")
rc = qc.RunQuality("mp", [qc1,qc2])
rd = qc.RunQuality("mp", [qc3,qc4])
qcml = qc.QCMLFile("mimimi", [rc,rd])

qc.JsonSerialisable.ToJson(rc)
qc.JsonSerialisable.ToJson(rd)
qc.JsonSerialisable.ToJson(mp)


qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(rc))
qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(rd))
qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(mp))


qc.JsonSerialisable.FromJson(qc.JsonSerialisable.ToJson(qcml))

