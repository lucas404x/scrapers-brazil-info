from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

import json

class Address:
    def __init__(self, cep, street, neighborhood, city, state):
        self.cep = cep
        self.street = street
        self.neighborhood = neighborhood
        self.city = city
        self.state = state
        
    def __eq__(self, other):
        return self.cep==other.cep
    
    def __hash__(self):
        return hash(('cep', self.cep))

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://geradornv.com.br/gerador-cep/")
btn = driver.find_element_by_id("nv-new-generator-copy-cep")
state_select = Select(driver.find_element_by_id("nv-state-cep"))
states = ("AC", "AL", "AM",
         "AP", "BA", "CE",
         "DF", "ES", "GO",
         "MA", "MG", "MS",
         "MT", "PA", "PB",
         "PE", "PI", "PR",
         "RJ", "RN", "RO",
         "RR", "RS", "SC",
         "SE", "SP", "TO")

addresses_quantity = []

with open("addresses.json", mode="w", encoding="utf-8") as fp:
    fp.write("[")

    for state in states:
        print(state)
        addresses = []
        state_select.select_by_value(state)
        for i in range(5000):
            btn.click()
            cep = driver.find_element_by_id("nv-field-cep").get_attribute("value")
            street = driver.find_element_by_id("nv-field-street").get_attribute("value")
            neighborhood = driver.find_element_by_id("nv-field-neighborhood").get_attribute("value")
            city = driver.find_element_by_id("nv-field-city").get_attribute("value")
            addresses.append(Address(cep, street, neighborhood, city, state))
        addresses = set(addresses)
        addresses_quantity.append(len(addresses))
        for address in addresses:
            fp.write(json.dumps(address.__dict__, ensure_ascii=False))
            fp.write(",")
        
    fp.write("]")
driver.close()

print(addresses_quantity)

