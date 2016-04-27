#!/usr/bin/env python

import os, sys
import shutil
import base64
import sqlite3
import random
from xml.dom import minidom

DEBUG = False
TABLE_SEPARATOR = " "
XML_HEADER = '<?xml version="1.0" encoding="ISO-8859-1"?>\n<?xml-stylesheet type="text/xml" href="#stylesheet"?>\n<!DOCTYPE catelog [\n  <!ATTLIST xsl:stylesheet\n  id  ID  #REQUIRED>\n  ]>\n'
XMLNS = '"http://www.prime-xs.eu/ms/qcml"' 

# XML Tags
XML_QCML = 'qcML'
XML_CVLIST = 'cvList'
XML_CV = 'cv'
XML_RUN_QUALITY = 'runQuality'
XML_SET_QUALITY = 'setQuality'
XML_QUALITY_PARAMETER = 'qualityParameter'
XML_THRESHOLD = 'threshold'
XML_ATTACHMENT = 'attachment'
XML_BINARY = 'binary'
XML_TABLE = 'table'
XML_TABLE_COLUMN = 'tableColumnTypes'
XML_TABLE_ROW = 'tableRowValues'

# Auxiliary methods
def getParamDict(param_list, offset="\t\t\t"):
    param_dict = {}
    for (name, value) in param_list:
        param_dict[name] = value
    if DEBUG:
        for key in param_dict:
            print offset + ' %s = %s' % (key, param_dict[key])
    return param_dict

def createSQLiteTables(conn):
    # Create tables
    sql = 'CREATE TABLE IF NOT EXISTS qcml (QC_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, qcml_file VARCHAR(45) NULL);'
    conn.execute(sql)
    sql = 'CREATE TABLE IF NOT EXISTS quality_assessment (QA_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, id VARCHAR(45) UNIQUE NOT NULL, is_set INTEGER(1) NOT NULL DEFAULT 0, QC_ID_FK INTEGER NOT NULL, FOREIGN KEY (QC_ID_FK) REFERENCES qcml (QC_ID_PK));'
    conn.execute(sql)
    sql = 'CREATE TABLE IF NOT EXISTS cv (CV_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, id VARCHAR(45) UNIQUE NOT NULL, full_name VARCHAR(45) NULL, version VARCHAR(45) NULL, uri VARCHAR(45) NULL);'
    conn.execute(sql)
    sql = 'CREATE TABLE IF NOT EXISTS cv_list (QC_ID_FK INTEGER NOT NULL, CV_ID_FK INTEGER NOT NULL, PRIMARY KEY (QC_ID_FK, CV_ID_FK), FOREIGN KEY (QC_ID_FK ) REFERENCES qcml (QC_ID_PK ) FOREIGN KEY (CV_ID_FK ) REFERENCES cv (CV_ID_PK ));'
    conn.execute(sql)
    sql = 'CREATE TABLE IF NOT EXISTS quality_parameter (QP_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, id VARCHAR(45) UNIQUE NOT NULL, name VARCHAR(45) NOT NULL, value VARCHAR(45) NULL, accession VARCHAR(45) NULL, unit_name VARCHAR(45) NULL, unit_accession VARCHAR(45) NULL, flag BOOLEAN, cv_ref INTEGER NOT NULL, unit_cv_ref INTEGER NULL, QA_ID_FK INTEGER NOT NULL, FOREIGN KEY (unit_cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (QA_ID_FK) REFERENCES quality_assessment (QA_ID_PK));'
    conn.execute(sql)
    sql = 'CREATE TABLE IF NOT EXISTS threshold (TH_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, name VARCHAR(45) NOT NULL, value VARCHAR(45) NULL, accession VARCHAR(45) NULL, unit_name VARCHAR(45) NULL, unit_accession VARCHAR(45) NULL, cv_ref INTEGER NOT NULL, unit_cv_ref INTEGER NULL, threshold_filename VARCHAR(45), QP_ID_FK INTEGER NOT NULL, FOREIGN KEY (unit_cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (QP_ID_FK) REFERENCES quality_parameter (QP_ID_PK));'
    conn.execute(sql)
    sql = 'CREATE TABLE IF NOT EXISTS attachment_parameter (AP_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, id VARCHAR(45) UNIQUE NOT NULL, name VARCHAR(45) NOT NULL, value VARCHAR(45) NULL, unit_name VARCHAR(45) NULL, unit_accession VARCHAR(45) NULL, accession VARCHAR(45) NULL, binary BLOBs, unit_cv_ref INTEGER NULL, cv_ref INTEGER NOT NULL, quality_parameter_ref VARCHAR(45) NULL, QA_ID_FK INTEGER NOT NULL, FOREIGN KEY (unit_cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (cv_ref ) REFERENCES cv (CV_ID_PK ), FOREIGN KEY (QA_ID_FK ) REFERENCES quality_assessment (QA_ID_PK ));'
    conn.execute(sql)
    sql = 'CREATE TABLE IF NOT EXISTS table_attachment (TA_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, AP_ID_FK INTEGER NOT NULL, FOREIGN KEY (AP_ID_FK) REFERENCES attachment_parameter (AP_ID_PK));'
    conn.execute(sql)
    sql = 'CREATE TABLE IF NOT EXISTS table_column (TC_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, name VARCHAR(100), TA_ID_FK INTEGER NOT NULL, FOREIGN KEY (TA_ID_FK) REFERENCES table_attachment (TA_ID_PK));'
    conn.execute(sql)
    sql = 'CREATE TABLE IF NOT EXISTS table_row (TR_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, row_num INTEGER, TA_ID_FK INTEGER NOT NULL, FOREIGN KEY (TA_ID_FK) REFERENCES table_attachment (TA_ID_PK));'
    conn.execute(sql)
    sql = 'CREATE TABLE IF NOT EXISTS table_value (TV_ID_PK INTEGER PRIMARY KEY ASC AUTOINCREMENT, value VARCHAR(100), type VARCHAR(100), TR_ID_FK INTEGER NOT NULL, TC_ID_FK INTEGER NOT NULL, FOREIGN KEY (TC_ID_FK) REFERENCES table_column (TC_ID_PK) );'
    conn.execute(sql)

# qcML objects
class CV: 
    def __init__(self, id = None, dictionary = {}, xml = None):
        self.id = id
        self.version = ""
        self.fullName = ""
        self.uri = ""
        self.sqliteId = None
        if dictionary:
            self.fromDict(dictionary)
        if xml:
            self.fromXml(xml)
        return
    
    def fromDict(self, dictionary):
        if 'ID' in dictionary.keys():
            self.id = dictionary['ID']
        if 'version' in dictionary.keys():
            self.version = dictionary['version']
        if 'fullName' in dictionary.keys():
            self.fullName = dictionary['fullName']
        if 'uri' in dictionary.keys():
            self.uri = dictionary['uri']

    def printout(self):
        print "\t\t - CV:"
        print "\t\t\t CV.id = " + self.id
        if self.version:
            print "\t\t\t CV.version = " + self.version
        if self.fullName:
            print "\t\t\t CV.fullName = " + self.fullName
        if self.uri:
            print "\t\t\t CV.uri = " + self.uri

    def fromXml(self, xml):
        if DEBUG:
            print "\t\t " + XML_CV + ":"                 
        self.fromDict(getParamDict(xml.attributes.items(), offset="\t\t\t"))

    def toXml(self,file, offset=""):
        file.write(offset + "<" + XML_CV)
        if self.uri:
            file.write(' uri="' + self.uri + '"')
        file.write(' ID="' + self.id  + '"')
        if self.fullName:
            file.write(' fullName="' + self.fullName + '"')
        if self.version:
            file.write(' version="' + self.version + '"')
        file.write("/>\n")

    def fromSQLite(self, row):
        self.id = row[1]
        self.sqliteId = row[0]
        self.fullName = row[2]
        self.version = row[3]
        self.uri = row[4]
        if DEBUG:
            print " - Got cv: " + str(row)

    def toSQLite(self, conn):
        cursor = conn.cursor()
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

class QcML:
    def __init__(self, qcml_file = ""):
        self.QcMLFile = qcml_file
        self.runQualityAssessmentList = [] # QualityAssessment list
        self.setQualityAssessmentList = [] # QualityAssessment list
        self.cvList = []
        self.sqliteId = None
        return

    def printout(self):
        print 'qcML printout:'
        print '\t QcMLFile = ' + self.QcMLFile
        print "\t - CVList: " 
        for item in self.cvList:
            item.printout()
        for assessment in self.runQualityAssessmentList + self.setQualityAssessmentList:
            assessment.printout()
                
    def fromXml(self, xml):
        # Run and Set Quality Assesments
        quality_assessments = xml.getElementsByTagName(XML_RUN_QUALITY) 
        quality_assessments += xml.getElementsByTagName(XML_SET_QUALITY) 
        if quality_assessments:
            for assessment in quality_assessments :
                qualityAssessment = QualityAssessment(xml = assessment)
                if qualityAssessment.isSet:
                    qcML.setQualityAssessmentList += [qualityAssessment]
                else:
                    qcML.runQualityAssessmentList += [qualityAssessment]
        # cvList
        if xml.getElementsByTagName(XML_CVLIST):
            for cv_list in xml.getElementsByTagName(XML_CVLIST) :
                if DEBUG:
                    print XML_CVLIST + ":"
                cv_elements = cv_list.getElementsByTagName(XML_CV)
                for cv_element in cv_elements:
                    qcML.cvList += [CV(xml = cv_element)]
        return    

    def toXml(self, file):
        file.write(XML_HEADER)
        file.write('<!-- XML file generated by qcml2qcdb.py (espona@imsb.biol.ethz.ch) -->\n')
        
        file.write('<' + XML_QCML + ' xmlns=' + XMLNS + '>\n')

        for assessment in self.runQualityAssessmentList + self.setQualityAssessmentList:
            assessment.toXml(file)
        
        file.write("\t<" + XML_CVLIST + ">"  + "\n")
        for item in self.cvList:
            item.toXml(file, offset="\t\t")
        file.write("\t</" + XML_CVLIST + ">"  + "\n")
        file.write('</' + XML_QCML + '>' + "\n")
        return    
    
    def fromSQLite(self, conn, id):
        cursor = conn.cursor()
        self.sqliteId = id
        cursor.execute("SELECT qcml_file from qcml where QC_ID_PK=:id;", {"id":qcml_pk})
        self.QcMLFile = cursor.fetchone()[0]
        
        # get cv list
        res = cursor.execute("select CV_ID_PK, id, full_name, version, uri from cv_list join cv on (CV_ID_FK=CV_ID_PK) where QC_ID_FK=:id;", {"id":qcml_pk})
        for row in res:
            new_cv = CV("")
            new_cv.fromSQLite(row)
            self.cvList += [new_cv]
        
        # get qualityAssessmentList
        res = cursor.execute("select QA_ID_PK, id, is_set from quality_assessment where QC_ID_FK=:id;", {"id":qcml_pk})
        for row in res:
            new_assessment = QualityAssessment({"ID":row[1]})
            new_assessment.fromSQLite(conn, row)
            if new_assessment.isSet:
                self.setQualityAssessmentList += [new_assessment]
            else:
                self.runQualityAssessmentList += [new_assessment]
        return 
        
    def toSQLite(self, conn):
        cursor = conn.cursor()
        cursor.execute("insert into qcml(qcml_file) values (:file);", {"file":self.QcMLFile})
        cursor.execute('SELECT last_insert_rowid()')
        qcml_pk = cursor.fetchone()[0]
        self.sqliteId = qcml_pk
        if DEBUG:
            print "qcml_pk = " + str(qcml_pk)
        
        for cv in self.cvList:
            cv_pk = cv.toSQLite(conn)
            if DEBUG:
                print "\t - cv_pk = " + str(cv_pk) 
            cursor.execute("insert into cv_list(QC_ID_FK, CV_ID_FK) values (:QC_ID_FK, :CV_ID_FK);", {"QC_ID_FK":qcml_pk, "CV_ID_FK":cv_pk})
            if DEBUG:
                print "\t - cl_pk = (" + str(qcml_pk) + ", " + str(cv_pk) + ")"
            
        for assessment in self.runQualityAssessmentList + self.setQualityAssessmentList:
            assessment_pk = assessment.toSQLite(conn,qcml_pk, self.cvList)
        return qcml_pk

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
                if param.__class__.__name__=="QualityParameter":
                    for threshold in param.thresholdList:
                        if threshold.unitCvRef:
                            if not cvInList(threshold.unitCvRef, cvList):
                                cvList += [CV(threshold.unitCvRef)]
                        if threshold.cvRef:
                            if not cvInList(threshold.cvRef, cvList):
                                cvList += [CV(threshold.cvRef)]
            return cvList           
        for assessment in self.runQualityAssessmentList:
            self.cvList = getCVfromList(assessment.paramList, self.cvList)
        for assessment in self.setQualityAssessmentList:
            self.cvList = getCVfromList(assessment.paramList, self.cvList)
        return self.cvList

class QualityAssessment:
    def __init__(self, dictionary = {}, xml = None):
        self.id = None
        self.isSet = False
        self.paramList = []
        self.sqliteId = None
        if dictionary:
            self.fromDict(dictionary)
        if xml:
            self.fromXml(xml)
        
    def fromDict(self, dictionary):
        self.id = dictionary['ID']
        if 'isSet' in dictionary.keys():
            self.isSet = bool(dictionary['isSet'])

    def printout(self):
        if not self.isSet:
            print '\t - RunQualityAssessment:'   
        else:
            print '\t - SetQualityAssessment:'
        print '\t\t id = ' + str(self.id)
        print '\t\t isSet = ' + str(self.isSet)
        print '\t\t - paramList: '
        for param in self.paramList:
            param.printout()  

    def fromXml(self, xml):
        self.isSet = (xml.tagName == XML_SET_QUALITY)
        if DEBUG:
            print xml.tagName + ':'
        self.fromDict(getParamDict(xml.attributes.items(), offset="\t\t"))
        
        for quality_parameter in xml.getElementsByTagName(XML_QUALITY_PARAMETER):
            self.paramList += [QualityParameter(xml = quality_parameter)]
        
        for attachment_item in xml.getElementsByTagName(XML_ATTACHMENT):
            self.paramList += [AttachmentParam(xml = attachment_item)]
            
    def toXml(self, file):
            if not self.isSet:
                file.write('\t<' + XML_RUN_QUALITY + ' ID="' + self.id + '">\n')  
            else:
                file.write('\t<' + XML_SET_QUALITY + ' ID="' + self.id + '">\n')
            for param in (self.paramList):
                param.toXml(file)
            if not self.isSet:
                file.write('\t</' + XML_RUN_QUALITY + '>\n')  
            else:
                file.write('\t</' + XML_SET_QUALITY + '>\n')
    
    def fromSQLite(self, conn, row):
        cursor = conn.cursor()
        self.sqliteId = row[0]
        self.id = row[1]
        self.isSet = bool(row[2])
        
        if DEBUG:
            print " - Got quality_assessment: " + str(row)

        # quality parameters
        res = cursor.execute("select QP_ID_PK, quality_parameter.id as id, name, value, unit_name, unit_accession, cv2.id as unit_cv_ref, accession, cv1.id as cv_ref, flag\
                             from quality_parameter join cv as cv1 on (cv_ref=cv1.CV_ID_PK) left join cv as cv2 on (unit_cv_ref=cv2.CV_ID_PK) where QA_ID_FK=:id;", {"id":self.sqliteId})
        
        for row in res:
            new_quality_parameter = QualityParameter({})
            new_quality_parameter.fromSQLite(row, conn)
            self.paramList += [new_quality_parameter]

        res = cursor.execute("select AP_ID_PK, attachment_parameter.id as id, name, value, unit_name, unit_accession, cv2.id as unit_cv_ref, accession, cv1.id as cv_ref, binary, quality_parameter_ref \
                             from attachment_parameter join cv as cv1 on (cv_ref=cv1.CV_ID_PK) left join cv as cv2 on (unit_cv_ref=cv2.CV_ID_PK) where QA_ID_FK=:id;", {"id":self.sqliteId})
        for row in res:
            new_attachment_parameter = AttachmentParam({})
            new_attachment_parameter.fromSQLite(row, conn)
            self.paramList += [new_attachment_parameter]

    def toSQLite(self, conn, qcml_pk, cv_list):
        cursor = conn.cursor()
        cursor.execute("insert into quality_assessment(id, is_set, QC_ID_FK) values (:id, :is_set, :QC_ID_FK);", 
                       {"id":self.id, "is_set":int(self.isSet), "QC_ID_FK":qcml_pk})
        cursor.execute('SELECT last_insert_rowid()')
        self.sqliteId = cursor.fetchone()[0]
        if DEBUG:
            print "\t - assessment_pk = " + str(self.sqliteId)  + "\t " + str(self.id) 
        for param in self.paramList:
            param.toSQLite(conn, self.sqliteId, cv_list)      
        return self.sqliteId
    
class AbstractParam:
    def __init__(self, dictionary):
        self.id = ""
        self.name = ""
        self.value = ""
        self.unitName = ""
        self.unitAccession = ""
        self.sqliteId = None
        self.unitName = ""
        self.unitAccession = ""
        self.unitCvRef = ""
        self.fromDict(dictionary)
    
    def fromDict(self, dictionary):
        if 'ID' in dictionary.keys():
            self.id = dictionary['ID']
        if 'name' in dictionary.keys():
            self.name = dictionary['name']
        if 'value' in dictionary.keys():
            self.value = dictionary['value']
        if 'unitName' in dictionary.keys():
            self.unitName = dictionary['unitName']
        if 'unitAccession' in dictionary.keys():
            self.unitAccession = dictionary['unitAccession']
        if 'unitCvRef' in dictionary.keys():
            self.unitCvRef = dictionary['unitCvRef']
          
    def printout(self, offset = "\t\t\t"):
        print offset + ' - ' + self.__class__.__name__ + ':'
        if self.id:
            print offset + '\t id = ' + self.id            
        print offset + '\t name = ' + self.name
        if self.value:
            print offset + '\t value = ' + self.value
        if self.unitName:
            print offset + '\t unitName = ' + self.unitName
        if self.unitAccession:
            print offset + '\t unitAccession = ' + self.unitAccession
        if self.unitCvRef:
            print offset + '\t unitCvRef = ' + self.unitCvRef
            
    def fromSQLite(self, row):
        #QP_ID_PK, name, id, value, unit_name, unit_accession, unit_cv_ref
        self.sqliteId = row[0]
        self.id = row[1]
        self.name = row[2]
        self.value = row[3]
        self.unitName = row[4]
        self.unitAccession = row[5]
        self.unitCvRef = row[6]  

class CVParam(AbstractParam):
    def __init__(self, dictionary):
        AbstractParam.__init__(self, dictionary)
        self.accession = ""
        self.cvRef = ""
        self.fromDict(dictionary)
        
    def fromDict(self, dictionary):
        AbstractParam.fromDict(self, dictionary)
        if 'accession' in dictionary.keys():
            self.accession = dictionary['accession']
        if 'cvRef' in dictionary.keys():
            self.cvRef = dictionary['cvRef']
        
    def printout(self, offset = "\t\t\t"):
        AbstractParam.printout(self, offset)
        print offset +'\t accession = ' + self.accession
        if self.cvRef:
            print offset +'\t cvRef = ' + str(self.cvRef)

    def toXml(self, file):
        if self.id:
            file.write(' ID="' + self.id  + '"')           
        file.write(' name="' + self.name + '"')
        if self.value:
            file.write(' value="' + self.value + '"')
        if self.cvRef:
            file.write(' cvRef="' + str(self.cvRef) + '"')
        file.write(' accession="' + self.accession + '"') 
        if self.unitAccession:
            file.write(' unitAccession="' + self.unitAccession + '"')
        if self.unitCvRef:
            file.write(' unitCvRef="' + self.unitCvRef + '"')
        if self.unitName:
            file.write(' unitName="' + self.unitName + '"')
        return
    
    def fromSQLite(self, row):
        AbstractParam.fromSQLite(self, row)
        self.accession = row[7]
        self.cvRef = row[8]

class QualityParameter(CVParam):
    def __init__(self, dictionary = {}, thresholdList = [], xml =  None):
        CVParam.__init__(self, dictionary)
        self.flag = None # Boolean
        self.thresholdList = thresholdList 
        if dictionary:
            self.fromDict(dictionary)
        if xml:
            self.fromXml(xml)
        
    def fromDict(self, dictionary):
        CVParam.fromDict(self, dictionary)
        if 'flag' in dictionary.keys():
            self.flag = bool(dictionary['flag'])
         
    def printout(self):
        CVParam.printout(self)
        if self.flag:
            print '\t\t\t\t flag = ' + str(self.flag)
        for threshold in self.thresholdList:
                threshold.printout()

    def fromXml(self, xml):
        resultlist = []
        if DEBUG:
            print '\t ' + XML_QUALITY_PARAMETER + ':'
        self.fromDict(getParamDict(xml.attributes.items()))     
        self.thresholdList = []
        for threshold_item in xml.getElementsByTagName(XML_THRESHOLD):
            self.thresholdList += [Threshold(xml = threshold_item)]
    
    def toXml(self, file):
        file.write('\t\t<' + XML_QUALITY_PARAMETER)
        CVParam.toXml(self, file)
        if self.flag:
            file.write(' flag="' + str(self.flag).lower() + '"')
        if self.thresholdList:
            file.write('>\n' )
            for threshold in self.thresholdList:
                threshold.toXml(file)
            file.write('\t\t</' + XML_QUALITY_PARAMETER + ">\n")
        else:     
            file.write('/>' + "\n")
    
    def fromSQLite(self, row, conn):
        CVParam.fromSQLite(self, row)
        self.flag = bool(row[9]) 
        self.thresholdList = []
        cursor = conn.cursor()
        res = cursor.execute("select TH_ID_PK, NULL as id, name, value, unit_name, unit_accession, cv2.id as unit_cv_ref, accession, cv1.id as cv_ref, threshold_filename\
                             from threshold join cv as cv1 on (cv_ref=cv1.CV_ID_PK) left join cv as cv2 on (unit_cv_ref=cv2.CV_ID_PK) where QP_ID_FK=:id;", {"id":self.sqliteId})
        if DEBUG:
            print " - Got quality_parameter: " + str(row)
        
        for th_row in res:
            threshold = Threshold({})
            threshold.fromSQLite(th_row)
            self.thresholdList += [threshold]
    
    def toSQLite(self, conn, assessment_pk, cv_list):
        cursor = conn.cursor()
        cv_ref_sqlite_id = None
        unit_cv_ref_sqlite_id = None
        for cv in cv_list:
            if self.cvRef:
                if cv.id == self.cvRef:
                    cv_ref_sqlite_id = cv.sqliteId
            if self.unitCvRef:
                if cv.id == self.unitCvRef:
                    unit_cv_ref_sqlite_id = cv.sqliteId

        if not self.id:
            while not self.id:
                random_id = "ID_" + str(random.random())[2:]
                cursor.execute('SELECT * from quality_parameter where id=:id', {"id":random_id})
                if not cursor.fetchone():
                    self.id = random_id

        cursor.execute("insert into quality_parameter (id, name, value, accession, unit_name, unit_accession, flag, cv_ref, unit_cv_ref, QA_ID_FK)  \
                        values (:id, :name, :value, :accession, :unit_name, :unit_accession, :flag, :cv_ref, :unit_cv_ref, :QA_ID_FK);", 
                        {"id":self.id, "name": self.name,"value": self.value,"accession": self.accession,
                         "unit_name": self.unitName,"unit_accession": self.unitAccession, "flag":self.flag,
                         "cv_ref":cv_ref_sqlite_id,"unit_cv_ref":unit_cv_ref_sqlite_id,"QA_ID_FK":assessment_pk})
        cursor.execute('SELECT last_insert_rowid()')
        self.sqliteId = cursor.fetchone()[0]
        if DEBUG:
            print "\t - qp_pk = " + str(self.sqliteId) + "\t " + str(self.id) 
        
        for threshold in self.thresholdList:
            threshold.toSQLite(conn, self.sqliteId, cv_list)
        return self.sqliteId

class Threshold(CVParam):
    def __init__(self, dictionary = {}, xml = None):
        CVParam.__init__(self, dictionary)
        self.thresholdFilename = ""
        if dictionary:
            self.fromDict(dictionary)
        if xml:
            self.fromXml(xml)

    def fromDict(self, dictionary):
        CVParam.fromDict(self, dictionary)
        if 'threshold_filename' in dictionary.keys():
            self.thresholdFilename = dictionary['threshold_filename']   
        
    def printout(self):
        CVParam.printout(self, "\t\t\t\t")
        if self.thresholdFilename:
            print '\t\t\t\t\t thresholdFilename = ' + self.thresholdFilename
    
    def toSQLite(self, conn, quality_parameter_pk, cv_list):
        cursor = conn.cursor()
        cv_ref_sqlite_id = None
        unit_cv_ref_sqlite_id = None
        for cv in cv_list:
            if self.cvRef:
                if cv.id == self.cvRef:
                    cv_ref_sqlite_id = cv.sqliteId
            if self.unitCvRef:
                if cv.id == self.unitCvRef:
                    unit_cv_ref_sqlite_id = cv.sqliteId

        cursor.execute("insert into threshold (name, value, accession, unit_name, unit_accession, threshold_filename, cv_ref, unit_cv_ref, QP_ID_FK)  \
                        values (:name, :value, :accession, :unit_name, :unit_accession, :threshold_filename, :cv_ref, :unit_cv_ref, :QP_ID_FK);", 
                        {"name": self.name,"value": self.value,"accession": self.accession,
                         "unit_name": self.unitName,"unit_accession": self.unitAccession, "threshold_filename":self.thresholdFilename,
                         "cv_ref":cv_ref_sqlite_id,"unit_cv_ref":unit_cv_ref_sqlite_id,"QP_ID_FK":quality_parameter_pk})
        cursor.execute('SELECT last_insert_rowid()')
        self.sqliteId = cursor.fetchone()[0]
        if DEBUG:
            print "\t\t - th_pk = " + str(self.sqliteId) + "\t " + str(self.name) + "\t " + str(self.thresholdFilename)  
        return self.sqliteId
    
    def fromSQLite(self, row):
        CVParam.fromSQLite(self, row)
        self.thresholdFilename = row[9]
        if DEBUG:
            print " - Got threshold: " + str(row)

    def toXml(self, file):
        file.write('\t\t\t<' + XML_THRESHOLD)
        if self.thresholdFilename:
            file.write(' threshold_filename="' + self.thresholdFilename + '"')
        CVParam.toXml(self, file)
        file.write('/>' + "\n")     

    def fromXml(self, xml):    
        if DEBUG:
            print '\t\t\t Threshold: '
        self.fromDict(getParamDict(xml.attributes.items(), offset="\t\t\t\t"))
 
class AttachmentParam(CVParam):
    def __init__(self, dictionary = {}, binary = "", table = [], xml = None):
        CVParam.__init__(self, dictionary)
        self.binary_txt = binary
        self.tableList = table
        self.qualityParameterRef = ""
        if dictionary:
            self.fromDict(dictionary)
        if xml:
            self.fromXml(xml)
        self.binary = self.readBinary(self.binary_txt)
        
    def fromDict(self, dictionary):
        CVParam.fromDict(self, dictionary)
        if 'qualityParameterRef' in dictionary.keys():
            self.qualityParameterRef = dictionary['qualityParameterRef']
        
    def readBinary(self, text):
        if len(text)>1:
            binary = text.encode("base64")
        else:
            binary = None   
        return binary
    
    def printout(self):
        CVParam.printout(self)
        if self.binary:
            print '\t\t\t\t binary = "' + self.binary_txt[0:20] + '..."'
        for table in self.tableList:
            print '\t\t\t\t table = ' 
            table.printout(offset = "\t\t\t\t\t") 
        if self.qualityParameterRef:
            print '\t\t\t\t qualityParameterRef = ' + self.qualityParameterRef            

    def fromXml(self, xml):
        def getBinary(binary_list):
            binary = ""
            if binary_list:
                binary = binary_list[0].firstChild.nodeValue
                if DEBUG:
                    print '\t\t\t binary: "' + binary_list[0].firstChild.nodeValue[0:20] + '..."'
            return binary
        if DEBUG:
            print '\t Attachment:'         
        self.fromDict(getParamDict(xml.attributes.items()))
        self.binary_txt = getBinary(xml.getElementsByTagName(XML_BINARY))
        self.tableList= []
        for xml_table in xml.getElementsByTagName(XML_TABLE):
            self.tableList +=  [TableAttachment(xml=xml_table)]            
    
    def toXml(self, file):
        file.write('\t\t<' + XML_ATTACHMENT )
        CVParam.toXml(self, file)
        if self.qualityParameterRef:
            file.write(' qualityParameterRef="' + self.qualityParameterRef + '"') 
        file.write('>' + "\n")     
        if self.binary:
            file.write('\t\t\t<' + XML_BINARY + '>' + self.binary_txt + '</' + XML_BINARY + '>' + "\n")
        for table in self.tableList:
            file.write(table.toXml('\t\t\t'))
        file.write('\t\t</' + XML_ATTACHMENT + '>' + "\n")

    def fromSQLite(self, row, conn):
        CVParam.fromSQLite(self, row)
        self.binary_txt = row[9]
        self.binary = self.readBinary(self.binary_txt)
        self.qualityParameterRef = row[10]
        if DEBUG:
            print " - Got attachment_parameter: " + str(row)
        
        cursor = conn.cursor()       
        res = cursor.execute('SELECT TA_ID_PK from table_attachment where AP_ID_FK=:sqliteId', {"sqliteId":int(self.sqliteId)})
        self.tableList = []
        for row in res:
            table_sqliteId = row[0]
            table = TableAttachment()
            table.fromSQLite(table_sqliteId, conn)
            self.tableList += [table]
            
    def toSQLite(self, conn, assessment_pk, cv_list):
        cursor = conn.cursor()
        cv_ref_sqlite_id = None
        unit_cv_ref_sqlite_id = None
        for cv in cv_list:
            if self.cvRef:
                if cv.id == self.cvRef:
                    cv_ref_sqlite_id = cv.sqliteId
            if self.unitCvRef:
                if cv.id == self.unitCvRef:
                    unit_cv_ref_sqlite_id = cv.sqliteId
        if not self.id:
            while not self.id:
                random_id = "ID_" + str(random.random())[2:]
                cursor.execute('SELECT * from attachment_parameter where id=:id', {"id":random_id})
                if not cursor.fetchone():
                    self.id = random_id

        cursor.execute("insert into attachment_parameter (id, name, value, accession, unit_name, unit_accession, cv_ref, unit_cv_ref, QA_ID_FK, binary, quality_parameter_ref)  \
                        values (:id, :name, :value, :accession, :unit_name, :unit_accession, :cv_ref, :unit_cv_ref, :QA_ID_FK, :binary, :quality_parameter_ref);", 
                        {"id":self.id, "name": self.name,"value": self.value,"accession": self.accession, "unit_name": self.unitName,"unit_accession": self.unitAccession,
                         "cv_ref":cv_ref_sqlite_id,"unit_cv_ref":unit_cv_ref_sqlite_id ,"QA_ID_FK":assessment_pk, "binary":self.binary_txt, "quality_parameter_ref":self.qualityParameterRef})
        cursor.execute('SELECT last_insert_rowid()')
        
        self.sqliteId = cursor.fetchone()[0]
        if DEBUG:
            print "\t - ap_pk = " + str(self.sqliteId) + "\t " + str(self.id) 

        for table in self.tableList:
            table.toSQLite(conn, self.sqliteId)
        return self.sqliteId
   
class TableAttachment:
    def __init__(self, columns = [], rowList = [], xml = None):
        self.columns = columns
        self.rowList = rowList
        if xml:
            self.fromXml(xml)
     
    def printout(self, offset = ''):
        table_str = "TABLE_STR_EMPTY"
        if self.columns:
            header = TABLE_SEPARATOR.join(self.columns)
            table_str = offset + header + "\n"
            table_str += offset + ('-'*len(header)) + "\n"
        for row in self.rowList:
            row_str = ""
            for value in row.values:
                row_str += str(value) + TABLE_SEPARATOR
            table_str += offset + row_str[:-1] + "\n"
        print table_str

    def fromXml(self, xml):
        header_list = xml.getElementsByTagName(XML_TABLE_COLUMN)
        if header_list:
            self.columns = header_list[0].firstChild.nodeValue.split(TABLE_SEPARATOR)
            if DEBUG:
                print '\t\t\t header:  ' + str(", ".join(self.columns))[0:50] +'...'
            row_list = xml.getElementsByTagName(XML_TABLE_ROW)
            self.rowList = []
            for row in row_list:
                if DEBUG & (row == row_list[0]):
                    print '\t\t\t rows: ' + str(", ".join(row.firstChild.nodeValue.split(TABLE_SEPARATOR)))[0:50] + '...'
                self.rowList += [Row(row.firstChild.nodeValue.split(TABLE_SEPARATOR))]
        else:
            self = None

    def toXml(self, offset=""):
        table_str = offset + "<" + XML_TABLE + ">\n"
        if self.columns:
            header = TABLE_SEPARATOR.join(self.columns)
            table_str +=  offset + "\t<" + XML_TABLE_COLUMN + ">" + header + "</" + XML_TABLE_COLUMN + ">\n"
        for row in self.rowList:
            row_str = ""
            for value in row.values:
                row_str += str(value) + TABLE_SEPARATOR
            table_str += offset + "\t<" + XML_TABLE_ROW + ">" + row_str[:-1] + "</" + XML_TABLE_ROW + ">\n"
        table_str += offset + "</" + XML_TABLE + ">\n"
        return table_str
        
    def fromSQLite(self, sqliteId, conn):
        self.sqliteId = sqliteId
        if DEBUG:
            print " - Got table_attachment: " + str(sqliteId)
        cursor = conn.cursor()       
        # get columns
        res = cursor.execute('SELECT TC_ID_PK, name, TA_ID_FK from table_column where TA_ID_FK=:sqliteId', 
                       {"sqliteId":self.sqliteId})
        self.columns = []
        column_sqliteId_list = []
        for row in res:
            self.columns += [row[1]]
            column_sqliteId_list += [row[0]]
        
        # get rows
        res = cursor.execute('SELECT TR_ID_PK, row_num, TA_ID_FK from table_row where TA_ID_FK=:sqliteId order by row_num', 
                       {"sqliteId":self.sqliteId})
        row_sqliteId_list = [] 
        for row in res:
            row_sqliteId_list += [row[0]]
        
        # get values
        self.rowList = []
        for row_sqliteId in row_sqliteId_list:
            values = []
            for column_sqliteId in column_sqliteId_list:
                res = cursor.execute('SELECT value from table_value where TR_ID_FK=:row_sqliteId and TC_ID_FK=:column_sqliteId', 
                       {"row_sqliteId":row_sqliteId, "column_sqliteId":column_sqliteId})
                for value_row in res:
                    values += [value_row[0]]
            self.rowList += [Row(values, row_sqliteId)]

    def toSQLite(self, conn, attachment_pk):
        cursor = conn.cursor()
        cursor.execute("insert into table_attachment (AP_ID_FK) values (:AP_ID_FK);", 
                       {"AP_ID_FK":attachment_pk})
        cursor.execute('SELECT last_insert_rowid()') 
        self.sqliteId = cursor.fetchone()[0]
        if DEBUG:
            print "\t\t - ta_pk = " + str(self.sqliteId) + "\t " + str(attachment_pk) 

        column_sqliteId_list = []
        for column in self.columns:
            cursor.execute("insert into table_column (name, TA_ID_FK) values (:name, :TA_ID_FK);", 
                       {"name": column,"TA_ID_FK":self.sqliteId})
            cursor.execute('SELECT last_insert_rowid()') 
            column_sqliteId = cursor.fetchone()[0]
            column_sqliteId_list += [column_sqliteId]
            if DEBUG:
                print "\t\t\t - tc_pk = " + str(column_sqliteId) + "\t " + str(column) + "\t " + str(self.sqliteId) 
        row_num = 0
        for row in self.rowList:
            cursor.execute("insert into table_row (row_num, TA_ID_FK) values (:row_num, :TA_ID_FK);", 
                       {"row_num": row_num,"TA_ID_FK":self.sqliteId})
            cursor.execute('SELECT last_insert_rowid()') 
            row_sqliteId = cursor.fetchone()[0]
            if DEBUG:
                print "\t\t\t - tr_pk = " + str(row_sqliteId) + "\t " + str(row_num) + "\t " + str(self.sqliteId) 
            value_index = 0   
            type = "string" 
            for value in row.values:
                try:
                    type = "integer"
                    aux = int(value)
                except ValueError:         
                    try:
                        type = "double"
                        aux = float(value)
                    except ValueError:         
                        type = "string"
                
                cursor.execute("insert into table_value (value, type, TR_ID_FK, TC_ID_FK) values (:value, :type, :TR_ID_FK, :TC_ID_FK);", 
                           {"value":value, "type":type, "TR_ID_FK":row_sqliteId, "TC_ID_FK":column_sqliteId_list[value_index]})
                cursor.execute('SELECT last_insert_rowid()') 
                value_sqliteId = cursor.fetchone()[0]
                if DEBUG:
                    print "\t\t\t\t - tv_pk = " + str(value_sqliteId) + "\t " + str(value) + "\t " + str(type) + "\t " + str(row_sqliteId) + "\t " + str(column_sqliteId_list[value_index])                     
                    value_index += 1 
            row_num += 1
        
        return self.sqliteId

class Row:
    def __init__(self, values = [], sqliteId = None):
        self.values = values
        self.sqliteId = sqliteId

#####################################################
# Conversion script starts  
if len(sys.argv)<2:
    print "ERROR: No input file (.db, .qcML) provided"
    sys.exit()
     
input_file = sys.argv[1]

if os.path.splitext(input_file)[1] == ".db":
    mode = "qcdb2qcml"
    print "\n Converting from qcDB to qcML:"
else:
    mode = "qcml2qcdb"
    print "\n Converting from qcML to qcDB:"

if mode == "qcml2qcdb":
    # 1. Parse the qcML file
    qcml_file = input_file
    xmldoc = minidom.parse(qcml_file)
    qcML = QcML(qcml_file)
    
    # 2. Build QcML object 
    print " - Parsing qcML file ..."
    # Assumes only one QcML element per file
    qcML.fromXml(xmldoc.getElementsByTagName(XML_QCML)[0])
    # fix for duplicated/missing CV elements
    qcML.getUniqueCVList()
    
    # Print QcML object
    print " - Generating the intermediate QcML object ..."
    if DEBUG:
        qcML.printout()
    
    # 3. Export it to SQLite
    print " - Generating the SQLite database..."
    if len(sys.argv) < 3:
        db_name = os.path.splitext(qcml_file)[0] + ".db"
    else:
        db_name = sys.argv[2]
    if DEBUG:
        print 'SQLite database: ' + db_name
    
    # Connect to the database 
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    createSQLiteTables(c)

    # Insert data in the database
    qcml_pk = qcML.toSQLite(conn)
    
    # Save (commit) the changes and close the connection
    conn.commit()
    conn.close()
    
    print ' Finished! To access the generated qcDB file execute: sqlite3 ' + db_name + '\n'

else:
    db_name = input_file
    print " - Generating qcML object(s) from database:"
    conn = sqlite3.connect(db_name)    
    cursor = conn.cursor()
    res = cursor.execute ("SELECT QC_ID_PK from qcml;")
    for row in res:
        qcml_pk = row[0]
        print "\t * Getting qcml object from database, id = " + str(qcml_pk)
        qcML = QcML("")
        qcML.fromSQLite(conn, qcml_pk)
        if DEBUG:
            qcML.printout()
        print "\t\t - Writing qcML file..."
        if len(sys.argv) < 3:
            new_qcml_file =  os.path.splitext(db_name)[0] + "_qcdb_" + str(qcml_pk) + ".qcml"
        else:
            new_qcml_file = os.path.splitext(db_name)[0] + "_" + str(qcml_pk) + ".qcml"   
        if DEBUG:
            print 'SQLite database: ' + db_name
        with open(new_qcml_file, 'w') as sink:
            qcML.toXml(sink)
        print '\t\t - Generated qcML file is: ' + new_qcml_file
    # Close the connection
    conn.close()
    print ' Finished! Written ' + str(qcml_pk) + ' qcML file(s)\n'
