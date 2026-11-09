from bs4 import BeautifulSoup


def table_rows(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if table is None:
        return []
    rows = []
    for tr in table.find_all("tr"):
        rows.append([cell.get_text(strip=True) for cell in tr.find_all(["th", "td"])])
    return rows
