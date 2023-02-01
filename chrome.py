import time

from mylog import Mylog
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait


class MyChrome(Mylog):
    _browser: webdriver
    _iStep: int = 1
    _iLoad: int = 5
    _iInput: int = 10
    _sUrl: str = ""

    def __init__(self):
        self._browser = None

    def storage(self, chromes: dict, key: str): pass
    def login(self, path: str, account: str, password: str): pass

    def create_browser(self, path: str, image: bool):
        if self._browser is not None:
            return

        option = ChromeOptions()
        option.page_load_strategy = 'none'  # get不阻塞
        '''''
        option.add_experimental_option("debuggerAddress", "127.0.0.1:9988")
        '''
        option.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        option.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        # 隐藏window.navigator.webdriver，禁用启用Blink运行时的功能
        option.add_argument('--disable-blink-features=AutomationControlled')
        option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        option.add_argument('--window-size=1440,900')  # 专门应对无头浏览器中不能最大化屏幕的方案
        option.add_argument('--disable-dev-shm-usage')
        option.add_argument('--user-agent=Mozilla/5.0'
                            ' (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                            ' (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36')
        if image is False:
            option.add_argument("blink-settings=imagesEnabled=true")  # 不加载图片, 提升速度
        # option.add_argument("--hide-scrollbars")  # 隐藏滚动条, 应对一些特殊页面
        # option.add_argument('log-level=3')

        option.add_experimental_option('excludeSwitches', ['enable-automation'])  # 设置为开发者模式，防止网站识别
        option.add_experimental_option('useAutomationExtension', False)
        # prefs = {
        #     'profile.default_content_setting_values': {
        #         'images': 2,
        #     }
        # }
        # option.add_experimental_option('prefs', prefs)
        # option.add_experimental_option("detach", True)  # 分离

        # option.add_extension("/Users/ix/Open_Link_in_Same_Tab_1.14.crx")  # 加载插件
        '''  # '''
        self._browser = webdriver.Chrome(executable_path=path, options=option)
        #self._browser.set_page_load_timeout(5)
        self._browser.maximize_window()

    def get_browser(self):
        return self._browser

    def set_browser(self, browser: webdriver):
        self._browser = browser

    def get(self, url):  # 打开网址
        self._log(1, "start", url)
        self._browser.get(url)
        WebDriverWait(self._browser, 5, 5).until(lambda diver:True)

    def close(self):
        self._log(0, "start", "close browser")
        if self._browser is None:
            self._log(0, "pass", "close browser")
            return
        self._browser.close()
        self._browser = None

    def element(self, by: str, value: str):
        try:
            return self._browser.find_element(by, value)
        except Exception as msg:
            self._err(0, msg)
        return None

    def _value(self, by: str, path: str, value):
        we: WebElement = self._browser.find_element(by, path)
        tester: str = we.get_attribute('value')
        if 0 < len(tester):
            if tester == str(value):
                return we
            self._browser.execute_script("arguments[0].value=''", we)
            time.sleep(self._iStep)
        we.send_keys(value)
        return we

    def _tabs(self):  # 切换到最新打开的窗口
        self._log(0, "start", "switch window")
        tabs = self._browser.window_handles
        if tabs is None:
            self._log(0, "passed", "switch window")
            return
        count: int = 0
        for tab in tabs:
            self._browser.switch_to.window(tab)
            count += 1
            if len(tabs) > count:
                self._browser.close()
        self._log(0, "switched", "to the last window({:d})".format(count))

    def _top(self):  # 滚动到页面顶部
        self._log(0, "start", "goto bottom of page")

        self._browser.execute_script("window.scrollTo(0,0)")  # 滑动到页面底部
        time.sleep(self._iStep)
        self._log(0, "reach", "the bottom of page")

    def _bottom(self):  # 滚动到页面底部
        self._log(0, "start", "goto bottom of page")

        self._browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")  # 滑动到页面底部
        time.sleep(self._iStep)
        self._log(0, "reach", "the bottom of page")

    def _middle(self):  # 滚动到页面中间
        self._log(0, "start", "goto middle of page")

        self._browser.execute_script("window.scrollTo(0,document.body.scrollHeight*0.3)")  # 滑动到页面中间
        time.sleep(self._iStep)
        self._log(0, "reach", "the middle of page")

    def _middle2(self):  # 滚动到页面中间
        self._log(0, "start", "goto middle of page")

        self._browser.execute_script("window.scrollTo(0,document.body.scrollHeight*0.6)")  # 滑动到页面中间
        time.sleep(self._iStep)
        self._log(0, "reach", "the middle of page")

    def _click(self, btn: WebElement):
        ActionChains(self._browser).move_to_element(btn).perform()
        ActionChains(self._browser).click(btn).perform()

    def _down2enter(self, count: int):
        for i in range(count):
            ActionChains(self._browser).send_keys(Keys.DOWN).perform()
            time.sleep(0.1)
        ActionChains(self._browser).send_keys(Keys.ENTER).perform()

    def _select2key(self, by: str, path: str, key: str):
        items = self._browser.find_elements(by, path)
        for item in items:
            ActionChains(self._browser).send_keys(Keys.DOWN).perform()
            time.sleep(0.1)
            if (item.text in key) or (key in item.text):
                break
        ActionChains(self._browser).send_keys(Keys.ENTER).perform()

    @staticmethod
    def _money2price(money: str):
        wan = 0 <= money.find("万")
        money = money.replace("万", "")
        money = money.replace("元", "")
        money = money.replace("¥", "")
        money = money.replace(",", "")
        numbers = money.split(".")

        times: int = 1
        price: float = 0
        if len(numbers) > 0:
            price += int(numbers[0])
        if len(numbers) > 1:
            times = 10 ** len(numbers[1])
            price *= times
            price += int(numbers[1])
        if wan:
            price *= 10000
        if 1 < times:
            price /= times
        return price

    @staticmethod
    def _cut_url(url: str):
        if 0 < url.find("?"):
            url = url[0: url.index("?")]
        return url
