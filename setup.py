# 项目：工作平台
# 模块：安装模块
# 作者：黄涛
# License:GPL
# Email:huangtao.sh@icloud.com
# 创建：2018-02-13

from orange import setup

__version__ = '0.2a2'

# 命令行程序入口
cscripts = [
    'lzbg=lzbg:main'
]

setup(
    name='lzbg',
    author='huangtao',
    description='履职报告',
    entry_points={'console_scripts': cscripts, },
    version=__version__,
)
