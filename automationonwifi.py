from selenium import webdriver
import smtplib, ssl
import time
from webdriver_manager.microsoft import EdgeChromiumDriverManager

##A Fucntion which will send a message.
def sendanemail():
    port = 587
    smtp_server = "smtp.gmail.com"
    sender_email = 'sender@gmail.com'#sendeer Email address
    receiver_email = 'sender@gmail.com'#Receiver Email address
    password = '********'
    
    message = """\
    There are new devices connected to your wifi, Kinldy check and validate"""
    
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)

#Funtion which will perform validation.
def validation(mydevices_macaddress, final_data_array):
    count = True
    for x in final_data_array:
        if (x[0] not in mydevices_macaddress):
            count = False
    if count == False:
        sendanemail()

#The following code is using Edge web driver to open the admin page of wifi router 
#Get the mac addresses connected to the device.
driver = webdriver.Edge(EdgeChromiumDriverManager().install())
driver.get('http://Username:Password@192.168.1.1/')
frame = driver.find_element_by_xpath('//frame[@name="title"]')
driver.switch_to_frame(frame)
driver.find_element_by_xpath('//*[@id="s6"]/a').click()

time.sleep(2)

driver.switch_to_default_content()
frame = driver.find_element_by_xpath('//frame[@name="title"]')
driver.switch_to_frame(frame)
frame = driver.find_element_by_xpath('//*[@id="mainFrameid"]')
driver.switch_to_frame(frame)
mac = driver.find_element_by_xpath('/html/body/blockquote/table[4]/tbody').text
lis = list(map(str, mac.splitlines()))
print(lis)
lis = lis[2:]
final_data_array = []
for elements in lis:
    elements = elements.split(' ')
    final_data_array.append(elements)


#validation.
#I have the list of mac addresses of my devices which i connect to my WIFI.
mydevices_macaddress = ['*****', '*****', '*****']
#mydevices_macaddress contains list of all mac addressess of your devices.
validation(mydevices_macaddress, final_data_array)

