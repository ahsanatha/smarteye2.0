
import json

newdata = {
            "id" : "2",
            "place": "Asrama2",
            "title" : "A man stole motorcycle2",
            "reporter": "Dhamir2",
            "image": "http://192.168.0.110:5000/static/Camera%204/0.jpg",
            "date": "2019-11-09",
            "time": "14:46:09",
            "elapsed": 1573284951.7094495
        }

with open('report.json') as data_file:    
    old_data = json.load(data_file)
    # print(old_data['report'])

    # Get last index
    # print(len(old_data['report'])-1)
    
    # Get for new index
    # print(len(old_data['report']))
    old_data['report'].append(newdata)

    with open('report.json', 'w') as data_write:
        json.dump(old_data, data_write, indent=4, sort_keys=True)
    # print(old_data['report']) 