import os, errno
import csv
import io
import json
import codecs

fieldnames = ["timestamp_usec", "datetime","month", "day", "year", "hour", "minute", "second", "weekofyear", "weekday", "dayofmonth" ,"data_query"]

def csvsave(filename, data):
    with codecs.open(filename, 'w', 'utf-8') as fout:
        fout.write(u'\uFEFF') #  (Excel needs it to open UTF-8 file properly)
        writer = csv.DictWriter(fout, fieldnames=fieldnames, delimiter="\t")    
        writer.writeheader()
        for row in data[1:]:
#            writer.writerow({k:str(v).encode('utf8') for k,v in row.items() })
            writer.writerow({k:str(v) for k,v in row.items() })

def jsonsave(filename, data):
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))

def create_dir(filedir):
    try:
        os.makedirs(filedir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

outputdir = "Processed_Searches/"
