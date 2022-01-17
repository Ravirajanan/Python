#packages
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import urllib


#using selenium to open webpage
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.certipedia.com/search/certified_companies?locale=en")

#parsing the data to a soup 
html_ = driver.page_source
soup = BeautifulSoup(html_,'lxml')

#getting all companies on the certifications list
ul_ = soup.find('ul', class_ = 'links search-results')
company_list = []
for i in ul_.find_all('li'):
    l = []
    if i.span.a:
        l.append(i.span.a['href'].strip())
        
    k= (i.text.strip('\n').split('\n'))
    l.extend(k)
    company_list.append(l)

#getting cookie details for header
l=[]
for i  in driver.get_cookies():
    l.append(i["name"]+'='+i['value'])
headers = requests.structures.CaseInsensitiveDict()
headers["Cookie"] = (';'.join(l))
headers['User-Agent']= """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"""
headers['Accept']="""text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"""
headers['Accept-Encoding']="""gzip, deflate, br"""
headers['Accept-Language']="""en-US,en;q=0.9"""
headers['Cache-Control']="""max-age=0"""
headers['Connection']="""keep-alive"""
# header created.

#getting certificate details from each company
data = []
for rr in range (len(company_list)):
    i = company_list[rr][0]
    url = """https://www.certipedia.com"""+i
    source = requests.get(url, headers = headers).text
    soup = BeautifulSoup(source, 'lxml')
    res = soup.find_all('tbody', class_ = 'search-results')
    for k in res:
        for tr in k.find_all('tr'):
            l = []
            for td in tr.find_all('td'):
                if td.a:
                    k = td.a
                    if k['href']:
                        l.append(k['href'].strip())
                    else:
                        l.append('-')
                if td.text:
                    l.append(td.text.strip())
                else:
                    l.append('-')
                
            l.append(company_list[rr][1])
            l.append(company_list[rr][3])
            data.append(l)

#getting more certificate info and creating data frame
final_data = []
for i in range(len(data)):
    url = data[i][2]
    certificate_no = url
    url_list = url.split('/')
    if url_list[1] == 'quality_marks':
        url = """https://www.certipedia.com""" + url
        certificate_no = certificate_no[55:]
        certificate_no = urllib.parse.unquote(certificate_no)
        certificate_no = certificate_no.replace('+', ' ')
        company_name = data[i][4]
        certificate_type = data[i][0]
        certificate_scope = data[i][1]
        address = data[i][-1]
        test_mark_number = data[i][3]
        source = requests.get(url, headers = headers).text
        soup = BeautifulSoup(source, 'lxml')
        image = soup.find('div', class_='quality_mark_logo')
        image = image.find('img')
        if image:
            image = """https://www.certipedia.com"""+image['src']
        else:
            image = '-'
        additional_info = soup.find('tr', class_ = 'emphasized_information')
        if additional_info:
            td = additional_info.find_all('td')
            additional_info = (td[-1].text.strip())
        else:
            additional_info = '-'
        
    else:
        certificate_no = url_list[2]
        certificate_no = certificate_no.split('?')
        certificate_no = certificate_no[0]
        certificate_no = urllib.parse.unquote(certificate_no)
        certificate_no = certificate_no.replace('+', ' ')
        company_name = data[i][4]
        company_name = data[i][4]
        certificate_type = data[i][0]
        certificate_scope = data[i][1]
        address = data[i][-1]
        test_mark_number = '-'
        image = '-'
        additional_info = '-'
    
    l = [company_name,certificate_type,certificate_no,test_mark_number,certificate_scope,address, image, additional_info]
    final_data.append(l)
columns_ = ['Company Name','Certificate Type', 'Certificate No', 'Test Mark Number', 'Certificate Scope', 'Address', 'image', 'Additional Info']
company_dataframe = pd.DataFrame(final_data, columns = columns_)
company_dataframe.set_index(['Company Name','Certificate Type'], inplace = True)
company_dataframe.to_csv("task_2_output.csv")