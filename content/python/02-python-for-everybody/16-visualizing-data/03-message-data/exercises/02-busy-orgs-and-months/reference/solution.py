def clean_sender(text):
    text = text.strip()
    if "<" in text and ">" in text:
        text = text[text.index("<") + 1 : text.index(">")]
    return text.strip().lower()


def activity(messages):
    orgs = {}
    months = {}
    for sender, date in messages:
        domain = clean_sender(sender).split("@")[-1]
        org = ".".join(domain.split(".")[-2:])
        orgs[org] = orgs.get(org, 0) + 1
        months[date[:7]] = months.get(date[:7], 0) + 1
    return {
        "by_org": sorted(orgs.items(), key=lambda kv: (-kv[1], kv[0])),
        "by_month": sorted(months.items()),
    }
