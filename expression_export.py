import json


def findExpression(obj) -> list:
    expr_list = []
    if isinstance(obj, dict):
        if "expr" in obj.keys():
            expr_list.append(obj["expr"])
        for key, value in obj.items():
            expr_list.extend(findExpression(value))
    elif isinstance(obj, list):
        for item in obj:
            expr_list.extend(findExpression(item))
    return expr_list


def get_expressions():
    with open("data/grafana-dashboard.json") as grafana_json:
        grafana = json.load(grafana_json)
        print(grafana)
        expressions = findExpression(grafana)
        print(expressions)
        for expr in expressions:
            print(expr + ",")
