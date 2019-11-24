#!/usr/bin/env python
# coding: utf-8

# In[2]:


pip install selenium


# In[3]:


from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup, Comment
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains


# In[2]:


import os
os.chdir('/path/reviews')


# In[4]:


driver = webdriver.Chrome()
driver.maximize_window()

# URL of the reviews page
link = "https://play.google.com/store/apps/details?id=com.snapchat.android&hl=en_US"
driver.get(link)
##Load full Review Page
driver.find_element_by_css_selector('#fcxH9b > div.WpDbMd > c-wiz > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div.XnFhVd > div').click()


# In[4]:


##Check the name of app
Ptitle = driver.find_element_by_class_name('AHFaub').text.replace(' ','')
print(Ptitle)


# In[6]:


#Function for scrolling page down
def scroll_down():
    """A method for scrolling the page."""

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")
    try:
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page.
            time.sleep(0.2)

        # Calculate new scroll height and compare with last scroll height.
            new_height = driver.execute_script("return document.body.scrollHeight")
        
            time.sleep(0.2)
            if new_height == last_height:
                break
            last_height = new_height
    except NoSuchElementException:
        pass


# In[ ]:


#Loading page till the date you want the reviews
for i in range(1,600):
    try:
        scroll_down()
        driver.find_element_by_css_selector('#fcxH9b > div.WpDbMd > c-wiz:nth-child(4) > div > div.ZfcPIb > div > div.JNury.Ekdcne > div > div > div.W4P4ne > div:nth-child(2) > div.PFAhAf > div').click()
        
    except:
        pass


# In[9]:


#Finding all the div elements
all_elem = driver.find_elements_by_xpath('//div[@jscontroller="H6eOGe"]')


# In[ ]:


all_reviews = []
for i in all_elem:
    try:
        content = i.get_attribute('outerHTML')
        soup = BeautifulSoup(content, 'html.parser')
        ##Review Date
        date = soup.find('span', attrs={'class':'p2TkOb'}).text.strip()
        #Review Rating
        rating = soup.find('div', attrs={'class':'pf5lIe'}).find('div')["aria-label"].split()[1]
        #Review has been helpful
        helpful = soup.find('div', attrs={'class':'jUL89d y92BAb'}).text.strip()
        ##Comment Description
        desc = soup.find('div', attrs={'class':'UD7Dzf'}).text.strip()
        temp = pd.DataFrame({'Date':date,'Rating':rating,'Helpful':helpful,'Review Text':desc},index=[0])
        all_reviews.append(temp)
        print('.', end = " ")
        time.sleep(0.2)
    except:
        pass


# In[12]:


all_reviews = pd.concat(all_reviews,ignore_index=True)


# In[13]:


all_reviews.to_csv('Reviews.csv')

