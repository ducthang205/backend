# importing necessary packages
import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from db import models
from db.database import conn
from db.models import records

from sqlalchemy.orm import Session
from fastapi import Depends, FastAPI, HTTPException


def get_data():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver.minimize_window()
    user = "supergalaxy205@gmail.com"
    _pass = "123456"
    url = "https://finance.vietstock.vn/CTI/thong-ke-giao-dich.htm"
    driver.get(url)
    button = driver.find_element(By.XPATH, "/html/body/div[2]/div[6]/div/div[2]/div[2]/a[3]")
    driver.execute_script("arguments[0].click();", button)
    username = driver.find_element(By.XPATH, "//*[@id=\"txtEmailLogin\"]")
    username.clear()
    username.send_keys(user)
    password = driver.find_element(By.XPATH, "//*[@id=\"txtPassword\"]")
    password.clear()
    password.send_keys(_pass)
    button = driver.find_element(By.XPATH, "//*[@id=\"btnLoginAccount\"]")
    driver.execute_script("arguments[0].click();", button)
    button = driver.find_element(By.XPATH, "//*[@id=\"view-tab\"]/li[2]/a")
    driver.execute_script("arguments[0].click();", button)
    sleep(8)
    data = []
    for a in range(1):

        j = 0
        while 1 == 1:
            for i in range(15):
                try:

                    id = i + j * 15

                    time = driver.find_element(By.XPATH,
                                               "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                                   i + 1) + "]/td[1]")

                    price = driver.find_element(By.XPATH,
                                                "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                                    i + 1) + "]/td[2]/span/span[1]")

                    change = driver.find_element(By.XPATH,
                                                 "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                                     i + 1) + "]/td[2]/span/span[2]")

                    per = driver.find_element(By.XPATH,
                                              "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                                  i + 1) + "]/td[2]/span/span[4]")

                    vol = driver.find_element(By.XPATH,
                                              "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                                  i + 1) + "]/td[3]")

                    totalVol = driver.find_element(By.XPATH,
                                                   "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                                       i + 1) + "]/td[3]")

                    density = driver.find_element(By.XPATH,
                                                  "//*[@id=\"deal-content\"]/div/div/div[2]/div/table/tbody/tr[" + str(
                                                      i + 1) + "]/td[4]")

                    value = {"id": 0, "time": time.text, "price": price.text, "change": change.text, "per": per.text,
                             "vol": vol.text,
                             "totalVol": totalVol.text, "density": density.text}
                    print(value)

                    result = conn.execute(records.insert().values(value))
                    data.append(value)
                    i = i + 1
                except:

                    break
            j = j + 1
            button = driver.find_element(By.XPATH, "//*[@id=\"btn-page-next\"]")
            driver.execute_script("arguments[0].click();", button)
        print(data)
    return data



