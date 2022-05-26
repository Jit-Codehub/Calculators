import requests

headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"}

url = "https://apiprod.timesnownews.com/request/photostorylist?seopath=web-stories/sports&pageno={}&itemcount=22&origin=desktop"

pageno=1
urls = []

while True:
    response = requests.get(url.format(pageno), headers= headers)
    data = response.json()
    d = data['response']['sections']['sports']['items']
    for i in d:
        for key, value in i.items():
            if key == 'url':
                urls.append(value.strip())
    if int(data['response']['sections']['sports']['total_records']) > len(urls):
        pageno+=1
    else:
        urls = set(urls)
        file_name="url1.txt"
        with open(file_name, "w") as outfile:
            outfile.write('\n'.join(urls))
            break
