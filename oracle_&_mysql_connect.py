import datetime
import sys
import mysql.connector
import cx_Oracle
import os 

os.chdir('C:\instantclient_11_2')  # -- This line is used to move the os directory to oracle client installed place so that cx_Oracle will work correctly.

args=sys.argv[1:]
cnx = mysql.connector.connect(user='username', password='password',host='hostname',database='databasename')
cursor = cnx.cursor()
con = cx_Oracle.connect('INFAREP_PROD_READ/infarep_prod_read@inf-prd-ora1.vmware.com:1521/INFPRD')
cur = con.cursor()
query = ("SELECT distinct file_name FROM vdeploy.vDeploy_build where user_story='"+args[0]+"'")
file_prod = "C:\\Users\\amedishetti\\Documents\\Anudeep\\AI\\python_AI\\Artifact\\"+args[0]+"_prod.txt"
file_env = "C:\\Users\\amedishetti\\Documents\\Anudeep\\AI\\python_AI\\Artifact\\"+args[0]+"_"+args[1]+".txt"
cursor.execute(query)
for row in cursor:
    s=row[0]
    if(s[0:2]=="wf"):
        query1 = ("SELECT * FROM (SELECT WF.WORKFLOW_NAME, COUNT(TSK.INSTANCE_NAME) AS TSK_COUNT FROM INFAREP_PROD.REP_WORKFLOWS WF INNER JOIN INFAREP_PROD.REP_TASK_INST TSK ON WF.WORKFLOW_ID=TSK.WORKFLOW_ID GROUP BY WF.WORKFLOW_NAME) S WHERE S.WORKFLOW_NAME='"+s[0:-4]+"'");
        cur.execute(query1)
        for result in cur:
            print(result,file=open(file_prod,"a"))
        query2 = ("SELECT * FROM (SELECT WF.WORKFLOW_NAME, COUNT(TSK.INSTANCE_NAME) AS TSK_COUNT FROM INFAREP_"+args[1]+".REP_WORKFLOWS WF INNER JOIN INFAREP_"+args[1]+".REP_TASK_INST TSK ON WF.WORKFLOW_ID=TSK.WORKFLOW_ID GROUP BY WF.WORKFLOW_NAME) S WHERE S.WORKFLOW_NAME='"+s[0:-4]+"'");
        con = cx_Oracle.connect('username/password@hostname/Servicename')
        cur=con.cursor()
        cur.execute(query2)
        for result in cur:
            print(result,file=open(file_env, "a"))
cursor.close()
cnx.close()
cur.close()
con.close()
file_1 = set()
file_2 = set()
with open(file_prod,'r') as f:
    for line in f:
	    file_1.add(line.strip())
with open(file_env, 'r') as f:
    for line in f:
	    file_2.add(line.strip())
print(file_1-file_2)

