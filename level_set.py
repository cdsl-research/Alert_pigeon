import requests
import level_calculator
import csv
import json

# データの保存先
config_file = "config.json"
# 保存したファイルを読み込む --- (*3)
with open(config_file, "r") as f:
  setting = json.load(f)

url = setting["kiali_url"] + "/kiali/api/namespaces/graph?duration="+ setting["duration"] +"&graphType=app&includeIdleEdges=true&injectServiceNodes=true&boxBy=cluster,namespace,app&namespaces="+setting["namespaces"]

r = requests.get(url)

nodes = r.json()["elements"]["nodes"]
edges = r.json()["elements"]["edges"]

node_dict = {}
for node in nodes:
    if "service" in node["data"]:
       node_dict[node["data"]["id"]] = ["service", node["data"]["service"]]
    elif "app" in node["data"]:
        node_dict[node["data"]["id"]] = ["app", node["data"]["app"]]
print(len(node_dict))

dependent_list = []
for edge in edges:
    dependent_list.append((edge["data"]["source"], edge["data"]["target"]))
#print(dependent_list)

dependented_dict = {}
for edge in edges:
    if edge["data"]["source"] in dependented_dict:
        dependented_dict[edge["data"]["source"]] += 1
    else:
        dependented_dict[edge["data"]["source"]] = 1
relation_dict, alert_level = level_calculator.lcalc(dependent_list)

with open("node_data.csv", "w") as f:
    writer = csv.writer(f)
    for k, v in node_dict.items():
        writer.writerow([k, *v])

with open("level_data.csv", "w") as f:
    writer = csv.writer(f)
    for k, v in alert_level.items():
        writer.writerow([k, v])




print("###relation###")
for dependanted in dependented_dict:
    print(f"{node_dict[dependanted]}:{len(relation_dict[dependanted])}")
print("###alert_level###")
for dependanted in dependented_dict:
    print(f"{node_dict[dependanted]}:{alert_level[dependanted]}")