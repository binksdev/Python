from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import pandas as pd
import os
import champions_list as cl

def get_champion_stats_from_gg(c_url):
	# Extract data from champions.gg using beautifulsoup
	print('Debug in: '+c_url)
	Champion = requests.get(c_url)

	Champion_Site = bs(Champion.content, 'html.parser')
	Champion_Name = Champion_Site.select('.champion-profile h1')[0].get_text()
	Champion_Lane = Champion_Site.select('.champion-profile ul .selected-role a h3')[0].get_text().replace(' ','')
	Champion_Table = Champion_Site.find(class_='champion-statistics')
	Champion_Stats = Champion_Table.select('table tbody')[0]

	All_Fields = Champion_Stats.select('tr')

	Stats_Dict = {}

	for field in All_Fields:
		f_content = field.select('td')[0:2]
		f_name = f_content[0].get_text().replace(' ','')
		f_info = f_content[1].get_text().replace(' ','')
		Stats_Dict[f_name.replace('\n','')] = f_info.replace('\n','')

	Stats_Dict['Name'] = Champion_Name
	Stats_Dict['Lane'] = Champion_Lane.replace('\n','')

	return Stats_Dict

def display_selected_lane(df, lane):
	# Display relevant data from the chosen lane
	lane_list = ['Top','Middle','Jungle','ADC','Support']

	chosen_lane = lane_list[lane-1] # List Starts from 0

	chosen_df = df[df['Lane'] == chosen_lane]

	chose_grp = chosen_df[['Lane','Name','WinRate','BanRate','AverageGamesPlayed','DamageDealt','Kills','GoldEarned']]

	print(chose_grp.sort_values(['WinRate','Kills'], ascending= [False,False]))

# Create empty dictionary
Full_Dict = {}

# Fill dictionary with data from Champion.gg
for i, li in enumerate(cl.list_urls):
	print('Loading Data, Please Wait.')
	print(str(i+1) + ' of ' + str(len(cl.list_urls)) + ' loaded.')
	Full_Dict[str(i)] = get_champion_stats_from_gg(li)
	do_clear()

# Convert Dictionary to DataFrame
champions_df = pd.DataFrame.from_dict(Full_Dict)
transposed_df = champions_df.transpose()

# Remove unrequired column
del transposed_df['OverallPlacement']

# Rename column
transposed_df = transposed_df.rename(columns={'PlayerbaseAverageGamesPlayed': 'AverageGamesPlayed'})

# Adjust column's data types and content
transposed_df['BanRate'] = transposed_df['BanRate'].apply(lambda x : x.replace('%',''))
transposed_df['BanRate'] = transposed_df['BanRate'].astype(float)

transposed_df['WinRate'] = transposed_df['WinRate'].apply(lambda x : x.replace('%',''))
transposed_df['WinRate'] = transposed_df['WinRate'].astype(float)

transposed_df['PlayRate'] = transposed_df['PlayRate'].apply(lambda x : x.replace('%',''))
transposed_df['PlayRate'] = transposed_df['PlayRate'].astype(float)

transposed_df['MinionsKilled'] = transposed_df['MinionsKilled'].astype(np.float32)

transposed_df['Kills'] = transposed_df['Kills'].astype(np.float32)

transposed_df['Deaths'] = transposed_df['Deaths'].astype(np.float32)

transposed_df['Assists'] = transposed_df['Assists'].astype(np.float32)

transposed_df['AverageGamesPlayed'] = transposed_df['AverageGamesPlayed'].astype(np.float32)

transposed_df['DamageDealt'] = transposed_df['DamageDealt'].astype(int)

transposed_df['DamageTaken'] = transposed_df['DamageTaken'].astype(int)

transposed_df['GoldEarned'] = transposed_df['GoldEarned'].astype(int)

# Getting rid of NaN values
transposed_df[['AverageGamesPlayed']] = transposed_df[['AverageGamesPlayed']].fillna(transposed_df[['AverageGamesPlayed']].min())

# Menu Loop
while(True):
	print('League of Legends Info')
	print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
	print('[1] Show all Data')
	print('[2] Highest Win Rate')
	print('[3] Generate CSV File')
	print('[4] Exit')

	choice = int(input('Select an Option: '))

	if choice == 1:
		do_clear()
		with pd.option_context('display.max_rows', None):
			print(transposed_df)

		input('Press enter to return to menu...')

	elif choice == 2:
		print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
		print('[1] Top')
		print('[2] Middle')
		print('[3] Jungler')
		print('[4] AD Carry')
		print('[5] Support')
		lane = int(input('Select a Lane: '))

		do_clear()
		display_selected_lane(transposed_df, lane)

		input('Press enter to return to menu...')

	elif choice == 3:
		name = str(input("Enter file's name: "))
		directory = os.getcwd() + '/csv_files'
		if not os.path.exists(directory):
			os.makedirs(directory)
		transposed_df.to_csv(directory + '/' + name + '.csv')
		do_clear()
		print('File created successfully')
		input('Press enter to return to menu...')

	elif choice == 4:
		break

	else:
		pass
	os.system('cls')