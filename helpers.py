import csv
import io
import json

fieldnames = ["timestamp_usec", "datetime","month", "day", "year", "hour", "minute", "second", "weekofyear", "weekday", "dayofmonth" ,"data_query"]

def csvsave(filename, data):
    with open(filename, 'w') as fout:
        fout.write(u'\ufeff'.encode('utf8')) #  (optional...Excel needs it to open UTF-8 file properly)
        writer = csv.DictWriter(fout, fieldnames=fieldnames, delimiter="\t")    
        writer.writeheader()
        for row in data[1:]:
            writer.writerow({k:unicode(v).encode('utf8') for k,v in row.items() })

def jsonsave(filename, data):
    with io.open(filename, 'w', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False))

