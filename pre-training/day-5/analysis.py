import pandas as pd

"""
Titanic Dataset Column Descriptions:

PassengerId : Unique passenger identifier

Survived    : Survival status
              0 = No, 1 = Yes

Pclass      : Ticket class
              1 = 1st, 2 = 2nd, 3 = 3rd

Name        : Full name of the passenger

Sex         : Gender

Age         : Age in years

SibSp       : Number of siblings / spouses aboard

Parch       : Number of parents / children aboard

Ticket      : Ticket number

Fare        : Passenger fare

Cabin       : Cabin number

Embarked    : Port of embarkation
              C = Cherbourg, Q = Queenstown, S = Southampton
"""

titanic_columns = {
    "PassengerId": "Unique passenger identifier",
    "Survived": "Survival status (0 = No, 1 = Yes)",
    "Pclass": "Ticket class (1 = 1st, 2 = 2nd, 3 = 3rd)",
    "Name": "Full name of the passenger",
    "Sex": "Gender of the passenger",
    "Age": "Age in years",
    "SibSp": "Number of siblings/spouses aboard",
    "Parch": "Number of parents/children aboard",
    "Ticket": "Ticket number",
    "Fare": "Fare paid by the passenger",
    "Cabin": "Cabin number",
    "Embarked": "Port of embarkation (C = Cherbourg, Q = Queenstown, S = Southampton)"
}

def analyze_data(file_path):
    # Load the dataset
    data = pd.read_csv(file_path)
    
    # How many passengers survived vs. didn't? Show as counts and percentages
    if 'Survived' in data.columns:
        print("\nSurvival Count:")
        print(data['Survived'].value_counts())
        print("\nSurvival Percentage:")
        print(data['Survived'].value_counts(normalize=True) * 100)

    # What was the survival rate by passenger class (1st, 2nd, 3rd)?
    if 'Survived' in data.columns and 'Pclass' in data.columns:
        print("\nSurvival Rate by Passenger Class:")
        print(data.groupby('Pclass')['Survived'].mean() * 100)

    # Average Age of passengers who survived vs those who did not
    if 'Survived' in data.columns and 'Age' in data.columns:
        print("\nAverage Age of Passengers by Survival Status:")
        print(data.groupby('Survived')['Age'].mean())
    
    # Which embarkation port had the highest survival rate
    if 'Survived' in data.columns and 'Embarked' in data.columns:
        print("\nSurvival Rate by Embarkation Port:")
        print(data.groupby('Embarked')['Survived'].mean() * 100)
    
    # How many passengers have missing values in Age column. Fill missing values with the median age
    if 'Age' in data.columns:
        print("\nNumber of Passengers with Missing Age Values:")
        print(data['Age'].isnull().sum())
        median_age = data['Age'].median()
        print("\nMissing Age Values Filled with Median Age:", median_age)
        data['Age'] = data['Age'].fillna(median_age)

    # Oldest surviving passenger: print name, age, and class
    if 'Age' in data.columns and 'Survived' in data.columns and 'Name' in data.columns and 'Pclass' in data.columns:
        oldest_survivor = data.loc[data['Survived'] == 1, 'Age'].max()
        oldest_survivor_data = data.loc[(data['Survived'] == 1) & (data['Age'] == oldest_survivor), ['Name', 'Age', 'Pclass']]
        print("\nOldest Surviving Passenger:")
        print(oldest_survivor_data)
    
    # What % of women survived vs. what % of men survived
    if 'Survived' in data.columns and 'Sex' in data.columns:
        print("\nSurvival Rate by Gender:")
        print(data.groupby('Sex')['Survived'].mean() * 100)

    # Create a new column 'AgeGroup': Child (<18), Adult (18-60), Senior (60+). Show survival rate per group
    if 'Age' in data.columns:
        data['AgeGroup'] = pd.cut(data['Age'], bins=[0, 18, 60, 150], labels=['Child', 'Adult', 'Senior'])
        print("\nSurvival Rate by Age Group:")
        print(data.groupby('AgeGroup')['Survived'].mean() * 100)

    # Among 3rd class passengers, what was the survival rate for men vs. women?
    if 'Survived' in data.columns and 'Sex' in data.columns and 'Pclass' in data.columns:
        print("\nSurvival Rate by Gender (3rd Class):")
        print(data[data['Pclass'] == 3].groupby('Sex')['Survived'].mean() * 100)

    # Drop all rows with missing Cabin data. How many rows remain? What % of original data did you keep?
    if 'Cabin' in data.columns:
        original_rows = len(data)
        data = data.dropna(subset=['Cabin'])
        remaining_rows = len(data)
        print(f"\nRows with missing Cabin data dropped. Remaining rows: {remaining_rows}")
        print(f"Percentage of original data kept: {(remaining_rows / original_rows) * 100:.2f}%")

if __name__ == "__main__":
    file_path = "titanic.csv"  # Replace with your dataset path
    analyze_data(file_path)