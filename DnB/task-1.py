from bs4.element import SoupStrainer
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

#using selenium to open webpage
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.epa.gov/greenpower/green-power-partnership-national-top-100")
time.sleep(5)

#parsing the data to a soup 
html_ = driver.page_source
soup = BeautifulSoup(html_,'lxml')

#selecting table data using class attribute
table_ = soup.find("table", class_ = "tablebord")
table_head = table_.find("thead")
columns_ = [i.text for i in table_head.find_all('th')]

#adding the data to a dataframe
list_ = []
table_body = table_.find("tbody")
for i in table_body.find_all('tr'):
    l = [j.text for j in i.find_all('td')]
    name = i.find('a')
    l[0] = name.text
    list_.append(l)
    
dataframe = pd.DataFrame(list_,columns=columns_)

#print dataframe and store it to csv
print(dataframe)
dataframe.to_csv('task_1_output.csv')
driver.close()