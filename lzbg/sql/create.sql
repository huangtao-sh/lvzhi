/*
    营业主管问题一览表
*/

create table if not exists lzwenti(
    type text,                -- 0-分管行长，1-运营主管，2-营业主管 
    period text,              -- 运营主管：2018-1；营业主管： 2018-01  
    category text null,       -- 运营主管：分行序号，营业主管：问题分类 
    rpt_branch text,          -- 报告机构 
    rpt_name text,            -- 报告人
    content text,             -- 问题内容
    reply text null,          -- 答复意见
    reply_depart text null,   -- 答复部门
    reply_name text null,     -- 答复人
    state text null,          -- 状态跟踪
    importance bool null      -- 重要性
);
/*
    分管行长、运营主管报告
*/
create table if not exists brreport(
    id text primary key,    -- 编号
    period text,            -- 报告期 ，2018-1
    type text,              -- 类型：0-分管行长，1-运营主管
    branch text,            -- 分行
    name text,              -- 姓名
    date text,              -- 报告时间
    content text            -- 报告内容
);
/*
    导入文件记录，用于防止重复导入文件
*/
create table if not exists loadfile(
    filename text primary key,  -- 文件名
    mtime int                   -- 修改时间
);

/*
    分行序列表
*/
create table if not exists brorder(
    brname text primary key,       -- 分行名称
    "order" int,                     -- 序号
    state bool                     -- 状态
);