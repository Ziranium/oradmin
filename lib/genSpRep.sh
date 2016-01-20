#! /bin/bash
# Created by Jonathan LAMBERT - jlambert@sigma.fr - www.sigma.fr

display_usage() {
        echo -e "\nUsage:\n$0 [arguments] \n"
        echo -e "\nArguments :"
        echo -e "\t-d [Instance]"
        echo -e "\t-s [dateStart] : ddmmhh24mi (9 fevrier 8h00 : 09020800)"
        echo -e "\t-e [dateEnd] : ddmmhh24mi (9 fevrier 20h00 : 09022000)"
	echo -e "\t-u [user]"
	echo -e "\t-p [password user]\n"
}

while getopts "s:e:d:p:u:" opt; do
  case $opt in
    s)
      DATESTART=$OPTARG
      ;;
    e)
      DATEEND=$OPTARG
      ;;
    d)
      ORACLE_SID=$OPTARG
      ;;
    p)
      PASS=$OPTARG
      ;;
    u)
      USER=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      display_usage
      ;;
  esac
done

if [ -z "${DATESTART}" -o -z "${DATEEND}" -o -z "${ORACLE_SID}" ]; then
    display_usage
    exit 2
fi

INST_NUM=1

case "$ORACLE_SID" in
  *[0-9])     ORACLE_DB=${ORACLE_SID%?}
              INST_NUM=${ORACLE_SID: -1}
              ;;
  *)          ORACLE_DB=$ORACLE_SID
              ;;
esac

case "$USER" in
  sys)        SYSDBA="as sysdba"
              ;;
  *)          SYSDBA=""
              ;;
esac

export $ORACLE_SID

sqlplus $USER/$PASS@$ORACLE_DB $SYSDBA <<EOF
column  begin_snap      new_value   begin_snap
column  end_snap        new_value   end_snap
column  report_name     new_value   report_name
column  inst_num        new_value   inst_num
column  dbid            new_value       dbid

select dbid from v\$database;
select ${INST_NUM} inst_num from dual;
select t1.snap_id begin_snap, t2.snap_id end_snap, '/tmp/sp_' || '${ORACLE_SID}_'  || t1.snap_time || '-' || t2.snap_time || '.txt' report_name from
(select snap_id, to_char(snap_time,'ddmmhh24mi') snap_time from perfstat.stats\$snapshot where to_char(snap_time,'ddmmhh24mi')= $DATESTART and instance_number = &inst_num and dbid = &dbid) t1,
(select snap_id, to_char(snap_time,'ddmmhh24mi') snap_time from perfstat.stats\$snapshot where to_char(snap_time,'ddmmhh24mi')= $DATEEND and instance_number = &inst_num and dbid = &dbid) t2;

start /u02/app/oracle/product/11.2.0.4/dbhome_1/rdbms/admin/sprepins

exit
EOF

