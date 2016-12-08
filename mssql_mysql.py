#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# version 150610v2
#

import os, sys, string
import re
import hashlib
import pymssql, MySQLdb


#
# Export people_host, the export must be utf8 format
#
try:
	mydb = pymssql.connect(host="123.123.123.123",
		user="username",
		password="password",
		database="database",
		as_dict=True)
	cursor = mydb.cursor()

	## query
	query = ("SELECT column_name(s) FROM [dbo].[table] where (change not like '*%' or change IS NULL) and column_name != ''")
	cursor.execute(query)

	### write to fw5 file
	fw5 = open('from5_big5.txt', 'w') # create csv
	for row in cursor:
		fw5.write(row[0] + "," + row[1]+ ","  + row[2]+ ","  + row[3]+ ","  + row[4] + '\n')
	cursor.close()
	mydb.close()
	fw5.close()
except: 
	pass

### encode to utf-8
try:
	myfrom = open('from5_big5.txt')
	myto = open('from5_utf8.txt', 'w')
	content_str = myfrom.read()
	content_str = unicode(content_str,'cp950','ignore').encode('utf-8','ignore')
	myto.write(content_str)
	myfrom.close()
	myto.close()
except:
	pass


#
# webmail_host: all webmail_host group's webmailid webmailpw into directory type
#
directory_email = {}
with open('from8.txt') as fr8:
    for line in fr8:
    	(webmail_id, webmail_pw) = line.strip().split(',')
    	directory_email[(webmail_id)] = webmail_pw
fr8.close()

#
# merge people_host with directory from webmail_host
# Doesn't check the data validity!!!
#
outdb_fr5 = [] #write to: fw5_5notMerge8_webmailID.txt
intodb_fr5 = []
with open('from5_utf8.txt') as fr5:
	for line in fr5:
		list_5 = line.strip().split(',')
		pid = list_5[0]
		pid = pid.upper()
		truename = list_5[3]
		schoolid = list_5[1]
		mainwork = list_5[2]
		username = list_5[4]
		username = username.lower()
		try:
			email_pw = str(directory_email[username])
			intodb_fr5.extend([(column_name(s))])
		except:
			outdb_fr5.extend([(list_5)])
fr5.close()

fw5_outdb = open('fw5_notMerge8_webmailID.txt','w')
for row in outdb_fr5:
	input_result = ",".join(row)
	fw5_outdb.write(input_result + '\n')
fw5_outdb.close()

intodb = open('intodb_before.txt','w')
for row in intodb_fr5:
	input_result = ",".join(row)
	intodb.write(input_result + '\n')
intodb.close()

#
# find the new/old difference from intodb_before.txt
#
fr_new = open('intodb_before.txt')
output_new = []
for line in fr_new: #change to list
	list_new = line.strip()
	output_new.append(list_new)
fr_new.close()

fr_old = open('intodb_before_old.txt')
output_old = []
for line in fr_old:
	list_old = line.strip()
	output_old.append(list_old)
fr_old.close()

set_new = set(output_new) #data is unique in set
set_old = set(output_old)

find_update = list(set_new.difference(set_old)) #find change from new

if not find_update:
	flag_mysql = 0	# find_update is empty, nothing to update
else:
	flag_mysql = 1
	fw_find_update = open('fw_find_update.txt','w')
	for row in find_update:
		fw_find_update.write(row + '\n')
	fw_find_update.close()

#
# flag_mysql = 0	# find_update is empty, nothing to update
# flag_mysql = 1	# find_update into mysql replace/update
#
if flag_mysql == 0 :
	pass
if flag_mysql == 1 :
	try:
		need_update = open('fw_find_update.txt')
		need_update_success = []
		need_update_fail_webmailpw = []
		need_update_fail_schoolid = []
		need_update_fail_pid = []

		#-----------------------Connet MySQL-----------------------
		# connect
		db = MySQLdb.connect("localhost","testuser","testpassword","test123")
		# prepare a cursor object using cursor() method 
		cursor = db.cursor()
		for line in need_update:
			list_update = line.strip().split(',')
			pid_orig = list_update[0]
			pid_orig = pid_orig.upper()
			pid = hashlib.sha256(pid_orig).hexdigest()
			truename = list_update[1]
			schoolid = list_update[2]
			mainwork = list_update[3]
			isaswork = list_update[3]
			subwork = list_update[3]
			subwork = subwork[1:]
			username = list_update[4]
			username = username.lower() #webmailid
			email = list_update[4]+"@webmail.com"
			email = email.lower()
			webmailpw = list_update[5]
			if re.match('^[A-Z][12][0-9]{8}$', pid_orig):
				code = pid_orig
				pid_first = {'A':10,'B':11,'C':12,'D':13,'E':14,'F':15,
					'G':16,'H':17,'I':34,'J':18,'K':19,'L':20,
					'M':21,'N':22,'O':35,'P':23,'Q':24,'R':25,
					'S':26,'T':27,'U':28,'V':29,'W':32,'X':30,
					'Y':31,'Z':33}
				N0=str(pid_first[code[0]])
				N00=int(N0[0])
				N01=int(N0[1])
				N1=int(code[1])
				N2=int(code[2])
				N3=int(code[3])
				N4=int(code[4])
				N5=int(code[5])
				N6=int(code[6])
				N7=int(code[7])
				N8=int(code[8])
				N9=int(code[9])
				check=(N00+N01*9+N1*8+N2*7+N3*6+N4*5+N5*4+N6*3+N7*2+N8+N9)%10
				if check == 0: # correct pid
					#schoolid into directory
					schoolid_directory = {}
					with open('schoolid.txt') as fr_schoolid:
						for line in fr_schoolid:
							(school_mlcid, school_id, school_name) = line.strip().split(',')
							schoolid_directory[(school_mlcid)] = school_id
						fr_schoolid.close()
					try:
						schoolid = str(schoolid_directory[schoolid])
					except:
						schoolid = ""							
					if len(schoolid) != 0:
						#change mainwork
						mainwork_dict = {'1abc':'abc', '2def':'def', '3ghi':'ghi'}
						mainwork = str(mainwork_dict[mainwork])
						#change isaswork
						isaswork_dict = {'1abc':'abc', '2def':'def', '3ghi':'ghi'}
						isaswork = str(isaswork_dict[isaswork])
						if schoolid == '000001': 
							mainwork = 'manager'
							isaswork = 'manager'
						if re.match('^[$1$].*[$].*', webmailpw):
							try:
								cursor.execute("REPLACE INTO mlcuser VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (column_name(s)))
								need_update_success.extend([(column_name(s)])
								db.commit()
							except:
								db.rollback()
		db.close() # disconnect from server	

		fw_need_update_success = open('fw_need_update_success.txt','w')
		for row in need_update_success:
			input_result = ",".join(row)
			fw_need_update_success.write(input_result + '\n')
		fw_need_update_success.close()
	except:
		pass
