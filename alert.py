import requests
import csv
import json
import time

def alert(output_count):

    alert_level = {}
    # データの保存先
    config_file = "config.json"
    rule_file = "rule.json"
    # 保存したファイルを読み込む --- (*3)
    with open(config_file, "r") as f:
        setting = json.load(f)

    with open(rule_file, "r") as f:
        rule = json.load(f)

    with open("node_data.csv", mode="r") as inp:
        reader = csv.reader(inp)
        node_dict = {rows[0]: [rows[1], rows[2]] for rows in reader}

    with open("level_data.csv", mode="r") as inp:
        reader = csv.reader(inp)
        alert_level = {rows[0]: rows[1] for rows in reader}

    #url = setting["kiali_url"]+"/kiali/api/namespaces/"+setting["namespaces"]+"/"+type+"/"+target+"/metrics"
    url2 = setting["kiali_url"]+"/kiali/api/namespaces/graph?duration=500s&graphType=app&injectServiceNodes=true&appenders=responseTime&namespaces=sock-shop"
    #print(url2)
    r = requests.get(url2)
    data = r.json()
    #print(data)

    request_dict = {}
    latency_dict = {}
    for edge in r.json()["elements"]["edges"]:
        if edge["data"]["traffic"]["protocol"] == "http":
            request_dict[edge["data"]["source"]] = float(edge["data"]["traffic"]["rates"]["http"])
        if "responseTime" in edge["data"]:
            latency_dict[edge["data"]["source"]] = edge["data"]["responseTime"]
    
    request_dict = sorted(request_dict.items(), key=lambda x:x[1], reverse=True)

    print("###RPS###")
    output_count+=1
    for rps in request_dict:
        print(f"{node_dict[rps[0]][1]}:{rps[1]}")
        output_count+=1

    alerts = []
    #print("###ResponceTime###")
    #output_count+=1
    for node, latency in latency_dict.items():
        print(f"{node_dict[node][1]}:{latency}")
        output_count+=1
        if node_dict[node][1] in rule:
            if rule[node_dict[node][1]] < int(latency):
                alerts.append([alert_level[node], node_dict[node][1]])
    return (request_dict, alerts,output_count)

if __name__ == '__main__':
    while True:
        output_count = 0
        _,alerts,output_count = alert(output_count)
        #print("###alert###")
        #output_count+=1
        #alerts.sort(reverse=True)
        #for alert in alerts:
        #    print(f"{alert[0]}:{alert[1]} is too late.           ")
        #    output_count+=1

        time.sleep(3)
        for i in range(output_count):
            print(" "*50)
            print("\033[3A")