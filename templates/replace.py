from bs4 import BeautifulSoup as bs

data = ''
with open('base copy 2.html', 'r', encoding='utf-8') as f:
    data = f.read()
    soup = bs(data, "html.parser")
    for item in soup.select("a"):
        print(item)
        print(item['title'])
    f.close()