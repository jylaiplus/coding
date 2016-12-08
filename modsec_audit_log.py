#!/usr/bin/python2.5
#encoding: utf-8
#Date: 2009-03-27

import re
import MySQLdb
fr = open('/etc/modsecurity/logs/modsec_audit (copy).log')
fw = open('/home/bukokoro/fw.txt', 'w')
count= 0

#-----------------------Regular Express-----------------------
#match secA string
secA_regex = re.compile(r'^[[0-9]*/[A-Za-z]*/[0-9]*:[0-9]*:[0-9]*:[0-9]*.*')

#match secA_date
secA_date_regex = re.compile(r'[0-9]*/[A-Za-z]*/[0-9]*:[0-9]*:[0-9]*:[0-9]*')
date_regex = re.compile(r'[^:]+')

#match secA_id
secA_id_regex = re.compile(r'([0-9]{1,3}\.)+[0-9]*.([0-9]*)')

#=================================================================
#match secB string
secB_regex = re.compile(r'^.*HTTP/1.1$', re.M)

#match secB_reqMethod
secB_reqMethod_regex = re.compile(r'\w*')

#match secB_reqPath
secB_reqPath_regex = re.compile(r'[^\w].*(.*)[^HTTP/1.1]')

#=================================================================
#match 40_generic_attacks.conf string
key_regex = re.compile('generic_attacks.*msg.*]')

#id-Unique rule ID, as specified by the id action
#rid_regex      = re.compile(r'\[id "([^"]+)')

#System Command Injection
msg_regex      = re.compile(r'\[msg "([^"]+)')

#CRITICAL
severity_regex = re.compile(r'\[severity "([^"]+)')

#WEB_ATTACK/COMMAND_INJECTION
tag_regex      = re.compile(r'\[tag "([^"]+)')

# match string User-Agent
user_agent_regex = re.compile(r'^User-Agent:.*')

# match client
client_regex = re.compile(r'[^User -Agent:].*')

# match string Server
server_str_regex = re.compile(r'^Server:.*')

# match server
server_regex = re.compile(r'[^Server:].*')

#-----------------------Connet MySQL-----------------------
# connect
db = MySQLdb.connect(host="localhost", user="root", passwd="db123", db="modsec_audit")

# create a cursor
cursor = db.cursor()

for i in fr:
    match_secA = secA_regex.search(i)
    match_secB = secB_regex.search(i)
    match_user_agent = user_agent_regex.search(i)
    match_attack = key_regex.search(i)
    match_server = server_str_regex.search(i)    
    if match_secA:
        log_secA  = match_secA.group()
        secA_id   = secA_id_regex.search(log_secA).group(2)
        secA_date = secA_date_regex.search(log_secA).group(0)
        #translate date
        date = date_regex.search(secA_date)
        date = date.group()
        date = re.sub('Jan', '01', date)
        date = re.sub('Feb', '02', date)
        date = re.sub('Mar', '03', date)
        date = re.sub('Apr', '04', date)
        date = re.sub('May', '05', date)
        date = re.sub('Jun', '06', date)
        date = re.sub('Jul', '07', date)
        date = re.sub('Aug', '08', date)
        date = re.sub('Sept', '09', date)
        date = re.sub('Oct', '10', date)
        date = re.sub('Nov', '11', date)
        date = re.sub('Dec', '12', date)
        date = re.split(r'/', date)
        date = date[2] + '-' + date[1] + '-' + date[0]
        time = re.split(r':', secA_date)
        time = time[1] + ':' +time[2] + ':' +time[3]
        secA_date = date + ' ' + time
    if match_secB:
        log_secB         = match_secB.group()
        secB_reqMethod   = secB_reqMethod_regex.search(log_secB).group(0)
        secB_reqPath     = re.sub("[;]", ':', secB_reqPath_regex.search(log_secB).group(0))
        secB_reqPath     = re.sub("script>", "script'>", secB_reqPath)
        secB_reqPath     = re.sub("SCRIPT>", "SCRIPT'>", secB_reqPath)
        secB_reqPath     = re.sub("[/]", "/'", secB_reqPath)
        
    if match_user_agent:
        match_client = match_user_agent.group()
        client = client_regex.search(match_client).group()
    if match_attack:
        log_attack = match_attack.group()
        fw_in = secA_id + '|'+ secA_date +'|'+ msg_regex.search(log_attack).group(1) +'|'+ severity_regex.search(log_attack).group(1) +'|'+ tag_regex.search(log_attack).group(1)
        fw.write(fw_in + '\n')
        msg        = msg_regex.search(log_attack).group(1)
        severity   = severity_regex.search(log_attack).group(1)
        tag        = tag_regex.search(log_attack).group(1)
        #execute SQL statement
        cursor.execute("INSERT INTO generic_attacks (secA_id, secA_date, secB_reqMethod, secB_reqPath, msg, severity, tag, client, server) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (secA_id, secA_date, secB_reqMethod, secB_reqPath, msg, severity, tag, client, server))
        count+=1
        print str(count),
    if match_server:
        match_server = match_server.group()
        server = server_regex.search(match_server).group()
fw.close()
fr.close()
