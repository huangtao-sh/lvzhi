# 项目：履职报告上报情况分析
# 模块：分析模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018/07/20
# 修订：2018/07/29 程序调整

from orange import Path, R, arg, cstr, datetime, now
from .db import path, init
from collections import defaultdict
from .sqlite import begin_tran, db_config
import json


def _get_period(date: str)->str:
    date = datetime(date).add(days=-25)
    return date % ('%Y-%m')


def fetch_period(db)-> str:
    sql = 'select period from report order by date desc limit 1'
    d = db.execute(sql).fetchone()
    if not d:
        raise Exception('无数据记录')
    return d[0]


def load_file(db):
    files = path.glob('会计履职报告*.xls')
    if not files:
        print('当前目录无文件')
    else:
        filename = max(files)
        print('当前导入文件：%s' % (filename))
        data = []
        for rows in filename.iter_sheets():
            rows = rows[-1]
            if len(rows) < 1:
                continue
            title = None
            for row in rows[1:]:
                if row[0]:
                    if title != row[0]:
                        title = row[0]
                        nr = [row[18:]]
                        data.append([title, _get_period(row[5]), row[2], row[4]+row[3], row[5],
                                     row[6], row[7], row[8], row[10], row[11], row[12], row[13], row[14],
                                     row[16], row[17], nr])
                    else:
                        nr.append(row[18:])
        data2 = []
        for r in data:
            r[-1] = json.dumps(r[-1])
            data2.append((r[3], r[2]))

    sql = f'insert or ignore into report values({",".join(["?"]*16)})'
    db.executemany(sql, data)
    sql = 'insert or ignore into branch values(?,?)'
    db.executemany(sql, data2)
    print('已处理数据：%d' % (len(data)))


def do_report(db):
    period = fetch_period(db)
    print('当前期次：%s' % (period))

    db.execute(
        'select count(br) as count from report where period=?', [period])
    d = db.fetchone()
    if d:
        print(f'报告数量：{d[0]}')
    print('报送数据错误清单')
    print('-'*30)
    sql = '''select br,count(name) as count,group_concat(name)as names
    from report where period= ?
    group by br
    having count>1 order by br'''
    db.execute(sql, [period])
    for no, (jg, count, names) in enumerate(db, 1):
        print(no, cstr(jg, 30), names, sep='\t')
    print(f'共计：{no}')
    print('\n未报送机构清单')
    print('-'*30)
    sql = '''select rowid,br,name from branch 
    where br not in (select br from report where period=?) 
    and name not in (select name from report where period=?)
    order by br'''
    no = 0
    db.execute(sql, [period, period])
    for no, (rowid, br, name) in enumerate(db, 1):
        print(no, cstr("%03d-%s" % (rowid, br), 35), name, sep='\t')
    print(f'共计：{no}')


@arg('-i', '--init', dest='init_', action='store_true', help='初始化')
@arg('-l', '--loadfile', action='store_true', help='导入文件')
@arg('-d', '--delete', metavar='branch', dest='branchs', nargs='*', help='删除机构')
@arg('-r', '--report', action='store_true', help='报告上报情况')
@arg('-f', '--force', action='store_true', help='强制初始化')
@arg('-s', '--show', action='store_true', help='显示')
@arg('-w', '--wenti', action='store_true', help='收集问题')
@arg('-e', '--export', nargs="?", metavar='qici', default='NOSET', dest='export_qc', help='导出一览表')
def main(init_=False, loadfile=False, branchs=None, report=False, force=False, show=False,
         export_qc=None, wenti=False):
    db_config(str(path/'lzbg.db'))
    if init_:
        init(force=force)
    if wenti:
        from .report import export_wt
        export_wt()
    with begin_tran()as db:
        if loadfile:
            load_file(db)
        if branchs:
            branchs = [(branch, branch)for branch in branchs]
            db.executemany('delete from branch where br=? or rowid=?', branchs)
            print('删除机构成功')
        if report:
            do_report(db)

        if export_qc != "NOSET":
            from .report import export_ylb
            export_ylb(db, export_qc)


if __name__ == '__main__':
    main()
