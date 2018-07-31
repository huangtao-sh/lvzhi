# 项目：履职报告上报情况分析
# 模块：分析模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018/07/20
# 修订：2018/07/29 调整数据表结构中的字段名称，增加 period 字段

from orange.sqlite import executescript

delete_sql = '''
drop table if exists report;
drop table if exists branch;
'''

create_sql = '''
create table if not exists report(
    title text primary key,
    period text,
    name text,
    br text,
    date text,
    cc text,
    attachment text,
    yxqk text,
    sbmc text,
    ycnr text,
    spyj text,
    fhjj text,
    zhjj text,
    shryj text,
    fzryj text,
    content text
);
create table if not exists branch
(
    br text unique,
    name text
);
'''


def init(force=False):
    script = create_sql
    if force:
        script = delete_sql+script
    executescript(script)
