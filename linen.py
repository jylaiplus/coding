# -*- coding: utf-8 -*-
# qpy: console
# qpy: jylaiplus
"""
This is an py for calculating stocks of linen.

@Author: jylaiplus
@Date: 2016-08-03-1659
"""

def sum(four_dep, double_dep, single_dep, room_stay):
	super_king_sheets = four_dep * 1
	kingsize_sheets = double_dep * 2 + single_dep * 1
	pillowcases = four_dep * 4 + double_dep * 8 + single_dep * 4
	kingsize_duvet_covers = double_dep * 2 + single_dep * 1
	hand_towels = four_dep * 2 + double_dep * 2 + single_dep * 2 + room_stay * 2
	bath_sheets = four_dep * 2 + double_dep * 2 + single_dep * 2 + room_stay * 2
	bath_mats = four_dep * 1 + double_dep * 1 + single_dep * 1 + room_stay * 1
	super_king_duvet = four_dep * 1
	single_king_sheets = double_dep * 2 + single_dep * 1
	single_king_duvet = double_dep * 2 + single_dep * 1
	print('===== Result =====')
	print('Super King Sheets: ', super_king_sheets)
	print('KINGSIZE SHEETS: ', kingsize_sheets)
	print('PILLOWCASES: ', pillowcases)
	print('KINGSIZE DUVET COVERS: ', kingsize_duvet_covers)
	print('')
	print('HAND TOWELS: ', hand_towels)
	print('BATH SHEETS: ', bath_sheets)
	print('BATH MATS: ', bath_mats)
	print('')
	print('Super King Duvet: ', super_king_duvet)
	print('Single Sheets: ', single_king_sheets)
	print('Single Duvet: ', single_king_duvet)

# Wait for valid input in while...not
is_valid=0
while not is_valid:
	try:
		four_dep = int(raw_input('400 room is Departed?'))
		double_dep = int(raw_input('Double room is Departed?'))
		single_dep = int(raw_input('Single room is Departed (except 400)?'))
		room_stay = int(raw_input('All room is Stay?'))
		is_valid = 1
	except ValueError:
		print('')
		print ('Empty input: Please restart your input.')
		print('')

if is_valid == 1:
	sum(four_dep, double_dep, single_dep, room_stay)
