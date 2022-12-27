from lib2to3.pgen2 import driver
from flask import Flask, redirect, render_template, request, url_for
import os
from pymongo import MongoClient
from dotenv import load_dotenv, find_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.chrome.options import Options
import yfinance as yf
from email.message import EmailMessage
import ssl
import smtplib
from lxml import etree

# Selenium Values Initializing
DRIVER_PATH = r"C:\Users\91939\Desktop\chromedriver.exe"


options = Options()
options.headless = True
driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)

# Database Values Initializing
load_dotenv(find_dotenv())
password = os.environ.get("MongoDB_PWd")
connection_string = f"mongodb+srv://DhruvAgarwal:{password}@computersciencewebsite.f7jhvvy.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)
app = Flask(__name__, template_folder='Templates')

# Automated Email Sending Values
email_sender = 'dhruvthedon12@gmail.com'
email_password = 'otsancuwyidshgoz'
email_reciever = 'dhruvagarwal2942@gmail.com'

subject = 'Target Price Reached'

em = EmailMessage()

em['From'] = email_sender
em['To'] = email_reciever
em['Subject'] = subject


# Database Values:
StockWebApp = client.StockApplicationSoftware
CollectionStockName = StockWebApp.StockNames
CollectionStockPrice = StockWebApp.StockPrices
CollectionTargetPrice = StockWebApp.StockTargetPrices
CollectionUserValues = StockWebApp.PortfolioValues

# Flask code for the Login Page

StockNames = []


@app.route('/', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if (request.form["Previous1"] == "formField1"):
            emailAddres = request.form["emailAddress"]
            print(emailAddres)
            password = request.form["pwd"]
            print(password)
    return render_template("login.html")


# Retrieving the Stock Names from Database, and storing them in
def StockNamesFunc():
    global StockNames
    stockNamesDatabase = CollectionStockName.find()
    for stocks in stockNamesDatabase:
        StockNames.append(stocks["Stock Name"])
    return StockNames


def TargetPriceFunc():
    TargetPrices = []
    stockNamesDatabase = CollectionStockName.find()
    for targetPrice in stockNamesDatabase:
        TargetPrices.append(targetPrice["Target Price"])
    return TargetPrices


# Function for automated email sending
Email_Sent = []


def emailSentFun():
    global Email_Sent
    StockNames = StockNamesFunc()
    for i in range(len(StockNames)):
        Email_Sent.append("False")


def SendingEmail(current):
    global Email_Sent
    TargetPrices = TargetPriceFunc()
    StockNames = StockNamesFunc()
    CurrentPrices = current
    for i in range(len(TargetPrices)):
        if (int(TargetPrices[i]) >= int(CurrentPrices[i])):
            if (Email_Sent[i] == "False"):
                body = f"{StockNames[i]} has reached the Target Price of {TargetPrices[i]}"
                em.set_content(body)
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                    smtp.login(email_sender, email_password)
                    smtp.sendmail(email_sender, email_reciever, em.as_string())
                Email_Sent[i] = "True"
            else:
                pass


# Functions for Sending/Retrieving Data from HTML Code
@app.route("/rel", methods=["GET", "POST"])
def get_data():
    PriceList = []
    StockNames = StockNamesFunc()
    for StockName in StockNames:
        stock_name = yf.Ticker(str(StockName)).info
        price = stock_name["regularMarketPrice"]
        PriceList.append(price)
    # SendingEmail(PriceList)
    return PriceList


@app.route("/names", methods=["GET", "POST"])
def get_names():
    StockNames = StockNamesFunc()
    return StockNames

# Primary Flask Function for the Home Page


StockNamesList = []
TargetPricesList = []


@app.route('/home', methods=["GET", "POST"])
def home():
    global StockNamesList
    global TargetPricesList
    if request.method == "POST":
        StockName = request.form.get("StockName")
        TargetPrice = request.form.get("TargetPrice")
        StockTBD = request.form.get("StockNameTBD")
        if (StockTBD is not None):
            CollectionStockName.delete_one({"Stock Name": StockTBD})
        elif ((StockName != "null") and (StockName is not None)):
            insertionList = {
                "Stock Name": StockName,
                "Target Price": TargetPrice
            }
            CollectionStockName.insert_one(insertionList)
        StockNamesList = StockNamesFunc()
        TargetPricesList = TargetPriceFunc()
    StockNamesList = StockNamesFunc()
    print(StockNames)
    TargetPrice = TargetPricesList
    return render_template("home.html", names=StockNamesList, TPrice=TargetPrice, length=len(StockNames))

# Function code for retrieving Stock Information


def StockInformation(StockTicker):
    StockInformationList = []
    driver.get(f"https://groww.in/stocks/{StockTicker}")
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    dom = etree.HTML(str(soup))

    StockPriceFullElement = soup.find(
        'div', class_='lpu38Pri valign-wrapper false fs28')
    StockPriceCodeUnfiltered = StockPriceFullElement.find_all(
        'span', class_="lpu38Pri fs28")
    FinalStockPrice = ""
    for char in StockPriceCodeUnfiltered:
        if len(str(char.text)) > 1 or str(char.text) == ".":
            FinalStockPrice += str(char.text[0])

    StockInformationList.append(FinalStockPrice)
    StockName = (dom.xpath(
        '//*[@id="root"]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div[2]/div[1]/h1')[0].text)
    StockInformationList.append(StockName)
    MarketCap = (dom.xpath(
        '//*[@id="stf545Stock"]/div[1]/table/tbody/tr[1]/td[2]')[0].text)
    StockInformationList.append(MarketCap)
    PriceToEarnings = (
        dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[3]/td[2]')[0].text)
    StockInformationList.append(PriceToEarnings)
    PriceToBook = (
        dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[5]/td[2]')[0].text)
    StockInformationList.append(PriceToBook)
    IndustryPToE = (
        dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[7]/td[2]')[0].text)
    StockInformationList.append(IndustryPToE)
    DebtToEquity = (
        dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[9]/td[2]')[0].text)
    StockInformationList.append(DebtToEquity)
    ROE = (
        dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[2]/td[2]')[0].text)
    StockInformationList.append(ROE)
    EPS = (
        dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[4]/td[2]')[0].text)
    StockInformationList.append(EPS)
    DividendYield = (
        dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[6]/td[2]')[0].text)
    StockInformationList.append(DividendYield)
    BookValue = (
        dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[8]/td[2]')[0].text)
    StockInformationList.append(BookValue)
    FaceValue = (
        dom.xpath('//*[@id="stf545Stock"]/div[1]/table/tbody/tr[10]/td[2]')[0].text)
    StockInformationList.append(FaceValue)
    Volume = (dom.xpath(
        '//*[@id="root"]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[4]/div[1]/section/section/div/div/div[4]/div/div[3]/span')[0].text)
    StockInformationList.append(Volume)
    Value = (dom.xpath(
        '//*[@id="root"]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[4]/div[1]/section/section/div/div/div[4]/div/div[4]/span')[0].text)
    StockInformationList.append(Value)
    OpenValue = (dom.xpath(
        '//*[@id="root"]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[4]/div[1]/section/section/div/div/div[4]/div/div[1]/span')[0].text)
    StockInformationList.append(OpenValue)
    PreviousClose = (dom.xpath(
        '//*[@id="root"]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[4]/div[1]/section/section/div/div/div[4]/div/div[2]/span')[0].text)
    StockInformationList.append(PreviousClose)
    StockDescription = (dom.xpath(
        '//*[@id="root"]/div/div[2]/div[1]/div/div/div[1]/div/div/div[2]/div/div/div[4]/div[6]/section/div/div[1]/div/div[2]/div/text()'))
    print(StockDescription)
    StockInformationList.append(StockDescription)
    return (StockInformationList)
    # Flask Code for Stock Search Page


StockInformationList = []


@app.route('/StockSearch', methods=["GET", "POST"])
def StockSearch():
    if request.method == "POST":
        global StockInformationList
        StockName = request.form.get("StockNames")
        StockInformationList = StockInformation(StockName)
    return render_template("StockSearch.html", StockInformation=StockInformationList)

# Retrieving user's input about stocks from the database


def portfolioStockInfoFun():
    PortStockNames = []
    # InitialPrice = []
    # Quantity = []
    portfolioStockNames = CollectionUserValues.find()
    for info in portfolioStockNames:
        PortStockNames.append(info["Stock Name"])
        # InitialPrice.append(info["Initial Price"])
        # Quantity.append(info["Quantity"])
    # print(PortStockNames)
    return PortStockNames


@app.route("/CurrentPrice", methods=["GET", "POST"])
def CurrentPrice():
    PriceList = []
    StockNames = portfolioStockInfoFun()
    for StockName in StockNames:
        stock_name = yf.Ticker(str(StockName)).info
        price = stock_name["regularMarketPrice"]
        PriceList.append(price)
        # print(price)
    return PriceList


@app.route("/StockNames", methods=["GET", "POST"])
def PortfolioNames():
    PortStockNames = portfolioStockInfoFun()
    return PortStockNames
# Flask Code for Portfolio Page


@app.route('/Portfolio', methods=["GET", "POST"])
def Portfolio():
    if request.method == "POST":
        Name = request.form["StockName"]
        InitialPrice = request.form["IPP"]
        quantity = request.form["Quantity"]
        InputValues = {
            "Stock Name": Name,
            "Initial Price": InitialPrice,
            "Quantity": quantity
        }
        CollectionUserValues.insert_one(InputValues)
    PortStockNames = portfolioStockInfoFun()
    return render_template("portfolio.html", names=PortStockNames, length=len(PortStockNames))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8090', debug=True)
