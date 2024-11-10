from requests import ConnectionError, get
from faker import Faker
from bs4 import BeautifulSoup
from abc import ABC

class HtmlPageABC(ABC):
    def __init__(self, url: str) -> None:
        ...
    
    def _get_web_page(self, url: str) -> list[int, str, str]:
        ...
    
    def _valedate_url(self, url: str) -> str:
        ...
        
    def _get_urls_source(self) -> list[str]:
        ...
    
    def _get_obj_page(self, url: str) -> list[int, str, str]:
        ...
        
    def _replase_url_to_path_local_file(self, url: str, name: str) -> None:
        ...
    
    def preparing_web_page_layout(self) -> None:
        ...
        
    def dump(self, dir) -> None:
        ...
        
class HtmlPageGetSource(HtmlPageABC):
    def __init__(self, url:str) -> None:
        self.main_url = url
        _url = self.main_url.split("/")
        self.protocol = _url[0][:-1] # http or https 
        self.domen = _url[2]    # example habr.ru
        self.bodyLink = "/".join(_url[3:])
        self.faker = Faker()
        del _url
    
    def _get_web_page(self, url: str) -> list[int, str]:
        try:
            fake = Faker()
            response = get(
                self.protocol + "://" + self.domen + "/" + self.bodyLink,
                headers={"User-Agent": self.faker.user_agent(),
                        "Accept": "*/*",
                        "Accept-Language": "en-US"}
                )
            return [response.status_code, response.text]
        except:
            if ConnectionError:
                print("Error connect to server")
                exit()
                
    def preparing_web_page_layout(self):
        status, html = self._get_web_page(self.main_url)
        if status != 200:
            print(f"Erorr status: {status}")
            exit()
        else:
            self.bsPageObj = BeautifulSoup(html, "lxml")
            self.strPageText = html
        
class HtmlPageLinkPreparing(HtmlPageGetSource):
    def _valedate_url(self, url: str) -> str:
        if "/" == url[0]:
            url = self.protocol + "://" + self.domen + "/" + url
        elif "http" != url[0:4]:
            url = self.protocol + "://" + self.domen + "/".join(self.bodyLink.split('/')[:-1]) + "/" + url
        return url
    
    def _get_name_for_url(self, url:str, type=None) -> str:
        name_file = url.split("/")[-1]
        if name_file == "" or "." not in name_file:
            name_file =  "object_" + str(self.count) + "." + type
        name_file = name_file.split("?")[0]
        name_file = name_file.split("@")[0]
        name_file = name_file.split(";")[0]
        name_file = name_file.split("+")[0]
        return name_file
         
    def _get_urls_source(self) -> list[str]:
        html_source_tags = {
            "src": ["img", "script", "audio", "video", "ifname", "embed"],
            "href": ["link"],
            "data-href": ["link"],
            "data": ["object"]
            }
        key_html_source_tags = list(html_source_tags)
        urls = [] 
        for args_tag in key_html_source_tags:
            for tag in html_source_tags[args_tag]:
                for element in self.bsPageObj.find_all(tag):
                    if element.attrs.get(args_tag, None):
                        urls.append(element[args_tag])
        return urls

class DumpHtmlPage(HtmlPageLinkPreparing):
    def __init__(self, url: str) -> None:
        self.count = 0
        super().__init__(url)
        
    def _replase_url_to_path_local_file(self, url: str, name: str) -> None:
        print(url, " ", name)
        self.strPageText = self.strPageText.replace(url, name)
    
    def _get_obj_page(self, url: str) -> list[int, str, str]:
        fake = Faker()
        url = self._valedate_url(url)
        response = get(
                    url,
                    headers={"User-Agent": self.faker.user_agent(),
                             "Accept": "*/*",
                             "Accept-Language": "en-US"}
                        )
        return response.status_code, response.content, response.headers["Content-Type"].split("/")[-1]
    
    def dump(self, dir) -> None:
        for url in self._get_urls_source():
            status, content, type = self._get_obj_page(url)
            name_file = self._get_name_for_url(url, type)
            self._replase_url_to_path_local_file(url, name_file)
            with open(f"{dir}/{name_file}", "wb") as file:
                file.write(content)
        with open(f"{dir}/index.html", "w") as file:
            file.write(self.strPageText)
