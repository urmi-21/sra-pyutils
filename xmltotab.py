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
    #fields=['EXPERIMENT','TITLE','STUDY_REF','DESIGN_DESCRIPTION','SAMPLE_DESCRIPTOR',
            #'LIBRARY_NAME','LIBRARY_STRATEGY','LIBRARY_SOURCE','LIBRARY_SELECTION','LIBRARY_LAYOUT','PLATFORM']
    result=[]
    for child in expnode.iter():
        print(child.tag,child.text,child.attrib)
        childtag=child.tag
        childval=child.text
        
        if not childval:
            childval='NA'
        if not childtag:
            childtag='NA'
            
        childattrib=child.attrib
        if childtag == 'EXPERIMENT':
            result.append(childattrib['accession'])
        elif childtag == 'TITLE':
            result.append(childval)
        elif childtag == 'STUDY_REF':
            result.append(childattrib['accession'])
            
        elif childtag == 'DESIGN_DESCRIPTION':
            result.append(childval)
            
        elif childtag == 'SAMPLE_DESCRIPTOR':
            result.append(childattrib['accession'])
            
        elif childtag == 'LIBRARY_NAME':
            result.append(childval)
            
        elif childtag == 'LIBRARY_STRATEGY':
            result.append(childval)
            
        elif childtag == 'LIBRARY_SOURCE':
            result.append(childval)
            
        elif childtag == 'LIBRARY_SELECTION':
            result.append(childval)
            
        elif childtag == 'LIBRARY_LAYOUT':
            layout=list(child)[0].tag
            result.append(layout)
            
        elif childtag == 'PLATFORM':
            for c in child.iter():
                if c.tag == 'INSTRUMENT_MODEL':
                    result.append(c.text)
                    
    #print ('\t'.join(result))
    print(result)
    result=replaceNone(result)
    return ('\t'.join(result))

def parse_runset(run_set):
    result=[]
    #find runs in run set
    for r in run_set:
        result.append(parse_run(r))
    return result
    
def parse_run(run):
    result=[]
    #fields=['RUN']
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
            result.append(childattrib['accession'])
            result.append(childattrib['alias'])
            result.append(childattrib['total_spots'])
            result.append(childattrib['total_bases'])
            result.append(childattrib['size'])
            result.append(childattrib['published'])
        elif childtag == 'Member':
            result.append(childattrib['accession'])
            result.append(childattrib['sample_name'])
            result.append(childattrib['tax_id'])
            result.append(childattrib['organism'])
    
    #print ('\t'.join(result))
    return ('\t'.join(result))
            
            


    

headers=[]
headers.append('Experiment')
headers.append('Experiment title')
headers.append('Study accession')
headers.append('Design description')
headers.append('Sample accession')
headers.append('Library name')
headers.append('Library strategy')
headers.append('Library source')
headers.append('Library selection')
headers.append('Library layout')
headers.append('Platform')
headers.append('SRA accession')
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
        print('TE:',thisexp,thisexp.attrib)
        exprow=parse_experiment(thisexp)
        
        #find submission node 
        thissubmission=exp_pck.find("SUBMISSION")
        subattrib=thissubmission.attrib
        sraid=subattrib['accession']
        
        
        #find runs
        runset=exp_pck.find("RUN_SET")
        runsrow=parse_runset(runset)
        
        #print this row
        
        for r in runsrow:
            print ('\t'.join([exprow,sraid,r]))
            towrite.append('\t'.join([exprow,sraid,r]))

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
chunks=listchunks(srrIds, 10)
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
    print(xmlstr)
    print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXx')
    #parse this xml string
    thisres=processXML(xmlstr)
    thisres=str(thisres.encode('utf-8').strip())
    #write to file
    outfile.write(thisres+'\n')
    
outfile.close()
print('Done')
    

#process in chunks





      
      
