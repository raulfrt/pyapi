
# -*- coding: utf-8 -*-

import json
import requests
from flask import jsonify
from time import sleep
from flask import jsonify
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver


class ScrapingDisco:
    def __init__(self, server_name="http://selenium:4444"):
        self.server_name = server_name
        self.executor_url = "{}/wd/hub".format(server_name)
        self.scrap_url = "https://www.disco.com.ar/electro/informatica"
        self.first_page = 0
        self.get_driver_session()

    def get_driver_session(self):
        # Start browser maximized and disable extensions
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-extensions")

        session_id = self.get_session_active()
        if not session_id:
            new_driver = webdriver.Remote(
                command_executor=self.executor_url, options=options
            )
            return new_driver

        driver_version = self.get_driver_version()

        # Save the original function, so we can revert our patch
        org_command_execute = RemoteWebDriver.execute

        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {"success": 0, "value": None, "sessionId": session_id,
                        "version": driver_version}
            else:
                return org_command_execute(self, command, params)

        # Patch the function before creating the driver object
        RemoteWebDriver.execute = new_command_execute

        new_driver = webdriver.Remote(
            command_executor=self.executor_url, options=options
        )
        new_driver.session_id = session_id

        # Replace the patched function with original function
        RemoteWebDriver.execute = org_command_execute

        return new_driver

    def clear_sessions(self, session_id=None):
        """
        Here we query and delete orphan sessions
        docs: https://www.selenium.dev/documentation/grid/advanced_features/endpoints/
        :return: None
        """
        url = self.server_name
        if not session_id:
            # delete all sessions
            r = requests.get("{}/status".format(url))
            data = json.loads(r.text)
            for node in data["value"]["nodes"]:
                for slot in node["slots"]:
                    if slot["session"]:
                        id = slot["session"]["sessionId"]
                        r = requests.delete("{}/session/{}".format(url, id))
        else:
            # delete session from params
            r = requests.delete("{}/session/{}".format(url, session_id))

    def get_session_active(self):
        """
        Here we query and delete orphan sessions
        docs: https://www.selenium.dev/documentation/grid/advanced_features/endpoints/
        :return: None
        """
        url = self.server_name
        r = requests.get("{}/status".format(url))
        data = json.loads(r.text)
        nodes = data["value"]["nodes"]
        if nodes:
            slots = nodes[0]["slots"]
            if slots:
                session = slots[0]["session"]
                if session:
                    return session.get("sessionId", False)
        return False

    def get_driver_version(self):
        url = self.server_name
        r = requests.get("{}/status".format(url))
        data = json.loads(r.text)
        nodes = data["value"]["nodes"]
        if nodes:
            slots = nodes[0]["slots"]
            if slots:
                session = slots[0]["session"]
                if session:
                    capabilities = session.get("capabilities", {})
                    chrome = capabilities.get("chrome", {})
                    return chrome.get("chromedriverVersion", False)
        return False

    def scraping(self, first_page=0):
        driver = self.get_driver_session()
        driver.get(self.scrap_url)
        btn_next_class = (
            "vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2"
            " min-h-small t-action--small bg-action-primary b--action-primary"
            " c-on-action-primary hover-bg-action-primary"
            " hover-b--action-primary hover-c-on-action-primary pointer"
        )
        btn_sl_next = "button." + btn_next_class.replace(" ", ".")

        class_btn_dis = (
            "vtex-button bw1 ba fw5 v-mid relative pa0 lh-solid br2"
            " min-h-small t-action--small bg-disabled b--muted-5 c-on-disabled"
        )
        btn_sl_dis = "button." + class_btn_dis.replace(" ", ".")
        btn_sl_register = "button.align-right.secondary.slidedown-button"

        try:
            btn_register = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, btn_sl_register))
            )
            btn_register.click()
        except Exception:
            pass

        while True:
            if first_page:
                break
            try:
                WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element((By.CSS_SELECTOR, btn_sl_dis))
                )
                btn_next = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, btn_sl_next))
                )
                driver.find_element(By.CSS_SELECTOR, "body").send_keys(
                    Keys.CONTROL + Keys.HOME
                )
                sleep(2)
                ActionChains(driver).move_to_element(btn_next).perform()
                sleep(3)
                btn_next.click()
            except Exception:
                break
        if not first_page:
            try:
                btn_progress = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            "//div[@class='progress' and @style='width: 100%;']",
                        )
                    )
                )
                ActionChains(driver).move_to_element(btn_progress).perform()
            except Exception:
                pass
            
        content = driver.page_source
        # driver.quit()
        soup = BeautifulSoup(content, features="html.parser")
        articles = soup.find_all(
            "article",
            class_=(
                "vtex-product-summary-2-x-element pointer pt3 pb4"
                " flex flex-column h-100"
            ),
        )
        records = []
        for article in articles:
            try:
                mark = article.find(
                    "span", class_="vtex-product-summary-2-x-productBrandName"
                ).get_text()
                description = article.find(
                    "span",
                    class_=(
                        "vtex-product-summary-2-x-productBrand"
                        " vtex-product-summary-2-x-brandName t-body"
                    ),
                ).get_text()
                price = article.select("div.contenedor-precio span")[
                    0
                ].get_text()
                records.append(
                    {"marca": mark, "descripcion": description, "precio": price}
                )
            except Exception:
                pass

        # response = json.dumps({"records": records})
        # print(response)
        response = jsonify({"records": records})
        response.status_code = 202
        return response
