def lcalc(items):
    relation_dict = {}
    for item in items:
        if item[0] in relation_dict:
            set.add(relation_dict[item[0]], item[1])
        else:
            relation_dict[item[0]] = set([item[1]])

    for i in relation_dict:
        for target, sources in relation_dict.items():
            for source in sources:
                if source in relation_dict:
                    relation_dict[target] = relation_dict[target].union(relation_dict[source])
    #print(relation_dict)

    relation_count = {}
    for target,sources in relation_dict.items():
        relation_count[target] = len(sources)
        #print(sources)

    level = (max(relation_count.values()) - min(relation_count.values()))

    relation_count = sorted(relation_count.items(), key=lambda x:x[1])
    alert_level = {}
    print(len(relation_count))
    i=0
    for (target,count) in relation_count:
        if i < len(relation_count)/4:
            target_level = 1
        elif i < len(relation_count)/2:
            target_level = 2
        elif i < len(relation_count)*3/4:
            target_level = 3
        else:
            target_level = 4
        alert_level[target] = target_level
        i+=1

    return (relation_dict,alert_level)