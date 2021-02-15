from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
import datetime

import emailer
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only

#headless option
#chrome_options.add_argument("--headless")
logFile = open('vaxBotLog.txt', 'a')
logFile.write('\n open file: {} \n'.format(datetime.datetime.now()))
try:
    # chrome_options.headless = True # also works
    driver = webdriver.Chrome(options=chrome_options)
    url = "https://www.cvs.com/immunizations/covid-19-vaccine"
    driver.get(url)

    assert "COVID Vaccine (COVID-19 Immunization Updates)" in driver.title

    driver.find_element_by_link_text('New Jersey').click()

    cities = driver.find_elements_by_class_name("city")
    vaxStatus = driver.find_elements_by_class_name("status")


    citiesLength = len(cities)
    print('cities:', citiesLength)
    vaxStatusLength = len(vaxStatus)
    print('status:', vaxStatusLength)
    emailText = 'CVS Appointments available at: \n'
    emailUpdates = []
    isTriggered = False
    if citiesLength == vaxStatusLength:
        print('same number of statuses as cities - continue to check')
    else:
        logFile.write('Number of cities do not match the number of statuses \n')
    for row in range(0, citiesLength):
        vaxStatText = vaxStatus[row].text
        cityText = cities[row].text
        if vaxStatText != 'Fully Booked':
            emailUpdates.push('\t {} -- {} \n'.format(cityText, vaxStatText))
        logFile.write('\t {} -- {} \n'.format(cityText, vaxStatText))

    if isTriggered: 
        for update in emailUpdates:
            emailText += update
        emailer.emailer(emailText)
        logFile.write('\t Appointment found! \n {} \n'.format(emailText))

except Exception as e:
    logFile.write('Error: {} - {}\n'.format(e, datetime.datetime.now()))
finally:
    driver.quit()
    logFile.write('Close File: {} \n'.format(datetime.datetime.now()))
    logFile.close()
