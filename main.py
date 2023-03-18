from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from resumegenerator import Controller, ScrapyService

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))


scrapyService = ScrapyService(
    driver=driver, username="vraton", password=None
)

controller = Controller(scrapy=scrapyService, company=None)

controller.get_remote_experiences()
