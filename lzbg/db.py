# 项目：履职报告上报情况分析
# 模块：分析模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018/07/20

from orange import Path
path = Path('D:/履职报告')

delete_sql = '''
drop table if exists report;
drop table if exists branch;
'''

create_sql = '''
create table if not exists report(
    title text primary key,
    bgr text,
    jg text,
    bgrq text,
    cs text,
    fj text,
    yxqk text,
    sbmc text,
    ycnr text,
    spyj text,
    fhjj text,
    zhjj text,
    shryj text,
    fzryj text,
    nr text
);
create table if not exists branch
(
    br text unique,
    name text
);
'''


def init(db, force=False):
    if not path:
        path.ensure()
        print('创建目录：%s' % path)
    script = create_sql
    if force:
        script = delete_sql+script
    db.executescript(script)
