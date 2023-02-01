from peewee import *

import zzz as setting
from playhouse.pool import PooledMySQLDatabase

g_db = PooledMySQLDatabase(setting.g_sBase, **setting.g_dDB)
g_bInit: bool = False


def init():
    try:
        if not g_db.table_exists(Recode):
            g_db.create_tables([Recode])
    except Exception as msg:
        print("error", msg)
        return False

    global g_bInit
    g_bInit = True
    return True


class BaseModel(Model):
    class Meta:
        database = g_db


class Recode(BaseModel):
    id = PrimaryKeyField()
    type = CharField(verbose_name="类别", max_length=8, null=False)
    key = CharField(verbose_name="第几期", max_length=8, null=False)
    number = CharField(verbose_name="开奖号码", max_length=64, null=False)
    money = CharField(verbose_name="奖池滚存", max_length=16, null=False)
    grand = SmallIntegerField(verbose_name="特等奖", null=False, default=0)
    first = SmallIntegerField(verbose_name="一等奖", null=False, default=0)
