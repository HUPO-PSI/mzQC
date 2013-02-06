#!/usr/bin/env python

import os, sys
import shutil
import base64
import sqlite3
from xml.dom import minidom

# qcML object definition
class CV:
    def __init__(self, id):
        self.id = id
        self.version = ""
        self.fullName = ""
        self.uri = ""
        self.sqliteId = None
        
    def printout(self):
        print "\t\t - CV:"
        print "\t\t\t CV.id = " + self.id
        if self.version:
            print "\t\t\t CV.version = " + self.version
        if self.fullName:
            print "\t\t\t CV.fullName = " + self.fullName
        if self.uri:
            print "\t\t\t CV.uri = " + self.uri

    def toSQLite(self, cursor):
        # TODO check if already exists
        cursor.execute("select CV_ID_PK from cv where id=:id ;", {"id":self.id})        
        result = cursor.fetchone()
        if result:
            self.sqliteId = result[0]
        else:
            cursor.execute("insert into cv(id, full_name, version, uri) values (:id, :full_name, :version, :uri);", 
                          {"id":self.id, "full_name":self.fullName, "version":self.version, "uri":self.uri})
            cursor.execute('SELECT last_insert_rowid()')
            self.sqliteId = cursor.fetchone()[0]
        return self.sqliteId
         
class AbstractParam:
    def __init__(self):
        self.name = ""
        self.value = ""
        self.unitName = ""
        self.unitAccession = ""
        self.unitCvRef = ""
        self.sqliteId = None

class CVParam(AbstractParam):
    def __init__(self, dictionary):
        AbstractParam.__init__(self)
        self.accession = ""
        self.cvRef = ""
        self.value = ""
        self.accession = ""
        self.unitName = ""
        self.unitAccession = ""
        self.unitCvRef = ""
        self.fromDict(dictionary)
        
    def fromDict(self, dictionary):
        self.name = dictionary['name']
        if 'value' in dictionary.keys():
            self.value = dictionary['value']
        if 'accession' in dictionary.keys():
            self.accession = dictionary['accession']
        if 'unitName' in dictionary.keys():
            self.unitName = dictionary['unitName']
        if 'unitAccession' in dictionary.keys():
            self.unitAccession = dictionary['unitAccession']
        if 'unitCvRef' in dictionary.keys():
            self.unitCvRef = dictionary['unitCvRef']
        self.cvRef = dictionary['cvRef']
        
    def printout(self):
        print '\t\t\t - ' + self.__class__.__name__ + ':'
        print '\t\t\t\t name = ' + self.name
        if self.value:
            print '\t\t\t\t value = ' + self.value
        print '\t\t\t\t accession = ' + self.accession
        if self.unitName:
            print '\t\t\t\t unitName = ' + self.unitName
        if self.unitAccession:
            print '\t\t\t\t unitAccession = ' + self.unitAccession
        if self.unitCvRef:
            print '\t\t\t\t unitCvRef = ' + self.unitCvRef
        if self.cvRef:
            print '\t\t\t\t cvRef = ' + self.cvRef            

class AttachmentParam(CVParam):
    def __init__(self, dictionary, binary):
        CVParam.__init__(self, dictionary)
        self.readBinary(binary)
        self.qualityParameterRef = ""
        self.fromDict(dictionary)
        
    def fromDict(self, dictionary):
        CVParam.fromDict(self, dictionary)
        if 'qualityParameterRef' in dictionary.keys():
            self.qualityParameterRef = dictionary['qualityParameterRef']
        
    
    def readBinary(self, text):
        if len(text)>1:
            self.binary = text.encode("base64")
        else:
            self.binary = None   
    
    def printout(self):
        CVParam.printout(self)
        print '\t\t\t\t binary = "' + self.binary[0:20] + '..."'
        if self.qualityParameterRef:
            print '\t\t\t\t qualityParameterRef = ' + self.qualityParameterRef            
            
    def toSQLite(self, cursor, assessment_pk, cv_list):
        cv_ref_sqlite_id = None
        unit_cv_ref_sqlite_id = None
        for cv in cv_list:
            if self.cvRef:
                if cv.id == self.cvRef:
                    cv_ref_sqlite_id = cv.sqliteId
            if self.unitCvRef:
                if cv.id == self.unitCvRef:
                    unit_cv_ref_sqlite_id = cv.sqliteId

        cursor.execute("insert into attachment_parameter (name, value, accession, unit_name, unit_accession, cv_ref, unit_cv_ref, QA_ID_FK, binary, quality_parameter_ref)  \
                        values (:name, :value, :accession, :unit_name, :unit_accession, :cv_ref, :unit_cv_ref, :QA_ID_FK, :binary, :quality_parameter_ref);", 
                        {"name": self.name,"value": self.value,"accession": self.accession, "unit_name": self.unitName,"unit_accession": self.unitAccession,
                         "cv_ref":cv_ref_sqlite_id,"unit_cv_ref":unit_cv_ref_sqlite_id ,"QA_ID_FK":assessment_pk, "binary":self.binary, "quality_parameter_ref":self.qualityParameterRef})
        cursor.execute('SELECT last_insert_rowid()')
        
        self.sqliteId = cursor.fetchone()[0]
        return self.sqliteId

class QualityParameter(CVParam):
    def __init__(self, dictionary):
        CVParam.__init__(self, dictionary)
        self.id = ""
        self.flag = None # Boolean
        # self.thresholdFilename = ""
        # self.threshold = none # CVParam
        self.fromDict(dictionary)
        
    def fromDict(self, dictionary):
        CVParam.fromDict(self, dictionary)
        if 'ID' in dictionary.keys():
            self.id = dictionary['ID']
        if 'flag' in dictionary.keys():
            self.flag = bool(dictionary['flag'])
        #if 'thresholdFilename' in dictionary.keys():
        #    self.thresholdFilename = dictionary['thresholdFilename']   
        
    def printout(self):
        CVParam.printout(self)
        if self.id:
            print '\t\t\t\t id = ' + self.id            
        if self.flag:
            print '\t\t\t\t flag = ' + str(self.flag)
        # TODO print '\t\t\t\t thresholdFilename = "' + thresholdFilename.
        # TODO print '\t\t\t\t thresholdFilename = "' + self.threshold 
    
    def toSQLite(self, cursor, assessment_pk, cv_list):
        cv_ref_sqlite_id = None
        unit_cv_ref_sqlite_id = None
        for cv in cv_list:
            if self.cvRef:
                if cv.id == self.cvRef:
                    cv_ref_sqlite_id = cv.sqliteId
            if self.unitCvRef:
                if cv.id == self.unitCvRef:
                    unit_cv_ref_sqlite_id = cv.sqliteId

        cursor.execute("insert into quality_parameter (id, name, value, accession, unit_name, unit_accession, cv_ref, unit_cv_ref, QA_ID_FK)  \
                        values (:id, :name, :value, :accession, :unit_name, :unit_accession, :cv_ref, :unit_cv_ref, :QA_ID_FK);", 
                        {"id":self.id, "name": self.name,"value": self.value,"accession": self.accession,
                         "unit_name": self.unitName,"unit_accession": self.unitAccession,"cv_ref":cv_ref_sqlite_id,"unit_cv_ref":unit_cv_ref_sqlite_id ,
                         "QA_ID_FK":assessment_pk})
        cursor.execute('SELECT last_insert_rowid()')
        self.sqliteId = cursor.fetchone()[0]
        print "\t - qp_pk = " + str(self.sqliteId) 
        return self.sqliteId

class QualityAssessment:
     def __init__(self, isSet = False):
        self.isSet = isSet
        self.paramList = []
        self.sqliteId = None
    
     def toSQLite(self, cursor, mzquality_pk, cv_list):
        cursor.execute("insert into quality_assessment(is_set, MQ_ID_FK) values (:is_set, :MQ_ID_FK);", {"is_set":int(self.isSet), "MQ_ID_FK":mzquality_pk})
        cursor.execute('SELECT last_insert_rowid()')
        self.sqliteId = cursor.fetchone()[0]
        print "\t - assessment_pk = " + str(self.sqliteId)   
        for param in self.paramList:
            param.toSQLite(c, self.sqliteId, cv_list)      
        return self.sqliteId
            
class MzQuality:
    def __init__(self, qcml_file):
        self.mzQualMLFile = qcml_file
        self.runQualityAssessmentList = []  # QualityAssessment list
        self.setQualityAssessmentList = [] # QualityAssessment list
        self.cvList = []
        self.sqliteId = None
        
    def getUniqueCVList(self):        
        def getCVfromList(param_list, cvList):
            def cvInList(id, cvList):
                for item in cvList:
                    if item.id == id:
                        return True
                return False        
            for param in param_list:
                if param.unitCvRef:
                    if not cvInList(param.unitCvRef, cvList):
                        cvList += [CV(param.unitCvRef)]
                if param.cvRef:
                    if not cvInList(param.cvRef, cvList):
                        cvList += [CV(param.cvRef)]
            return cvList
        cvList = []
        for assessment in self.runQualityAssessmentList:
            cvList = getCVfromList(assessment.paramList, cvList)
        for assessment in self.setQualityAssessmentList:
            cvList = getCVfromList(assessment.paramList, cvList)
        self.cvList = cvList
        return self.cvList    
    
    def printout(self):
        def print_params(paramList):
            print '\t\t - paramList: '
            for param in paramList:
                param.printout()                    

        print 'MzQuality:'
        print '\t mzQualMLFile = ' + self.mzQualMLFile
        
        print "\t - CVList: " 
        for item in self.cvList:
            item.printout()

        for assessment in self.runQualityAssessmentList + self.setQualityAssessmentList:
            if not assessment.isSet:
                print '\t - RunQualityAssessment:'   
            else:
                print '\t - SetQualityAssessment:'
            print '\t\t isSet = ' + str(assessment.isSet)
            print_params(assessment.paramList)
            
    def toSQLite(self, cursor):
        cursor.execute("insert into mzquality(mzqualml_file) values (:file);", {"file":self.mzQualMLFile})
        cursor.execute('SELECT last_insert_rowid()')
        mzquality_pk = cursor.fetchone()[0]
        self.sqliteId = mzquality_pk
        print "mzquality_pk = " + str(mzquality_pk)
        
        for cv in self.cvList:
            cv_pk = cv.toSQLite(cursor)
            print "\t - cv_pk = " + str(cv_pk) 
            cursor.execute("insert into cv_list(MQ_ID_FK, CV_ID_FK) values (:MQ_ID_FK, :CV_ID_FK);", {"MQ_ID_FK":mzquality_pk, "CV_ID_FK":cv_pk})
            print "\t - cl_pk = (" + str(mzquality_pk) + ", " + str(cv_pk) + ")"
            
        for assessment in self.runQualityAssessmentList + self.setQualityAssessmentList:
            assessment_pk = assessment.toSQLite(c,mzquality_pk, self.cvList)
        return mzquality_pk

# Methods
def getParamDict(param_list):
    param_dict = {}
    for (name, value) in param_list:
        print '\t\t %s  = %s' % (name, value)
        param_dict[name] = value
    return param_dict

def getBinary(binary_list):
    binary = ""
    if binary_list:
        binary = binary_list[0].firstChild.nodeValue
        print '\t\t binary: "' + binary_list[0].firstChild.nodeValue[0:20] + '..."'
    return binary

def parseParamList(paramlist):
    resultlist = []
    for param in paramlist:
        print '\t QualityParameter:'
        resultlist += [QualityParameter(getParamDict(param.attributes.items()))]
    return resultlist

def parseAttachmentList(attachmentlist):
    resultlist = []
    for attachment in attachmentlist:
        print '\t Attachment:'         
        resultlist += [AttachmentParam(getParamDict(attachment.attributes.items()), 
                       getBinary(attachment.getElementsByTagName('binary')))]
    return resultlist

# Conversion script starts   
# 1. Parse the qcML file
qcml_file = sys.argv[1]
xmldoc = minidom.parse(qcml_file)
mzQuality = MzQuality(qcml_file)

# 2. Build MzQuality object 
print "\n ####### qcML file #######"
# Run Quality
quality_assessments = xmldoc.getElementsByTagName('RunQuality') 
if quality_assessments:
    for assessment in quality_assessments :
        print 'RunQuality:'
        runQuality = QualityAssessment(isSet = False)
        runQuality.paramList += parseParamList(assessment.getElementsByTagName('QualityParameter'))
        runQuality.paramList += parseAttachmentList(assessment.getElementsByTagName('Attachment'))
        mzQuality.runQualityAssessmentList += [runQuality]

# Set Quality
quality_assessments = xmldoc.getElementsByTagName('SetQuality') 
if quality_assessments :
    for assessment in quality_assessments :
        print 'SetQuality:'
        setQuality = QualityAssessment(isSet = True)
        setQuality.paramList += parseParamList(assessment.getElementsByTagName('QualityParameter'))
        setQuality.paramList += parseAttachmentList(assessment.getElementsByTagName('Attachment'))        
        mzQuality.setQualityAssessmentList += [setQuality]

if len(mzQuality.cvList)==0:
    mzQuality.getUniqueCVList()

# Print MzQuality object
print "\n ####### MzQuality object #######"
mzQuality.printout()

# 3. Export it to SQLite
print "\n ####### SQLite database #######"
if len(sys.argv) < 3:
    db_name = os.path.splitext(qcml_file)[0] + ".db"
else:
    db_name = sys.argv[2]
print 'SQLite database: ' + db_name

# Connect to the database 
conn = sqlite3.connect(db_name)
c = conn.cursor()

# Create tables
sql = 'CREATE TABLE IF NOT EXISTS mzquality (MQ_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, mzqualml_file VARCHAR(45) NULL);'
c.execute(sql)
sql = 'CREATE TABLE IF NOT EXISTS quality_assessment (QA_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, is_set INTEGER(1) NOT NULL DEFAULT 0, MQ_ID_FK INTEGER NOT NULL, FOREIGN KEY (MQ_ID_FK) REFERENCES mzquality (MQ_ID_PK));'
c.execute(sql)
sql = 'CREATE TABLE IF NOT EXISTS cv (CV_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, id VARCHAR(45) UNIQUE NOT NULL, full_name VARCHAR(45) NULL, version VARCHAR(45) NULL, uri VARCHAR(45) NULL);'
c.execute(sql)
# ID unique?? sql = 'CREATE TABLE IF NOT EXISTS quality_parameter (QP_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, id VARCHAR(45) UNIQUE NOT NULL, name VARCHAR(45) NOT NULL, value VARCHAR(45) NULL, accession VARCHAR(45) NULL, unit_name VARCHAR(45) NULL, unit_accession VARCHAR(45) NULL, cv_ref INTEGER NOT NULL, unit_cv_ref INTEGER NULL, QA_ID_FK INTEGER NOT NULL, FOREIGN KEY (unit_cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (QA_ID_FK) REFERENCES quality_assessment (QA_ID_PK));'
sql = 'CREATE TABLE IF NOT EXISTS quality_parameter (QP_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, id VARCHAR(45) NOT NULL, name VARCHAR(45) NOT NULL, value VARCHAR(45) NULL, accession VARCHAR(45) NULL, unit_name VARCHAR(45) NULL, unit_accession VARCHAR(45) NULL, cv_ref INTEGER NOT NULL, unit_cv_ref INTEGER NULL, QA_ID_FK INTEGER NOT NULL, FOREIGN KEY (unit_cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (QA_ID_FK) REFERENCES quality_assessment (QA_ID_PK));'
c.execute(sql)
# id unique?? sql = 'CREATE TABLE IF NOT EXISTS attachment_parameter (AP_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, name VARCHAR(45) NOT NULL, value VARCHAR(45) NULL, unit_name VARCHAR(45) NULL, unit_accession VARCHAR(45) NULL, accession VARCHAR(45) NULL, binary BLOB NOT NULL, unit_cv_ref INTEGER NULL, cv_ref INTEGER NOT NULL, quality_parameter_ref VARCHAR(45) NULL, QA_ID_FK INTEGER NOT NULL, FOREIGN KEY (unit_cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (quality_parameter_ref ) REFERENCES quality_parameter (id ), FOREIGN KEY (QA_ID_FK ) REFERENCES quality_assessment (QA_ID_PK ));'
sql = 'CREATE TABLE IF NOT EXISTS attachment_parameter (AP_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, name VARCHAR(45) NOT NULL, value VARCHAR(45) NULL, unit_name VARCHAR(45) NULL, unit_accession VARCHAR(45) NULL, accession VARCHAR(45) NULL, binary BLOB NOT NULL, unit_cv_ref INTEGER NULL, cv_ref INTEGER NOT NULL, quality_parameter_ref VARCHAR(45) NULL, QA_ID_FK INTEGER NOT NULL, FOREIGN KEY (unit_cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (QA_ID_FK ) REFERENCES quality_assessment (QA_ID_PK ));'
c.execute(sql)
sql = 'CREATE TABLE IF NOT EXISTS cv_list (MQ_ID_FK INTEGER NOT NULL, CV_ID_FK INTEGER NOT NULL, PRIMARY KEY (MQ_ID_FK, CV_ID_FK), FOREIGN KEY (MQ_ID_FK ) REFERENCES mzquality (MQ_ID_PK ) FOREIGN KEY (CV_ID_FK ) REFERENCES cv (CV_ID_PK ));'
c.execute(sql)

# Insert data
mzquality_pk = mzQuality.toSQLite(c)

# Save (commit) the changes and close the connection
conn.commit()
conn.close()

print 'Finished! To access the generated qcDB file execute: sqlite3 ' + db_name


