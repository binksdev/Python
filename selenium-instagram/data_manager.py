import pandas as pd
import json
import os

def get_data(data):
    # Convert List of Dictionaries into a DataFrame
    dataframe = pd.DataFrame(data)

    # Get Description
    content = dataframe.describe()

    # Save Description as a Dictionary
    desc = {'Likes':
                    {
                    'mean': round(content['Likes'].mean(), 2),
                    'median': round(content['Likes'].median(), 2),
                    'min': round(content['Likes'].min(), 2),
                    'max': round(content['Likes'].max(), 2),
                    'variance': round(content['Likes'].std(), 2)
                    },
            'Comments':
                    {
                    'mean': round(content['Comments'].mean(), 2),
                    'median': round(content['Comments'].median(), 2),
                    'min': round(content['Comments'].min(), 2),
                    'max': round(content['Comments'].max(), 2),
                    'variance': round(content['Comments'].std(), 2)
        	    	}
            }

    return desc

def data_to_file(data):
    # Create data folder if it doesn't exists
    current_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_path, 'data')

    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    # JSON filename
    filename = os.path.join(folder_path, 'data.json')

    # Create JSON file and save data
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)