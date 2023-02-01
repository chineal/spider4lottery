from datetime import datetime


def log(shell: bool, file: bool, account: str, clazz: str, level: int, title: str, message: str):
    if shell:
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), f"{account}-{clazz} {title}:{message}")
    if file or 0 < level:
        with open(f"./logs/{account}_" + datetime.now().strftime("%Y-%m-%d") + ".log", "a+") as f:
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" {clazz}-{title}:{message}\r\n")


class Mylog:
    _iUserid: int = 0
    _sAccount: str = ""
    _bShellFlag: bool = False
    _bFileFlag: bool = False

    def get_flags(self):
        return self._sAccount, self._bShellFlag, self._bFileFlag

    def flags(self, shell: bool, file: bool, account: str, key: int = 0):
        self._bShellFlag = shell
        self._bFileFlag = file
        self._sAccount = account
        if 0 < key:
            self._iUserid = key

    def _err(self, level: int, msg: Exception): pass

    def _log(self, level: int, title: str, message: str):
        log(self._bShellFlag, self._bFileFlag, self._sAccount, self.__class__.__name__, level, title, message)

