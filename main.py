import os
import time
# import threading
import mysql
import zzz as setting

from kaijiang500 import Kj, Zj6j1, Ssq, Kl8


def run(kj: Kj):
    kj.flags(True, False, "test", 1)
    kj.create_browser(setting.g_sPath, True)
    kj.index()
    time.sleep(1)
    while True:
        if kj.check():
            continue
        if not kj.load():
            break
        time.sleep(3)
        kj.info()


if __name__ == "__main__":
    if not os.path.exists("./logs"):
        os.mkdir("./logs")
    os.environ["webdriver.chrome.driver"] = setting.g_sPath
    mysql.init()
    #run(Zj6j1())
    #run(Ssq())
    run(Kl8())

