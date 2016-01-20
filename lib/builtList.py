_ELECP=['ELECPAC','ELECPAM','ELECPAP','ELECPAV','ELECPAW','ELECPCN','ELECPJC','ELECPJP','ELECPSC','ELECPSE','ELECPSF','ELECPSU']
_ELECQ=['ELECQAC','ELECQAM','ELECQAP','ELECQAV','ELECQAW','ELECQCN','ELECQJC','ELECQJP','ELECQSC','ELECQSE','ELECQSF','ELECQSU']
_ELECK=['ELECKAC','ELECKAM','ELECKAP','ELECKAV','ELECKAW','ELECKCN','ELECKJC','ELECKJP','ELECKSC','ELECKSE','ELECKSF','ELECKSU']
_ELECT=['ELECTAP','ELECTJP','ELECTSU']
_ELECR=['ELECRAC','ELECRAM','ELECRAP','ELECRAV','ELECRAW','ELECRCN','ELECRJC','ELECRJP','ELECRSC','ELECRSE','ELECRSF','ELECRSU']
_ELECF=['ELECFAP','ELECFJP','ELECFSU']
_ODAP=['PREMODAP','ARHODAP']
_ODAT=['PREMODAT','ARHODAT']
_MUT04=['OPAC36','OPAC36R','IWAU','IWDEMOS','IWINFO','IWMT1','IWVAL72','IWPL','LINE','AIPPROD','CIF','PREMHHM','SIPEAPRD','SIPEARE7','SIPCACR7','SIPCACP','HHWEB','OPM','G3HCHRON','GCSROPRD','SIPEARH']

_DBLIST = {
	'ELECP':_ELECP,
	'ELECQ':_ELECQ,
	'ELECK':_ELECK,
	'ELECT':_ELECT,
	'ELECR':_ELECR,
	'ELECF':_ELECF,
	'ELECALL':_ELECP+_ELECQ+_ELECK+_ELECT+_ELECR+_ELECF,
	'ODAP':_ODAP,
	'ODAT':_ODAT,
	'ODAALL':_ODAP+_ODAT,
	'MUTALL':_MUT04
}

_REGISTEREDQUERY = {
        'etatbase':"select open_mode from v$database",
	'redofrequency':"""SELECT SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH:MI:SS'), 1, 5) "DAY(MM/DD)",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'00', 1,0))"00",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'01', 1,0))"01",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'02', 1,0))"02",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'03', 1,0))"03",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'04', 1,0))"04",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'05', 1,0))"05",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'06', 1,0))"06",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'07', 1,0))"07",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'08', 1,0))"08",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'09', 1,0))"09",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'10', 1,0))"10",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'11', 1,0))"11",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'12', 1,0))"12",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'13', 1,0))"13",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'14', 1,0))"14",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'15', 1,0))"15",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'16', 1,0))"16",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'17', 1,0))"17",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'18', 1,0))"18",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'19', 1,0))"19",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'20', 1,0))"20",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'21', 1,0))"21",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'22', 1,0))"22",
		SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'23', 1,0))"23",
		COUNT (*) TOTAL
FROM v$log_history a
		GROUP BY SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH:MI:SS'), 1, 5)
		ORDER BY SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH:MI:SS'), 1, 5) DESC""",
	'redofrequencyweek':"""SELECT SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH:MI:SS'), 1, 5) "DAY(MM/DD)",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'00', 1,0))"00",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'01', 1,0))"01",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'02', 1,0))"02",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'03', 1,0))"03",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'04', 1,0))"04",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'05', 1,0))"05",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'06', 1,0))"06",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'07', 1,0))"07",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'08', 1,0))"08",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'09', 1,0))"09",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'10', 1,0))"10",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'11', 1,0))"11",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'12', 1,0))"12",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'13', 1,0))"13",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'14', 1,0))"14",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'15', 1,0))"15",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'16', 1,0))"16",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'17', 1,0))"17",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'18', 1,0))"18",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'19', 1,0))"19",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'20', 1,0))"20",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'21', 1,0))"21",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'22', 1,0))"22",
                SUM (DECODE (SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH24:MI:SS'), 10, 2),'23', 1,0))"23",
                COUNT (*) TOTAL
FROM v$log_history a
		WHERE first_time > SYSDATE - 7
                GROUP BY SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH:MI:SS'), 1, 5)
                ORDER BY SUBSTR (TO_CHAR (first_time, 'MM/DD/RR HH:MI:SS'), 1, 5) DESC""",
        'opencursors':"""select s as SID, u as username, MaxVal, PrmVal, round(100*MaxVal/PrmVal) Pct
 from
 (select to_number(value) as PrmVal
 from v$parameter
 where name = 'open_cursors'),
  (select s, u, a MaxVal
   from
    (select op.sid s, nvl(user_name, 'Background') u, count(*) a,
            row_number() over (ORDER BY count(*) Desc) r
     from v$open_cursor op, v$session
     where v$session.sid = op.sid
        and v$session.username =op.user_name
     group by op.sid, user_name)
   where r=1)""",
        'processes':"""select MaxVal as PrmVal, PrmVal as Val, round(100*PrmVal/MaxVal) Pct
 from
 (select to_number(value) as MaxVal from v$parameter where name = 'processes'),
 (select count(*) as PrmVal from v$process)""",
        'tablespaces':"""with
files as
     (select tablespace_name, sum (bytes) total_tbs_bytes
      from dba_data_files
      group by tablespace_name
      union
      select tablespace_name, sum (bytes) total_tbs_bytes
      from dba_temp_files
      group by tablespace_name),
fragments as
     (select tablespace_name, sum (bytes) total_tbs_free_bytes
      from dba_free_space
      group by tablespace_name
      union
      select a.tablespace_name, d.bytes_total - SUM (a.used_blocks * d.block_size) total_tbs_free_bytes
      from v$sort_segment a,
            (
            select b.name, c.block_size, sum(c.bytes) bytes_total
            from v$tablespace b, v$tempfile c
            where b.ts#= c.ts#
            group by b.name, c.block_size
            ) d
      where a.tablespace_name = d.name
      group by a.tablespace_name, d.bytes_total ),
autoextend as

     (select tablespace_name, sum (size_to_grow) total_growth_tbs
      from (select tablespace_name, sum (maxbytes) size_to_grow
            from dba_data_files
            where autoextensible = 'YES'
            group by tablespace_name
            union
            select tablespace_name, sum (bytes) size_to_grow
            from dba_data_files
            where autoextensible = 'NO'
            group by tablespace_name
            union
            select tablespace_name, sum (maxbytes) size_to_grow
            from dba_temp_files
            where autoextensible = 'YES'
            group by tablespace_name
            union
            select tablespace_name, sum (bytes) size_to_grow
            from dba_temp_files
            where autoextensible = 'NO'
            group by tablespace_name)
      group by tablespace_name)
select e.tablespace_name,
       round((((files.total_tbs_bytes - fragments.total_tbs_free_bytes)/autoextend.total_growth_tbs)*100)) PCT_USED
from dba_tablespaces e, files, fragments, autoextend
where e.tablespace_name = files.tablespace_name
  and e.tablespace_name = fragments.tablespace_name
  and e.tablespace_name = autoextend.tablespace_name
order by PCT_USED desc""",
	'flashUsed':"""select round(sum(percent_space_used),0) as PctUsed from v$flash_recovery_area_usage""",
	'statsAuto':"""SELECT JOB_STATUS, trunc(sysdate-nvl(to_date(to_char(JOB_START_TIME, 'DD/MM/YYYY'), 'DD/MM/YYYY'), sysdate)) Past_Days
FROM   DBA_AUTOTASK_JOB_HISTORY
WHERE  client_name ='auto optimizer stats collection'
  AND  JOB_START_TIME = (select max(JOB_START_TIME) FROM DBA_AUTOTASK_JOB_HISTORY WHERE client_name ='auto optimizer stats collection')
ORDER BY JOB_START_TIME DESC""",
	'objectsize':"""select owner, segment_name, nvl(partition_name,'none'), round(bytes/1048576) from dba_segments""",
	'sessions':"""select count(*) nbsession from v$session where type != 'BACKGROUND'""",
	'volArch':""" select nvl(round(sum(blocks*block_size)/1024/1024), 0) SizeMB from v$archived_log where COMPLETION_TIME > to_date(to_char(sysdate, 'DD/MM/YYYY'), 'DD/MM/YYYY') and name is not null""",
	'memorycache':"""select 'LIBCACHE' cache, round(100*(1-sum(reloads)/sum(pins)),0) Ratio
 from v$librarycache
 union
 select 'BUFCACHE' cache, round(100*(1-(phy.value-dir.value-lob.value)/ses.value),0) Ratio
 from v$sysstat ses, v$sysstat lob, v$sysstat dir, v$sysstat phy
 where ses.name='session logical reads'
   and phy.name='physical reads'
   and dir.name='physical reads direct'
   and lob.name='physical reads direct (lob)'""",
	'datasize':"""select round(sum(bytes)/1024/1024/1024) SizeGB from dba_segments"""
}

