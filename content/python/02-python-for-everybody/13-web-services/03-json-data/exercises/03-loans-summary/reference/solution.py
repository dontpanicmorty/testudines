import json


def summarize_loans(json_text):
    totals = {}
    for loan in json.loads(json_text):
        totals[loan["member"]] = totals.get(loan["member"], 0) + loan["days"]
    return json.dumps(totals, sort_keys=True)
