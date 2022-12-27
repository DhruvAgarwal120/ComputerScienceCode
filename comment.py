from selenium import webdriver
from bs4 import BeautifulSoup
import time
import requests
from lxml import etree
from selenium.webdriver.chrome.options import Options

DRIVER_PATH = r"C:\Users\91939\Desktop\chromedriver.exe"


options = Options()
options.headless = True
driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)

driver.get("https://groww.in/stocks/reliance-industries-ltd")
time.sleep(5)

soup = BeautifulSoup(driver.page_source, "html.parser")

dom = etree.HTML(str(soup))

# Code for Stock Price
# StockPriceFullElement = soup.find(
#     'div', class_='lpu38Pri valign-wrapper false fs28')

# StockPriceCodeUnfiltered = StockPriceFullElement.find_all(
#     'span', class_="lpu38Pri fs28")
# firstCharacterList = ""
# for char in StockPriceCodeUnfiltered:
#     if len(str(char.text)) > 1 or str(char.text) == ".":
#         firstCharacterList += str(char.text[0])
# print(firstCharacterList)

# Basic Description for the Stock

# StockDescription = dom.xpath(
#     '//*[@id="root"]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[4]/div[6]/section/div/div[1]/div/div[2]/div/text()')

# Fundamental Information of the Stock

# MarketCap = (dom.xpath(
#     '//*[@id="stf545Stock"]/div[1]/table/tbody/tr[1]/td[2]')[0].text)

# PriceToEarnings = (
#     dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[3]/td[2]')[0].text)

# PriceToBook = (
#     dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[5]/td[2]')[0].text)
# #
# IndustryPToE = (
#     dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[7]/td[2]')[0].text)

# DebtToEquity = (
#     dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[9]/td[2]')[0].text)

# ROE = (
#     dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[2]/td[2]')[0].text)

# EPS = (
#     dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[4]/td[2]')[0].text)

# DividendYield = (
#     dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[6]/td[2]')[0].text)

# BookValue = (
#     dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[8]/td[2]')[0].text)

# FaceValue = (
#     dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[10]/td[2]')[0].text)

# Volume = (dom.xpath(
#     '//*[@id="root"]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[4]/div[1]/section/section/div/div/div[4]/div/div[3]/span')[0].text)

# Value = (dom.xpath(
#     '//*[@id="root"]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[4]/div[1]/section/section/div/div/div[4]/div/div[4]/span')[0].text)
