
# Libraries
# Selenium: accessing websites and automation testing
# Pandas: for structuring our data
# Time, datetime: using delays and returning current
# smtplib: connecting to our email and sending our message

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart


#Connect to the Web Browser
#browser = webdriver.Chrome(executable_path='/chromedriver')
browser = webdriver.Chrome("/usr/local/bin/chromedriver")
browser.maximize_window() # For maximizing window
browser.implicitly_wait(20) # gives an implicit wait for 20 seconds

#For the departure country
#Setting ticket types paths
# To obtain this labels IDs, quickly go to Expedia to check the interface and the options available to choose from.
# Use right click + inspect option on the ticket type buttons (roundtrip, one way, etc.) to see the tags related to it.

return_ticket = "//*[@id='wizard-flight-tab-roundtrip']/div[2]/div[1]/div/div[1]/div/div/div[2]/div[1]/button']"
one_way_ticket = "//label[@id='flight-type-one-way-label-hp-flight']"
multi_ticket = "//label[@id='flight-type-multi-dest-label-hp-flight']"

#Choose a ticket type
# This function looks for tags and ids or other attributes and makes the choice on the web page.
def ticket_chooser(ticket):

    try:
        ticket_type = browser.find_element(by=By.XPATH, value=ticket)
        ticket_type.click()
    except Exception as e:
        pass

# choose the departure country
def dep_country_chooser(dep_country):
    #//*[@id="location-field-leg1-origin"]
    fly_from = browser.find_element(by=By.XPATH, value="//input[@id='flight-origin-hp-flight']")
    fly_from.clear()
    time.sleep(1.5)
    fly_from.send_keys('  ' + dep_country)
    time.sleep(1.5)
    first_item = browser.find_element(by=By.XPATH, value="//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_item.click()

# For the arrival country

def arrival_country_chooser(arrival_country):
    fly_to = browser.find_element(by=By.XPATH, value="//input[@id='flight-destination-hp-flight']")
    time.sleep(1)
    fly_to.clear()
    time.sleep(1.5)
    fly_to.send_keys('  ' + arrival_country)
    time.sleep(1.5)
    first_item = browser.find_element(by=By.XPATH, value="//a[@id='aria-option-0']")
    time.sleep(1.5)
    first_item.click()

# Departure date
def dep_date_chooser(month, day, year):

    dep_date_button = browser.find_element(by=By.XPATH, value="//input[@id='flight-departing-hp-flight']")
    dep_date_button.clear()
    dep_date_button.send_keys(month + '/' + day + '/' + year)

#Return date:
def return_date_chooser(month, day, year):
    return_date_button = browser.find_element(by=By.XPATH, value="//input[@id='flight-returning-hp-flight']")

    for i in range(11):
    # For the return date, clearing whatever was written wasn’t working for some reason (probably due to the page having this 
    # as autofill not allowing me to override it with .clear())
    # The way I worked around this is by using Keys.BACKSPACE which simply tells Python to click backspace 
    # (to delete whatever is written in the date field)
        return_date_button.send_keys(Keys.BACKSPACE)
    return_date_button.send_keys(month + '/' + day + '/' + year)

# This function will click the search button.
def search():
    search = browser.find_element(by=By.XPATH, value="//button[@class='btn-primary btn-action gcw-submit']")
    search.click()
    time.sleep(15)
    print('Results ready!')

# Compiling the Data
#Connect Python to our web browser and access the website (Expedia in our example here).
#Choose the ticket type based on our preference (round trip, one way, etc.).
#Select the departure country.
#Select the arrival country (if round trip).
#Select departure and return dates.
#Compile all available flights in a structured format (for those who love to do some exploratory data analysis!).
#Connect to your email.
#Send the best rate for the current hour.

df = pd.DataFrame()
def compile_data():
    global df
    global dep_times_list
    global arr_times_list
    global airlines_list
    global price_list
    global durations_list
    global stops_list
    global layovers_list

    #departure times
    dep_times = browser.find_element(by=By.XPATH, value="//span[@data-test-id='departure-time']")
    dep_times_list = [value.text for value in dep_times]

    #arrival times
    arr_times = browser.find_element(by=By.XPATH, value="//span[@data-test-id='arrival-time']")
    arr_times_list = [value.text for value in arr_times]

    #airline name
    airlines = browser.find_element(by=By.XPATH, value="//span[@data-test-id='airline-name']")
    airlines_list = [value.text for value in airlines]

    #prices
    prices = browser.find_element(by=By.XPATH, value="//span[@data-test-id='listing-price-dollars']")
    price_list = [value.text.split('/div>')[1] for value in prices]

    #durations
    durations = browser.find_element(by=By.XPATH, value="//span[@data-test-id='duration']")
    durations_list = [value.text for value in durations]

    #stops
    stops = browser.find_element(by=By.XPATH, value="//span[@class='number-stops']")
    stops_list = [value.text for value in stops]

    #layovers
    layovers = browser.find_element(by=By.XPATH, value="//span[@data-test-id='layover-airport-stops']")
    layovers_list = [value.text for value in layovers]

    now = datetime.datetime.now()
    current_date = (str(now.year) + '-' + str(now.month) + '-' + str(now.day))
    current_time = (str(now.hour) + ':' + str(now.minute))
    current_price = 'price' + '(' + current_date + '---' + current_time + ')'
    for i in range(len(dep_times_list)):
        try:
            df.loc[i, 'departure_time'] = dep_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'arrival_time'] = arr_times_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'airline'] = airlines_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'duration'] = durations_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'stops'] = stops_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, 'layovers'] = layovers_list[i]
        except Exception as e:
            pass
        try:
            df.loc[i, str(current_price)] = price_list[i]
        except Exception as e:
            pass

    print('Excel Sheet Created!')

#Setting Up Our Email Functions

#email credentials
username = 'myemail@hotmail.com'
password = 'XXXXXXXXXXX'

#Connect

def connect_mail(username, password):
    global server
    server = smtplib.SMTP('smtp.outlook.com', 587)
    server.ehlo()
    server.starttls()
    server.login(username, password)

#Create the Message

#Create message template for email
def create_msg():
    global msg
    msg = '\nCurrent Cheapest flight:\n\nDeparture time: {}\nArrival time: {}\nAirline: {}\nFlight duration: {}\nNo. of stops: {}\nPrice: {}\n'.format(cheapest_dep_time,
                       cheapest_arrival_time,
                       cheapest_airline,
                       cheapest_duration,
                       cheapest_stops,
                       cheapest_price)

#Send the Message
def send_email(msg):
    global message
    message = MIMEMultipart()
    message['Subject'] = 'Current Best flight'
    message['From'] = 'myemail@hotmail.com'
    message['to'] = 'myotheremail@hotmail.com'

    server.sendmail('myemail@hotmail.com', 'myotheremail@hotmail.com', msg)

# Save our DataFrame to an Excel sheet and sleep for 3600 seconds (1 hour).
# This loop will run 8 times in one-hour intervals, thus it will run for 8 hours. 
# You can tweak the timing to your preference.

for i in range(8):    
    link = 'https://www.expedia.com/'
    browser.get(link)
    time.sleep(5)

    #choose flights only
    #browser.maximize_window() # For maximizing window
    #browser.implicitly_wait(20) # gives an implicit wait for 20 seconds
    flights_only = browser.find_element(by=By.XPATH, value="//*[@id='wizardMainRegionV2']/div/div/div/div/ul/li[2]/a/span")
    flights_only.click()

    ticket_chooser(return_ticket)

    dep_country_chooser('Costa Rica')

    arrival_country_chooser('Madrid')

    dep_date_chooser('06', '06', '2023')

    return_date_chooser('05', '07', '2023')

    search()

    compile_data()

    #save values for email
    current_values = df.iloc[0]

    cheapest_dep_time = current_values[0]
    cheapest_arrival_time = current_values[1]
    cheapest_airline = current_values[2]
    cheapest_duration = current_values[3]
    cheapest_stops = current_values[4]
    cheapest_price = current_values[-1]

    print('run {} completed!'.format(i))

    create_msg()
    connect_mail(username,password)
    send_email(msg)
    print('Email sent!')

    df.to_excel('flights.xlsx')

    time.sleep(3600)
