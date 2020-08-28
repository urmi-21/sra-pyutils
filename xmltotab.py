# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 22:17:21 2020

@author: mrbai
"""
import sys
import os
import xml.etree.ElementTree as ET 
import csv 
import subprocess


def replaceNone(lst):
    return ['NA' if v is None else v for v in lst]


def parse_experiment(expnode):
    fields=['Experiment_accession','Title','Study_accession','Design_description',
            'Library_name','Library_strategy','Library_source','Library_selection','Library_layout','Platform']
    d = {}
    for f in fields:
        d[f]='NA'
    
    for child in expnode.iter():
        #print(child.tag,child.text,child.attrib)
        childtag=child.tag
        childval=child.text
        
        if not childval:
            childval='NA'
        if not childtag:
            childtag='NA'
            
        childattrib=child.attrib
        if childtag == 'EXPERIMENT':
            d['Experiment_accession']=childattrib['accession']
            
        elif childtag == 'TITLE':
            d['Title']=childval
            
        elif childtag == 'STUDY_REF':
            d['Study_accession']=childattrib['accession']
            
            
        elif childtag == 'DESIGN_DESCRIPTION':
            d['Design_description']=childval
            
            
        #elif childtag == 'SAMPLE_DESCRIPTOR':
        #    d['Sample_accession']=childattrib['accession']
        
            
        elif childtag == 'LIBRARY_NAME':
            d['Library_name']=childval
            
            
        elif childtag == 'LIBRARY_STRATEGY':
            d['Library_strategy']=childval
            
            
        elif childtag == 'LIBRARY_SOURCE':
            d['Library_source']=childval
            
            
        elif childtag == 'LIBRARY_SELECTION':
            d['Library_selection']=childval
            
            
        elif childtag == 'LIBRARY_LAYOUT':
            layout=list(child)[0].tag
            d['Library_layout']=layout
            
            
        elif childtag == 'PLATFORM':
            for c in child.iter():
                if c.tag == 'INSTRUMENT_MODEL':
                    d['Platform']=c.text
                    
                    
    #print ('\t'.join(result))
    #print(result)
    #result=replaceNone(result)
    #return ('\t'.join(result))
    #return d
    return '\t'.join([d[f] for f in fields])

def parse_study(node):
    d = {}
    fields=['Study_acession','Study_alias','Center_name','External_id','Study_title','Study_type',
            'Study_abstract','Study_description']
    for f in fields:
        d[f]='NA'
        
    #get study attribs
    study_attrib=node.attrib
    d['Study_acession']=study_attrib['accession']
    d['Study_alias']=study_attrib['alias']
    d['Center_name']=study_attrib['center_name']
        
    for child in node.iter():
        #print(child.tag,child.text,child.attrib)
        childtag=child.tag
        childval=child.text
        if not childval:
            childval='NA'
        if not childtag:
            childtag='NA'
            
        childattrib=child.attrib
        
        
        if childtag == 'EXTERNAL_ID':
            d['External_id']=childattrib['namespace']+':'+childval
    
        elif childtag == 'STUDY_TITLE':
            d['Study_title']=childval
            
        elif childtag == 'STUDY_TYPE':
            d['Study_type']=childattrib['existing_study_type']
            
        elif childtag == 'STUDY_ABSTRACT':
            d['Study_abstract']=childval
            
        elif childtag == 'STUDY_DESCRIPTION':
            d['Study_description']=childval
            
        
    return '\t'.join([d[f] for f in fields])
        

def parse_runset(run_set):
    result=[]
    #find runs in run set
    for r in run_set:
        result.append(parse_run(r))
    return result
    
def parse_run(run):
    
    d = {}
    fields=['Run_accession','Run_alias','Total_spots','Total_bases','Size','Publised_date',
            'Sample_accession','Sample_name','Tax_id','Organism']
    for f in fields:
        d[f]='NA'
    
    for child in run.iter():
        childtag=child.tag
        childval=child.text
        if not childval:
            childval='NA'
        if not childtag:
            childtag='NA'
            
        childattrib=child.attrib
        for a in childattrib:
            if not childattrib[a]:
                childattrib[a]='NA'
                
        if childtag == 'RUN':
            d['Run_accession']=childattrib['accession']
            d['Run_alias']=childattrib['alias']
            d['Total_spots']=childattrib['total_spots']
            d['Total_bases']=childattrib['total_bases']
            d['Size']=childattrib['size']
            d['Publised_date']=childattrib['published']
            
        elif childtag == 'Member':
            d['Sample_accession']=childattrib['accession']
            d['Sample_name']=childattrib['sample_name']
            d['Tax_id']=childattrib['tax_id']
            d['Organism']=childattrib['organism']
            
    
    #print ('\t'.join(result))
    #return ('\t'.join(result))
    #return d
    #return result as string
    return '\t'.join([d[f] for f in fields])
        
            
            


    

headers=[]
headers.append('Experiment')
headers.append('Experiment title')
headers.append('Study accession')
headers.append('Design description')
headers.append('Library name')
headers.append('Library strategy')
headers.append('Library source')
headers.append('Library selection')
headers.append('Library layout')
headers.append('Platform')
headers.append('SRA accession')
headers=headers+['Study_acession','Study_alias','Center_name','External_id','Study_title','Study_type',
            'Study_abstract','Study_description']
headers.append('SRR accession')
headers.append('SRR alias')
headers.append('Total spots')
headers.append('Total bases')
headers.append('Size')
headers.append('Date publised')
headers.append('Sample accession')
headers.append('Sample name')
headers.append('Tax id')
headers.append('Organism')

i=0

def processXML(xmlstring):
    towrite=[]
    root=ET.fromstring(xmlstring)
    for exp_pck in root:
        #find Exp node
        thisexp=exp_pck.find("EXPERIMENT") 
        #print('TE:',thisexp,thisexp.attrib)
        exprow=parse_experiment(thisexp)
        
        #find submission node 
        thissubmission=exp_pck.find("SUBMISSION")
        subattrib=thissubmission.attrib
        sraid=subattrib['accession']
        
        #find study node 
        studynode=exp_pck.find("STUDY")
        studyrow=parse_study(studynode)
        
        
        
        #find runs
        runset=exp_pck.find("RUN_SET")
        runsrow=parse_runset(runset)
        
        #print this row
        
        for r in runsrow:
            #print ('\t'.join([exprow,sraid,r]))
            towrite.append('\t'.join([exprow,sraid,studyrow,r]))

    return '\n'.join(towrite)
    #f=open('tsvout.tsv','w')
    #
    #f.write('\n'.join(towrite))
    #f.close()


def listchunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


#read input file
with open(sys.argv[1]) as f:
    srrIds=f.read().splitlines()

#open outfile
outfile=open(sys.argv[2],'w')
outfile.write('\t'.join(headers)+'\n')

#process in batch of 10
chunks=listchunks(srrIds, 15)
tmpfile='__tmp'
ind=1
for l in chunks:
    print(ind)
    ind+=1
    f=open(tmpfile,'w')
    f.write('\n'.join(l)+'\n')
    f.close()
    #get xml
    cmd='epost -db sra -format acc -input '+ tmpfile+' | efetch -format native'
    #print(cmd)
    result = subprocess.Popen(cmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = result.communicate()
    out=out.decode("utf-8")
    exitCode=result.returncode
    if exitCode!=0:
        print('ERORRRRRRRR')
        continue
    xmlstr=str(out.encode('utf-8').strip())
    #print(xmlstr)
    #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXx')
    #parse this xml string
    thisres=processXML(xmlstr)
    thisres=str(thisres.encode('utf-8').strip())
    #write to file
    outfile.write(thisres+'\n')
    
outfile.close()
print('Done')
    

#process in chunks





      
      
