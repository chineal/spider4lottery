import time
import mysql
import re
from chrome import MyChrome

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


class Kj(MyChrome):
    _type: str = ""
    _index: int = 0
    _numbers: list = []
    _xpathDislog4btn: str = "//div[@id='popupContainerID']/div/div/a[2]"
    _xpathData4selector: str = ""

    _xpathData4balls: list = []
    _xpathData4money: list = []
    _xpathData4grand: list = []
    _xpathData4first: list = []

    __balls: list = []

    def __init__(self):
        super().__init__()
        self._type = self.__class__.__name__

    def check(self):
        if self._index >= len(self._numbers):
            return False
        recode: mysql.Recode = mysql.Recode.select(
            mysql.Recode.id
        ).where(
            mysql.Recode.type == self._type,
            mysql.Recode.key == self._key()
        ).order_by(
            mysql.Recode.id.desc()
        ).limit(1)
        if 0 == len(recode):
            return False
        self._index += 1
        return True

    def load(self): pass
    def _key(self): pass
    def _grand(self): return True

    def index(self):
        if 0 == len(self._sUrl):
            return
        if 0 == len(self._xpathData4selector):
            return
        self.get(self._sUrl)
        time.sleep(self._iLoad)
        items = self._browser.find_elements(By.XPATH, self._xpathData4selector)
        for item in items:
            self._numbers.append(item.get_attribute('href'))

    def info(self):
        balls: list = []
        for path in self._xpathData4balls:
            balls = self._browser.find_elements(By.XPATH, path)
            if 0 < len(balls):
                break
        if 0 == len(balls):
            self._index += 1
            return

        number: str = ""
        for ball in balls:
            number += ball.text
        money: str = self._find(self._xpathData4money)
        first: str = self._find(self._xpathData4first)
        grand: str = self._find(self._xpathData4grand) if self._grand() else None
        value = re.compile(r'^[0-9]+$')

        recode = mysql.Recode()
        recode.type = self._type  # 类别
        recode.key = self._key()  # 第几期
        recode.number = number  # 开奖号码
        recode.money = money  # 奖池滚存
        recode.grand = int(grand) if grand is not None and value.match(grand) else 0  # 特等奖
        recode.first = int(first) if first is not None and value.match(first) else 0  # 一等奖
        recode.save()

    def _find(self, xpath: list):
        for path in xpath:
            temp: WebElement = self.element(By.XPATH, path)
            if temp is not None:
                return temp.text
        return None

    def _dislog(self):
        self._log(0, "start", "check dislog")

        dislog: WebElement = self.element(By.XPATH, self._xpathDislog4btn)
        if dislog is not None:
            dislog.click()


class Zj6j1(Kj):
    _sUrl: str = "https://kaijiang.500.com/zj6j1.shtml"
    _index: int = 1

    # _xpathData4no: str = "/html/body/div[5]/div[3]/div[2]/div[1]/div[2]/table[1]/tbody/tr[1]/td/span[1]/a/font/strong"
    _xpathData4selector: str = "//select[@id='expectlist']/option"

    def __init__(self):
        super().__init__()
        self._xpathData4balls.append("/html/body/div[5]/div[3]/div[2]/div[1]/div[2]"
                                     "/table[1]/tbody/tr[2]/td/table/tbody/tr/td[2]/div/ul/li")
        self._xpathData4balls.append("/html/body/div[5]/div[4]/div[2]/div/div[2]"
                                     "/table[1]/tbody/tr[2]/td/table/tbody/tr/td[2]/div/ul/li")
        self._xpathData4balls.append("/html/body/table[1]/tbody/tr[2]/td/table/tbody/tr/td[2]/div/ul/li")

        self._xpathData4money.append("/html/body/div[5]/div[3]/div[2]/div[1]/div[2]/table[1]/tbody/tr[3]/td/span[2]")
        self._xpathData4money.append("/html/body/div[5]/div[4]/div[2]/div/div[2]/table[1]/tbody/tr[3]/td/span[2]")
        self._xpathData4money.append("/html/body/table[1]/tbody/tr[3]/td/span[2]")

        self._xpathData4grand.append("/html/body/div[5]/div[3]/div[2]/div[1]/div[2]/table[2]/tbody/tr[3]/td[2]")
        self._xpathData4grand.append("/html/body/div[5]/div[4]/div[2]/div/div[2]/table[2]/tbody/tr[3]/td[2]")
        self._xpathData4grand.append("/html/body/table[2]/tbody/tr[3]/td[2]")

        self._xpathData4first.append("/html/body/div[5]/div[3]/div[2]/div[1]/div[2]/table[2]/tbody/tr[4]/td[2]")
        self._xpathData4first.append("/html/body/div[5]/div[4]/div[2]/div/div[2]/table[2]/tbody/tr[4]/td[2]")
        self._xpathData4first.append("/html/body/table[2]/tbody/tr[4]/td[2]")

    def load(self):
        if self._index >= len(self._numbers):
            return False
        url: str = "https://kaijiang.500.com/shtml/zj6j1/%s.shtml" % self._numbers[self._index]
        self.get(url)
        return True

    def _key(self):
        return self._numbers[self._index]


class Ssq(Kj):
    _sUrl: str = "https://kaijiang.500.com/ssq.shtml"
    _index: int = 0

    _xpathData4selector: str = "/html/body/div[6]/div[3]/div[2]/div[1]/div[1]/div[3]/span/div/a"
    # _xpathData4key: str = "/html/body/div[6]/div[3]/div[2]/div[1]/div[2]" \
    #                       "/table[1]/tbody/tr[1]/td/span[1]/a/font/strong"
    _xpathData4name: str = "/html/body/div[6]/div[3]/div[2]/div[1]/div[2]/table[3]/tbody/tr[4]/td[1]"

    def __init__(self):
        super().__init__()
        self._xpathData4balls.append("/html/body/div[6]/div[3]/div[2]/div[1]/div[2]"
                                     "/table[1]/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/div/ul/li")
        self._xpathData4money.append("/html/body/div[6]/div[3]/div[2]/div[1]/div[2]/table[1]/tbody/tr[3]/td/span[2]")
        self._xpathData4grand.append("/html/body/div[6]/div[3]/div[2]/div[1]/div[2]/table[3]/tbody/tr[4]/td[2]")
        self._xpathData4first.append("/html/body/div[6]/div[3]/div[2]/div[1]/div[2]/table[2]/tbody/tr[3]/td[2]")
        self._xpathData4first.append("/html/body/div[6]/div[3]/div[2]/div[1]/div[2]/table[3]/tbody/tr[3]/td[2]")

    def load(self):
        if self._index >= len(self._numbers):
            return False
        url: str = self._numbers[self._index]
        self.get(url)
        return True

    def _key(self):
        # return self._browser.find_element(By.XPATH, self._xpathData4key).text
        url: str = self._numbers[self._index]
        paths: list = url.split("/")
        file: str = paths[-1]
        names: list = file.split(".")
        return names[0]

    def _grand(self):
        name: WebElement = self.element(By.XPATH, self._xpathData4name)
        if name is not None and "一等奖特别奖" == name.text:
            return True
        return False


class Kl8(Kj):
    _sUrl: str = "https://kaijiang.500.com/kl8.shtml"
    _index: int = 0

    _xpathData4selector: str = "/html/body/div[6]/div[3]/div[2]/div[1]/div[1]/div[3]/span/div/a"

    def __init__(self):
        super().__init__()
        self._xpathData4balls.append("/html/body/div[6]/div[3]/div[2]/div[1]/div[2]"
                                     "/table/tbody/tr[2]/td/table/tbody/tr/td[2]/div/ul/li")
        self._xpathData4money.append("/html/body/div[6]/div[3]/div[2]/div[1]/div[2]/table/tbody/tr[3]/td/span[2]")
        self._xpathData4first.append("/html/body/div[6]/div[3]/div[2]/div[1]/div[2]/div[3]/table/tbody/tr[3]/td[3]")

    def load(self):
        if self._index >= len(self._numbers):
            return False
        url: str = self._numbers[self._index]
        self.get(url)
        return True

    def _key(self):
        url: str = self._numbers[self._index]
        paths: list = url.split("/")
        file: str = paths[-1]
        names: list = file.split(".")
        return names[0]
