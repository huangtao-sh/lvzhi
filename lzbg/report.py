# 项目：工作平台
# 模块：主管履职报告报表
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-05-25 20:48

from .db import path
from orange import Path
from glemon import P

FORMATS = {       # 预定义格式
    'h1': {'font_name': '黑体', 'text_wrap': True, 'font_size': 18,
           'align': 'center'},  # 一级标题
    'wrap': {'font_name': '微软雅黑', 'text_wrap': True, 'valign': 'vcenter'},  # 折行
    'cwrap': {'font_name': '微软雅黑', 'text_wrap': True, 'align': 'center',
              'valign': 'vcenter'},  # 换行并居中
    'normal': {'font_name': '微软雅黑'}}  # 正常


YLBFORMAT = [
    {'header': '机构', "width": 20, 'format': 'cwrap'},
    {'header': '报告人', 'width': 9, 'format': 'cwrap'},
    {'header': '内容', 'width': 50, 'format': 'wrap'},
    {'header': '收集问题', 'width': 50, 'format': 'wrap'},
]

SBFORMAT = [
    {'header': '机构', "width": 20, 'format': 'cwrap'},
    {'header': '报告人', 'width': 9, 'format': 'cwrap'},
    {'header': '异常机具', 'width': 35, 'format': 'wrap'},
    {'header': '异常内容', 'width': 50, 'format': 'wrap'},
]


def export_ylb(qc=None, fn=None):
    from .lzbg import get_qc
    date = get_qc(qc)
    qc = date[0][:7]
    print(f'期次    ：{qc}')
    print(f'日期区间：{date[0]} - {date[1]}')
    ylb_path = path / '一览表'
    ylb_path.ensure()
    fn = ylb_path / ('营业主管履职报告一览表（%s）.xlsx' % (qc))

    if fn.exists():
        s = input('%s 已存在，是否覆盖，Y or N?\n' % (fn.name))
        if s.upper() != 'Y':
            return
    print(f'生成文件：{fn}')
    return
    wt_data, zh_data, sb_data = [], [], []
    for obj in LzBaogao.objects(P.qc == qc):
        for k in obj.nr:
            if (('建议' in k['zl'])or('问题'in k['zl']))and(len(k['nr']) >= 10):
                wt_data.append(('%s%s' % (obj.br, obj.dept),
                                obj.name,  k['nr'], None))
        if obj.zhjj and (len(obj.zhjj) > 5):
            zh_data.append(('%s%s' % (obj.br, obj.dept),
                            obj.name, obj.zhjj, None))
        if obj.err_devs or obj.dev_errs:
            sb_data.append(('%s%s' % (obj.br, obj.dept),
                            obj.name, obj.err_devs, obj.dev_errs))
    fn.write_tables(
        {'sheet': '问题及建议', 'columns': YLBFORMAT, 'data': wt_data},
        {'sheet': '需总行解决问题', 'columns': YLBFORMAT, 'data': zh_data},
        {'sheet': '机具问题', 'columns': SBFORMAT, 'data': sb_data},
        formats=FORMATS, force=True
    )
    print('导出问题：%d条' % (len(wt_data)))
    print('需总行解决问题：%d条' % (len(zh_data)))
    print('设备问题：%d条' % (len(sb_data)))


WTFORMAT = [
    {'header': '问题分类', 'width': 13.5, 'format': 'cwrap'},
    {'header': '机构', 'width': 24.63, 'format': 'cwrap'},
    {'header': '具体内容', 'width': 57.63, 'format': 'wrap'},
    {'header': '报告人', 'width': 10.88, 'format': 'cwrap'},
    {'header': '答复人', 'width': 10.88, 'format': 'cwrap'},
    {'header': '答复意见', 'width': 47.38, 'format': 'wrap'}]


def export_wt(yyb=True, fn=None):
    yf = LzBaogao.cur_qc()
    print('当前月份：%s' % (yf))
    fn = path / '3处理问题' / ('营业主管履职报告（%s）·.xlsx' % (yf))
    data = list(LzWenTi.objects(yf=yf).order_by('bm', 'wtfl', 'dfr').scalar(
        'wtfl', 'jg', 'jtnr', 'bgr', 'dfr', 'dfyj'))
    with fn.write_xlsx(formats=FORMATS) as book:
        book.worksheet = '运营管理部'
        book.A1_F1 = '营业主管履职报告重点问题（%s）' % (yf), "h1"
        book.add_table("A2", columns=WTFORMAT, data=data)
        print('共导出%d条数据' % (len(data)))


PUBLISH_FORMAT = {
    'title': {'font_name': '仿宋', 'font_size': 18, 'bold': True, 'align': 'center'},
    'header': {'font_name': '黑体', 'font_size': 14, 'align': 'center'},
    'center': {'font_name': '微软雅黑', 'font_size': 11, 'valign': 'vcenter', 'align': 'center',
               'text_wrap': True},
    'nr': {'font_name': '微软雅黑', 'font_size': 11, 'valign': 'vcenter',
           'text_wrap': True},
}
