create table if not exists lzwenti(
    period text,
    category text,
    branch text,
    name text,
    content text,
    depertment text,
    
);

create table if not exists brreport(
    id text primary key,
    period text,
    type text,
    branch text,
    name text,
    date text,
    content text,
    update_time int
);