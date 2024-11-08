from requests import get
from faker import Faker
from bs4 import BeautifulSoup
from typing import Union
import os
class WebPage:
    def __init__(self, url: str) -> None:
        _url = url.split("/")
        self.protocol = _url[0][:-1] # http or https 
        self.domen = _url[2]    # example habr.ru
        self.bodyLink = "/".join(_url[3:])
        self.faker = Faker()
        del _url
        
    def __get_web_page(self) -> Union[int, str]:
        fake = Faker()
        response = get(
            self.protocol + "://" + self.domen + "/" + self.bodyLink,
            headers={"User-Agent": self.faker.user_agent(),
                     "Accept": "*/*",
                     "Accept-Language": "en-US"}
            )
        return response.status_code, response.text
    
    def __validate_url(self, url: str) -> str:
        if "h" != url[0]:
            return self.protocol + "://" + self.domen + url
        else:
            return url
    
    def __get_obj_web_page(self, url: str) -> Union[int, str, dict]:
        url = self.__validate_url(url)
        response = get(url, 
                             headers={"User-Agent": self.faker.user_agent(),
                             "Accept": "*/*",
                             "Accept-Language": "en-US"}
                            )
        return response.status_code, response.content, response.headers
    def __get_all_head_link(self, bsObject: BeautifulSoup) -> Union[str, str]:
        return [obj["href"] for obj in bsObject.head.find_all("link")]
    
    def __get_all_body_img(self, bsObject: BeautifulSoup) -> Union[str, str]:
        return [obj["src"] for obj in bsObject.body.find_all("img")]
    
    def preparing_web_page_layout(self):
        status, html = self.__get_web_page()
        if status != 200:
            print(f"Erorr status: {status}")
            exit()
        else:
            self.bsPageObj = BeautifulSoup(html, "lxml")
            self.strPageText = html
    
    def dump(self, dir: str):
        coutn_obj = 0
        
        for url in self.__get_all_head_link(self.bsPageObj):
            status, content, headers = self.__get_obj_web_page(url if url[0] == "/" else self.protocol + "://" + self.domen + "/" + "/".join(self.bodyLink.split("/")[:-1]) + "/" + url)
            nameFile = url.split("/")[-1]
            if not nameFile:
                nameFile = f"{coutn_obj}{object}.{headers['Content-Type'].split('/')[-1]}"
                coutn_obj += 1
            self.strPageText = self.strPageText.replace(url, f"{dir.rstrip('/')}/{nameFile}")
            with open(f"{dir.rstrip('/')}/{nameFile}", "wb") as file:
                file.write(content)
        
        for url in self.__get_all_body_img(self.bsPageObj):
            status, content, headers = self.__get_obj_web_page(url if url[0] == "/" else self.protocol + "://" + self.domen + "/" + "/".join(self.bodyLink.split("/")[:-1]) + "/" + url)
            nameFile = url.split("/")[-1]
            if not nameFile:
                nameFile = f"{coutn_obj}{object}.{headers['Content-Type'].split('/')[-1]}"
                coutn_obj += 1
            self.strPageText = self.strPageText.replace(url, f"{dir.rstrip('/')}/{nameFile}")
            with open(f"{dir.rstrip('/')}/{nameFile}", "wb") as file:
                file.write(content)
        
        with open("index.html", "w") as file:
            file.write(self.strPageText)
