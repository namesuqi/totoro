# coding=utf-8
"""
通过ORM库操作mysql数据库

把表的映射定义都放在本文件
将表的操作放到具体业务库中

__author__ = 'zengyuetian'

reference: http://docs.sqlalchemy.org/en/latest/orm/tutorial.html

"""

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from libs.const.database import *

# describing the database tables we’ll be dealing with,
# and then by defining our own classes which will be mapped to those tables.
Base = declarative_base()

DB_CONNECT_STRING = 'mysql+mysqldb://{0}:{1}@{2}:{3}/{4}'.\
    format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_BOSS)


class Roles(Base):
    __tablename__ = "ppc_roles"
    id = Column(Integer, primary_key=True)
    tenant_id = Column(Integer)
    name = Column(String)

    def __init__(self, tenant_id, name):
        self.tenant_id = tenant_id
        self.name = name


class MysqlORM(object):
    def __init__(self):
        self.engine = create_engine(DB_CONNECT_STRING, echo=True)
        self.DBSession = sessionmaker(bind=self.engine)
        self.session = self.DBSession()

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)


if __name__ == "__main__":
    role = Roles(tenant_id=100000042, name='autotester')
    orm = MysqlORM()

    # 增加1条记录
    orm.session.add(role)
    orm.session.commit()

    # 查询
    my_role = orm.session.query(Roles).filter(Roles.tenant_id == 100000042).all()
    print type(my_role)
    for role in my_role:
        print role.id, role.name

    # 修改
    orm.session.query(Roles).filter(Roles.tenant_id == 100000042).update({"name": "auto"})
    my_role = orm.session.query(Roles).filter(Roles.tenant_id == 100000042).all()
    print type(my_role)
    for role in my_role:
        print role.id, role.name

    # 删除
    orm.session.query(Roles).filter(Roles.tenant_id == 100000042).delete()
    orm.session.commit()

    my_role = orm.session.query(Roles).filter(Roles.tenant_id == 100000042).all()
    print type(my_role)
    for role in my_role:
        print role.id

    orm.session.close()
