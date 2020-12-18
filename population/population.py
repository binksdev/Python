# Built-In
import os
# Pandas
import numpy as np
import pandas as pd
# Data Visualization
import matplotlib.pyplot as plt

def visualize_by_gender(option, population):

    # Visualize the distribution of the population by age in Catalunya
    # The last element of the series with the id 100001 contains the sum of all values in the series
    young = population[f'Young_{option}'][100001] / 1000
    older = population[f'Older_{option}'][100001] / 1000
    elder = population[f'Elder_{option}'][100001] / 1000

    plt.bar(['0 - 14', '15 - 64', '65 or more'], [young, older, elder])

    plt.title(f'{option.capitalize()} Distribution in Catalunya by Age')
    plt.xlabel('Age Groups')
    plt.ylabel('Total Population in Thousands')

    plt.show()

def visualize_total(population):

    # Visualize the population of Male and Females in catalunya
    # The last element of the series with the id 100001 contains the sum of all values in the series
    male = population['Male'][100001] / 1000
    female = population['Female'][100001] / 1000

    plt.bar(['Male', 'Female'], [male, female])

    plt.title('Popoulation by Gender in Catalunya')
    plt.xlabel('Genders')
    plt.ylabel('Total Population in Thousands')

    plt.show()

# Data File
filename = 'catalunya_population.csv'

# Dataframe
population_df = pd.read_csv(filename, index_col='Codi')

# Any (Year) column is NaN so we drop it
population_df.drop(columns=['Any'], inplace=True)

# To make readable we will rename the columns to english and simplify their names
# We will rename one at a time to make it easier to understand

# Literal = Location
population_df.rename(columns={"Literal": "Location"}, inplace=True)

# Homes. De 0 a 14 anys   = Young_male
population_df.rename(columns={"Homes. De 0 a 14 anys": "Young_male"}, inplace=True)
# Homes. De 15 a 64 anys  = Older_male
population_df.rename(columns={"Homes. De 15 a 64 anys": "Older_male"}, inplace=True)
# Homes. De 65 anys i més = Elder_male
population_df.rename(columns={"Homes. De 65 anys i més": "Elder_male"}, inplace=True)
# Dones. De 0 a 14 anys   = Young_female
population_df.rename(columns={"Dones. De 0 a 14 anys": "Young_female"}, inplace=True)
# Dones. De 15 a 64 anys  = Older_female
population_df.rename(columns={"Dones. De 15 a 64 anys": "Older_female"}, inplace=True)
# Dones. De 65 anys i més = Elder_female
population_df.rename(columns={"Dones. De 65 anys i més": "Elder_female"}, inplace=True)
# Total. De 0 a 14 anys   = Young_pop
population_df.rename(columns={"Total. De 0 a 14 anys": "Young_people"}, inplace=True)
# Total. De 15 a 64 anys  = Older_pop
population_df.rename(columns={"Total. De 15 a 64 anys": "Older_people"}, inplace=True)
# Total. De 65 anys i més = Elder_pop
population_df.rename(columns={"Total. De 65 anys i més": "Elder_people"}, inplace=True)

# Males
population_df['Male'] = population_df['Young_male'] + population_df['Older_male'] + population_df['Elder_male']
# Females
population_df['Female'] = population_df['Young_female'] + population_df['Older_female'] + population_df['Elder_female']

# Menu Loop
while True:

    try:
        print('Select one of the following options')
        print('1) Distribution of Men by Age')
        print('2) Distribution of Women by Age')
        print('3) Total population by Gender')
        print('4) Exit')

        option = int(input('Enter option: '))

        if option == 1:
            visualize_by_gender('male', population_df)
            os.system('cls')

        elif option == 2:
            visualize_by_gender('female', population_df)
            os.system('cls')

        elif option == 3:
            visualize_total(population_df)
            os.system('cls')

        elif option == 4:
            break

        else:
            print('Option is not valid')

    except ValueError as err:
        print('Integers allowed only')