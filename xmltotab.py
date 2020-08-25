# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 22:17:21 2020

@author: mrbai
"""

import xml.etree.ElementTree as ET 
import csv 

def parseXML(xmlfile): 
  
    # create element tree object 
    tree = ET.parse(xmlfile) 
  
    # get root element 
    root = tree.getroot() 
  
    # create empty list for news items 
    newsitems = [] 
  
    # iterate news items 
    for item in root.findall('./EXPERIMENT_PACKAGE'): 
        # empty news dictionary 
        news = {} 
  
        # iterate child elements of item 
        for child in item: 
  
            # special checking for namespace object content:media 
            if child.tag == '{http://search.yahoo.com/mrss/}content': 
                news['media'] = child.attrib['url'] 
            else: 
                news[child.tag] = child.text.encode('utf8') 
  
        # append news dictionary to news items list 
        newsitems.append(news) 
      
    # return news items list 
    return newsitems 

def savetoCSV(newsitems, filename): 
  
    # specifying the fields for csv file 
    fields = ['EXPERIMENT', 'SUBMISSION', 'Organization', 'STUDY', 'SAMPLE', 'Pool','RUN_SET'] 
  
    # writing to csv file 
    with open(filename, 'w') as csvfile: 
  
        # creating a csv dict writer object 
        writer = csv.DictWriter(csvfile, fieldnames = fields) 
  
        # writing headers (field names) 
        writer.writeheader() 
  
        # writing data rows 
        writer.writerows(newsitems) 
  
#newsitems = parseXML('efetchxml.xml')

# store news items in a csv file 
#savetoCSV(newsitems, 'topnews.csv') 




#for elem in tree.iter():
#    print (elem)

#print(root)
outdict={}
fields=['EXPERIMENT Accession','TITLE','STUDY_REF','DESIGN_DESCRIPTION','SAMPLE_Accession','LIBRARY_NAME','LIBRARY_STRATEGY',
        'LIBRARY_SOURCE','LIBRARY_SELECTION','LIBRARY_LAYOUT','PLATFORM']


def parse_experiment(expnode):
    fields=['EXPERIMENT','TITLE','STUDY_REF','DESIGN_DESCRIPTION','SAMPLE_DESCRIPTOR',
            'LIBRARY_NAME','LIBRARY_STRATEGY','LIBRARY_SOURCE','LIBRARY_SELECTION','LIBRARY_LAYOUT','PLATFORM']
    result=[]
    for child in expnode.iter():
        childtag=child.tag
        childval=child.text
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
    return ('\t'.join(result))

def parse_runset(run_set):
    result=[]
    #find runs in run set
    for r in run_set:
        result.append(parse_run(r))
    return result
    
def parse_run(run):
    result=[]
    fields=['RUN']
    for child in run.iter():
        childtag=child.tag
        childval=child.text
        childattrib=child.attrib
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
            
            


    
file = open("efetchall.xml",encoding='utf-8')
xmlline = file.read().replace("\n", " ")
file.close()

xmlstr='xmldata=<?xml version="1.0"  ?>'
xmldocs=xmlline.split(xmlstr)
#print((xmldocs[0]))
    
towrite=[]
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


for xml in xmldocs:
    #tree = ET.parse('efetchall.xml')
    #root = tree.getroot()
    #from string root = ET.fromstring(country_data_as_string)
    #tree = ET.parse('efetchxml.xml')
    root=ET.fromstring(xml)
    for exp_pck in root:
        i+=1
        print(i)
        outdict={}
        #print('outer',exp_pck.tag,'txt',exp_pck.text)
        #find Exp node
        thisexp=exp_pck.find("EXPERIMENT") 
        #print('TE:',thisexp,thisexp.attrib)
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
            #print ('\t'.join([exprow,sraid,r]))
            towrite.append('\t'.join([exprow,sraid,r]))


f=open('tsvout.tsv','w')
f.write('\t'.join(headers)+'\n')
f.write('\n'.join(towrite))
f.close()






      
      
