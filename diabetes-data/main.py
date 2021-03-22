# Data Processing Libraries
import pandas as pd
import numpy as np
# Data Visualization Libraries
import matplotlib.pyplot as plt

def visualize_by_condition(content:pd.DataFrame):
    index_p = [1.0, 2.0]
    index_n = [1.2, 2.2]

    for condition in content.columns[2:-1]:

        _, ax = plt.subplots()

        positive = content[['class',f'{condition}']].value_counts()['Positive'].sort_index()
        negative = content[['class',f'{condition}']].value_counts()['Negative'].sort_index()

        positive_value = positive.values.tolist()

        negative_value = negative.values.tolist()

        ax.bar(index_p, positive_value, width=0.2, color='r', align='center', label='positive diabetes')
        ax.bar(index_n, negative_value, width=0.2, color='b', align='center', label='negative diabetes')

        plt.xticks([1.1, 2.1], ['Yes', 'No'])

        plt.xlabel(f'Suffer from {condition}')
        plt.ylabel('No. of Cases')

        plt.title(f'Cases of {condition} in people with diabetes')

        ax.legend()

        plt.show()

def grouped_by_age(content:pd.DataFrame):

    age_positive = content[content['has_diabetes'] == 1]['Age']
    age_negative = content[content['has_diabetes'] == 0]['Age']

    positive = pd.cut(age_positive, bins=[0, 20, 40, 60, 80, 100], include_lowest=True)
    negative = pd.cut(age_negative, bins=[0, 20, 40, 60, 80, 100], include_lowest=True)

    positive_group = age_positive.groupby(positive).count()
    negative_group = age_negative.groupby(negative).count()

    x_pos = range(len(positive_group))
    x_neg = [i+0.2 for i in x_pos]

    _, ax = plt.subplots()

    ax.bar(x_pos, positive_group.values, width=0.2, color='r', label='Positive')
    ax.bar(x_neg, negative_group.values, width=0.2, color='b', label='Negative')

    plt.xticks(x_pos, ['0 to 20', '21 to 40', '41 to 60', '61 to 80', 'over 80'])

    plt.xlabel('Range of Ages')
    plt.ylabel('No. of Persons')

    plt.legend()

    plt.show()

def grouped_by_gender(content:pd.DataFrame):

    index_pos = [1.0, 2.0]
    index_neg = [1.2, 2.2]

    gender_positive = content[content["has_diabetes"] == 1]["Gender"]
    gender_negative = content[content["has_diabetes"] == 0]["Gender"]

    positive = gender_positive.value_counts().sort_index()
    negative = gender_negative.value_counts().sort_index()

    _, ax = plt.subplots()

    ax.bar(index_pos, positive, width=0.2, color='r', label='positive diabetes')
    ax.bar(index_neg, negative, width=0.2, color='b', label='negative diabetes')

    plt.xticks([1.1, 2.1], ['Female', 'Male'])

    plt.legend(loc=4)

    plt.xlabel("Gender")
    plt.ylabel("No. of Cases")

    plt.title("Gender ratio for diabetes cases")

    plt.show()

if __name__ == '__main__':
    content = pd.read_csv('diabetes_data_upload.csv')

    # Visualize if there is any correlation between the afflictions and diabetes
    # visualize_by_condition(content)

    content['has_diabetes'] = [1 if person == 'Positive' else 0 for person in content['class']]

    # Let's create two groups one for Age and another for Gender
    age_group = content[['has_diabetes', 'Age']]
    gen_group = content[['has_diabetes', 'Gender']]

    # grouped_by_age(age_group)
    
    # grouped_by_gender(gen_group)