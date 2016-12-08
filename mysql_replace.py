#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# for master update - version 150304
#

import os, sys, string, csv
import re
import hashlib
import MySQLdb

#
# Export (163.Student), the export must be utf8 format
#
try:
	#-----------------------Connet MySQL-----------------------
	# connect
	db = MySQLdb.connect("localhost","username","password","db_name")
	
	# prepare a cursor object using cursor() method 
	cursor = db.cursor()

	## query
	query = ("SELECT column_name(s) FROM master")
	cursor.execute(query)

	### write to fw5 file
	fwdb = open('db-export.txt', 'w')

	# create csv
	for row in cursor:
		fwdb.write(row[0] + "," + row[1]+ ","  + row[2]+ ","  + row[3]+ '\n')
	cursor.close()
	db.close()
	fwdb.close()
except: 
	pass

#
# find the delete-student difference from readbook_quarterly.csv and db-export.txt
#
fr_new = open('readbook.csv')
output_new = []
for line in fr_new: #change to list
	list_readbook = line.strip().split(',')
	pid_orig = list_readbook[0]
	pid_orig = pid_orig.upper()
	pid = hashlib.sha256(pid_orig).hexdigest()
	truename = list_readbook[1]
	schoolid = list_readbook[2]
	schoolno = list_readbook[3]
	password = hashlib.md5(pid_orig).hexdigest()
	list_new = pid + "," + truename + "," + schoolid + "," + schoolno + "," + password
  	output_new.append(list_new)
fr_new.close()

fr_old = open('db-export.txt')
output_old = []
for line in fr_old:
	list_old = line.strip()
	output_old.append(list_old)
fr_old.close()

set_new = set(output_new) #the data is unique
set_old = set(output_old)
find_update = list(set_new.difference(set_old))

if not find_update:
	flag_mysql = 0	# find_delete is empty, nothing to update
else:
	flag_mysql = 1
	fw_find_update = open('master-find-update.txt','w')
	for row in find_update:
		fw_find_update.write(row + '\n')
	fw_find_update.close()

	#schoolname into dictionary
	schoolname_directory = {}
	with open('schoolname.txt') as fr_schoolname:
		for line in fr_schoolname:
			(school_id, school_name) = line.strip().split(',')
			schoolname_directory[(school_id)] = school_name
		fr_schoolname.close()

#
# flag_mysql = 0	# find_update is empty, nothing to update
# flag_mysql = 1	# find_update into mysql replace/update
#
if flag_mysql == 0 :
	pass
if flag_mysql == 1 :
	try:
		need_update = open('master-find-update.txt')
		need_update_success = []
		need_update_fail = []
		db = MySQLdb.connect("localhost","username","password","master")
		cursor = db.cursor()
		for line in need_update: # iterates the rows of the file in orders
			list_update = line.strip().split(',')
			pid = list_update[0]
			truename = list_update[1]
			schoolid = list_update[2]
			schoolno = list_update[3]
			mainwork = 'Student'
			username = schoolid + "-" + schoolno
			password = list_update[4]
			
			try:
				schoolname = str(schoolname_directory[schoolid])
			except:
				schoolname = schoolid
			
			try:
				insertstmt = ("REPLACE INTO mlcstudent (column_name(s)) \
					VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" \
					% (column_name(s)))
				cursor.execute(insertstmt)
				need_update_success.extend([(column_name(s))])
				db.commit()
			except:
				need_update_fail.extend([(column_name(s))])
			db.rollback()
		db.close()

		fw_need_update_success = open('need-update-success.txt','w')
		for row in need_update_success:
			input_result = ",".join(row)
			fw_need_update_success.write(input_result + '\n')
		fw_need_update_success.close()

		fw_need_update_fail = open('need-update-fail.txt','w')
		for row in need_update_fail:
			input_result = ",".join(row)
			fw_need_update_fail.write(input_result + '\n')
		fw_need_update_fail.close()					

	except:
		fw_fail_update_file = open('fail-update-inputfile.txt','w')
		fw_fail_update_file.close()
		pass
