import pandas
import requests
from bs4 import BeautifulSoup

def city_names_extracter(country):
    city_names_data = requests.get(("https://www.yelp.co.uk/locations/countries/{}").format(country))
    city_names_data.status_code

    data_city_names = BeautifulSoup(city_names_data.content, 'html.parser')

    cities = []
    for i in data_city_names.select('li a'):
        if i.text!= "About Yelp":
            cities.append(i.text)
        else:
            break

    return cities

cities = city_names_extracter('nz')
cities_copy = cities
len(cities)

def city_url_generator(cities_list):
    city_wise_urls =[]
    edited_cities_list = []
    for i in cities_list:
        if i not in edited_cities_list:
                edited_cities_list.append(i)
                
        if " " in i:
            cities_list.remove(i)
            s = '%2'
            edit = i.strip().split()
            joined = s.join(edit)
            cities_list.append(joined)
            
    for j in edited_cities_list:
        url = "https://www.yelp.com/search?cflt=restaurants&find_loc={}%2C+New+Zealand".format(j)
        city_wise_urls.append(url)
    return city_wise_urls

all_citywise_urls = city_url_generator(cities_copy)
all_city_wise_urls_copy = all_citywise_urls
len(city_url_generator(cities_copy))
all_city_wise_urls_copy

def pages_for_each_city(cities_urls):
    total_pages = []
    for t in cities_urls:
        h = requests.get(t)
        sou = BeautifulSoup(h.content, 'html.parser')
        pages_count = sou.find_all('span')[-21].text[-1]
        if bool(re.search(r'\d', pages_count)):
            total_pages.append(pages_count)
    return total_pages

# bool(re.search(r'\d', inputString))
pages_for_each_city(all_city_wise_urls_copy)
total_pages_citywise = pages_for_each_city(all_city_wise_urls_copy)
total_pages_citywise_copy = total_pages_citywise

def businesses_name_extractor(cities_names_list):
    all_names = []
    basic_urls_citywise =[]
    for n in cities_names_list:
        basic_urls_each_city =[]
        names_here = []
        url = "https://www.yelp.com/search?cflt=restaurants&find_loc={}%2C+New+Zealand".format(n)
        req_url = requests.get(url)
        soup_url = BeautifulSoup(req_url.content, 'html.parser')
        here = soup_url.select('h4 span a')
        for all_in_here in here:
            names_here.append(all_in_here.text)
        available_pages = soup_url.find_all('span')[-21].text[-1]
        start =10
        try:
            while start< (10*int(available_pages)):
                further_urls ="https://www.yelp.com/search?cflt=restaurants&find_loc={}&start={}".format(n, start)
                basic_urls_each_city.append(further_urls)
                req_further = requests.get(further_urls)
                soup_further = BeautifulSoup(req_further.content, 'html.parser')
                further_names = soup_further.select('h4 span a')
                for each_further in further_names:
                    names_here.append(each_further.text)
                start = start+10
        except:
            pass
        basic_urls_citywise.append(basic_urls_each_city)
        all_names.append(names_here)
    return all_names, basic_urls_citywise


restaurants_names = businesses_name_extractor(cities_copy)
restaurants_names_copy = restaurants_names

import smtplib 

# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 

from_add = environ['KK_ID']
to_add = from_add
pw = environ['KK_PW']
# start TLS for security 
s.starttls() 

# Authentication 
s.login("sender_email_id", "sender_email_id_password") 

# message to be sent 
message = restaurants_names_copy

# sending the mail 
s.sendmail("sender_email_id", "receiver_email_id", message) 

# terminating the session 
s.quit() 
