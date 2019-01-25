import dateutil.parser
import re
import csv
import os, errno
import io
import json
import sys
from pprint import pprint
from datetime import datetime
import argparse

import helpers


def timestamp_usec_to_datetime(t):
    d = datetime.fromtimestamp(float(t) / 1000000.0)
    return d

############## define input arguments

parser = argparse.ArgumentParser(description='Consolidate JSON files and output as simplified JSON/CSV')
parser.add_argument('-d','--dir', help='Directory containing Google Takeout JSON files')
parser.add_argument('-o','--output', help='Output filename for .csv and .json files')
args = vars(parser.parse_args())


############## get all filenames
path_to_json = 'TakeoutData/' if args['dir'] == None else args['dir']

print(" ")
print(" ===  Reading JSON files in '" + path_to_json + "'...")

json_files = [os.path.join(root, f) for root, subdirs, files in os.walk(path_to_json) for f in files if f.endswith('.json')]

print(" ===  Combining JSON files...",)

if(len(json_files) == 0):
    print("There are no JSON files in " + path_to_json + "!")
    sys.exit(0)

############# concat all jsons into list (let's hope this doesn't break on large numbers of json)
alljsons = []
for f in json_files:
    print("..processing..",)
    with open(f) as data:
        d = json.load(data)
        alljsons.extend(d)


print("")
print(" ===  Creating simple JSON...")

############ make a super simple json
simplejson = []
for j in alljsons:

#    print(j)
    m = re.search('Searched for (.*)', j['title'])
    if(m):
        single_query = {}
        single_query["data_query"] =  m.group(1)
        d = dateutil.parser.parse(j['time'])
        single_query["timestamp_usec"] = d.timestamp()
        single_query["datetime"] = d.strftime("%m/%d/%Y %I:%M:%S %p")
        single_query["month"] = int(d.strftime("%m"))
        single_query["day"] = int(d.strftime("%d"))
        single_query["year"] = int(d.strftime("%Y"))
        single_query["hour"] = int(d.strftime("%H"))
        single_query["minute"] = int(d.strftime("%M"))
        single_query["second"] = int(d.strftime("%S"))
        single_query["weekofyear"] = int(d.strftime("%U"))
        single_query["weekday"] = d.strftime("%a")
        single_query["dayofmonth"] = int(d.strftime("%d"))
        simplejson.append(single_query)


############ sort json into chronological order
simplejson.sort(key=lambda x: x['timestamp_usec'])

## either use output filename, or get the date range of all queries
if(args['output'] == None):
    daterange = ""
    daterange += timestamp_usec_to_datetime(simplejson[0]['timestamp_usec']).strftime("%m-%d-%Y")
    daterange += "_to_"
    daterange += timestamp_usec_to_datetime(simplejson[-1]['timestamp_usec']).strftime("%m-%d-%Y")
    #filebase = 'all_google_queries_simplified__' + daterange
    filebase = 'all_google_queries_simplified' 
else:
    filebase = args['output']

print(" ===  Writing CSV...")


########### create directory
helpers.create_dir(helpers.outputdir)

########### write a csv!
helpers.csvsave(helpers.outputdir + filebase + '_tsv.txt', simplejson)

print(" ===  Writing JSON...")

########### write a JSON!

helpers.jsonsave(helpers.outputdir + filebase + '.json', simplejson)

print(" ===  Done! Files were created at '" + helpers.outputdir + filebase + "_tsv.txt' and '" + helpers.outputdir + filebase + ".json'")
if(args['output'] == None):
    print(" ===  Now copy and paste `python google_2_pickout_queries.py` and press enter!")
else:
    print(" ===  Now try running `python google_2_pickout_queries.py -j " + filebase + ".json` ! ")
print(" ")
