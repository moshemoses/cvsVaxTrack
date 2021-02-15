from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only

#headless option
#chrome_options.add_argument("--headless")


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

if citiesLength == vaxStatusLength:
    print('same number of statuses as cities - continue to check')
else:
    print('Number of cities do not match the number of statuses')
for row in range(0, citiesLength):
    print(cities[row].text + '--' + vaxStatus[row].text)

driver.quit()
