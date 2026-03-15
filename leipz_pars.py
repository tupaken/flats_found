import requests
from bs4 import BeautifulSoup

class leipzig_pars:

    def __init__(self):
        self.url = "https://www.leipzig.de/leben-in-leipzig/bauen-und-wohnen/wohnen/sozialwohnung?tx_lepurpose%5Bfilter%5D%5Bkeyword%5D=&tx_lepurpose%5Bfiltered%5D=1&tx_lepurpose%5Bfilter%5D%5Bsortorder%5D=asc&tx_lepurpose%5Bfilter%5D%5Bsortby%5D=sorting&tx_lepurpose%5Bfilter%5D%5Bpage%5D=1&tx_lepurpose%5Bfilter%5D%5B1365%5D%5B%5D=7385&tx_lepurpose%5Bfilter%5D%5B1484%5D%5B%5D=7665#c374892"
        self.req = requests.get(self.url, timeout=20, headers={
        "User-Agent": "Mozilla/5.0 (compatible; MyParser/1.0)"})
        self.state=self.req.raise_for_status()
        self.last_flat="/leben-in-leipzig/bauen-und-wohnen/wohnen/sozialwohnung/detail/projekt/martinshoehe-15-1"

    def pars(self):
        print(self.state)
        soup = BeautifulSoup(self.req.text, "html.parser")
        el=soup.find_all("a",class_=["link-teaser"])
        urls = [e.get("href") for e in el]
        if len(urls)%20!=0:
            return urls
        stop=True
        count=2
        while(stop):
            url2=f"https://www.leipzig.de/leben-in-leipzig/bauen-und-wohnen/wohnen/sozialwohnung?tx_lepurpose%5Bfilter%5D%5Bkeyword%5D=&tx_lepurpose%5Bfiltered%5D=1&tx_lepurpose%5Bfilter%5D%5Bsortorder%5D=asc&tx_lepurpose%5Bfilter%5D%5Bsortby%5D=sorting&tx_lepurpose%5Bfilter%5D%5Bpage%5D={count}&tx_lepurpose%5Bfilter%5D%5B1365%5D%5B%5D=7385&tx_lepurpose%5Bfilter%5D%5B1484%5D%5B%5D=7665#c374892"
            req = requests.get(url2, timeout=20, headers={ "User-Agent": "Mozilla/5.0 (compatible; MyParser/1.0)"})
            req.raise_for_status()
            soup2 = BeautifulSoup(req.text, "html.parser")
            el2=soup2.find_all("a",class_=["link-teaser"])
            urls2 = [e2.get("href") for e2 in el2]
            count+=1
            if len(urls2)<1:
                count=2
                stop=False
            else:
                urls+=urls2
        return urls

    def get_new_flats(self):
        urls=self.pars()
        #last_url=urls.pop()
        #print("******** "+last_url)
        for i in range(len(urls) - 1, -1, -1):
            if urls[i]==self.last_flat:
                return urls[i+1:]


print(leipzig_pars().get_new_flats())