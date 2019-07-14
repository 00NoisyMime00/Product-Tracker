import requests
from bs4 import BeautifulSoup

url = 'https://www.proxynova.com/proxy-server-list/country-in/'


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
}



def getELiteProxies():
    proxies = {}
    response = requests.get(url, headers=headers)
    

    soup = BeautifulSoup(response.content, 'html.parser')

    proxyTable = soup.find('table', attrs={'id':'tbl_proxy_list'}).find('tbody')

    tableRows = proxyTable.find_all('tr')


    for row in tableRows:
        x = row.find_all('td')
        try:
            if x[6].text.strip() == 'Elite':
                ip_test = x[0].find('abbr').get('title').strip()
                
                flag = 0

                for c in ip_test:
                    if c.isalpha() and c != '.':
                        flag = 1
                        break
                if flag == 1:
                    break

                try:
                    port = x[1].find('a').text.strip()
                except:
                    port = x[1].text.strip()

                ip = 'http://'+ip_test+':'+port
                print(ip)

                proxies = {'http':ip,'https':ip}

                try:
                    if requests.get('https://flipkart.com',proxies=proxies,headers=headers,timeout=20).status_code == 200:
                        print('worked!')
                        print(proxies,'returning this..')
                        return proxies
                        
                except:
                    print('FAIL')
                
        except:
            
            print('ERROR IN PROXY')
            print('+++++++')
            pass
    

if __name__ == '__main__':             
    proxies = getELiteProxies()
    print(proxies)
    