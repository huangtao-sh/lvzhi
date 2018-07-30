# 项目：运营主管履职报告
# 模块：数据库模型
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-07-29 19:17

from orange.sqlite import db_config, begin_tran, begin_query, execute, executemany, executescript, find, findone

drop_sql = '''


'''

create_sql = '''
create table if not exists fhreport(
    id text primary key,
    period text,
    type text,
    branch text,
    name text,
    date text,
    content text,
    update_time int
);
'''
