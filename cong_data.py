import censusdata
import pandas as pd
import re

# Define the state and years
state_fips = '17'  # FIPS code for Illinois
years = [2014, 2016, 2018, 2022,]  # Years to collect data
acs_survey = 'acs/acs1'  # Use 'acs1' for 1-Year estimates

# Initialize an empty DataFrame to store results
all_data = pd.DataFrame()

# Loop through each year to get data
for year in years:
    # Get ACS data for congressional districts in Illinois
    data = censusdata.download(
        src='acs1',  # Use 'acs1' for 1-Year estimates
        year=year,
        geo=censusdata.censusgeo([('state', state_fips), ('congressional district', '*')]),
        var=[# Population Total
    'B01001_001E',  # Total population
    
    # Immigration and Citizenship
    'B05001_001E',  # Total Population
    'B05001_002E',  # U.S. citizen, born in the United States
    'B05001_003E',  # U.S. citizen, born in Puerto Rico or U.S. Island Areas
    'B05001_004E',  # U.S. citizen, born abroad of American parent(s)
    'B05001_005E',  # U.S. citizen by naturalization
    'B05001_006E',  # Not a U.S. citizen
    
    # Place of Birth
    'B05002_001E',  # Total Population
    'B05002_002E',  # Native
    'B05002_013E',  # Foreign born
    
    # Year of Entry
    'B05005_001E',  # Total Foreign-born population
    'B05005_002E',  # Entered 2010 or later
    'B05005_009E',  # Entered 2000 to 2009
    'B05005_016E',  # Entered before 2000
    
    # Language Spoken at Home
    'B16001_001E',  # Total population 5 years and over
    'B16001_002E',  # Only English
    'B16001_003E',  # Spanish
    'B16001_006E',  # Other Indo-European languages
    'B16001_009E',  # Asian and Pacific Island languages
    'B16001_012E',  # Other languages
    
    # Race and Ethnicity
    'B02001_002E',  # White alone
    'B02001_003E',  # Black or African American alone
    'B02001_004E',  # American Indian and Alaska Native alone
    'B02001_005E',  # Asian alone
    'B02001_006E',  # Native Hawaiian and Other Pacific Islander alone
    'B02001_007E',  # Some other race alone
    'B02001_008E',  # Two or more races
    'B03002_012E',  # Hispanic or Latino (of any race)
    
    # Gender by Age Groups
    # Male
    'B01001_002E',  # Total Male
    'B01001_003E',  # Male: Under 5 years
    'B01001_004E',  # Male: 5 to 9 years
    'B01001_005E',  # Male: 10 to 14 years
    'B01001_006E',  # Male: 15 to 17 years
    'B01001_007E',  # Male: 18 and 19 years
    'B01001_008E',  # Male: 20 years
    'B01001_009E',  # Male: 21 years
    'B01001_010E',  # Male: 22 to 24 years
    'B01001_011E',  # Male: 25 to 29 years
    'B01001_012E',  # Male: 30 to 34 years
    'B01001_013E',  # Male: 35 to 39 years
    'B01001_014E',  # Male: 40 to 44 years
    'B01001_015E',  # Male: 45 to 49 years
    'B01001_016E',  # Male: 50 to 54 years
    'B01001_017E',  # Male: 55 to 59 years
    'B01001_018E',  # Male: 60 and 61 years
    'B01001_019E',  # Male: 62 to 64 years
    'B01001_020E',  # Male: 65 and 66 years
    'B01001_021E',  # Male: 67 to 69 years
    'B01001_022E',  # Male: 70 to 74 years
    'B01001_023E',  # Male: 75 to 79 years
    'B01001_024E',  # Male: 80 to 84 years
    'B01001_025E',  # Male: 85 years and over

    # Female
    'B01001_026E',  # Total Female
    'B01001_027E',  # Female: Under 5 years
    'B01001_028E',  # Female: 5 to 9 years
    'B01001_029E',  # Female: 10 to 14 years
    'B01001_030E',  # Female: 15 to 17 years
    'B01001_031E',  # Female: 18 and 19 years
    'B01001_032E',  # Female: 20 years
    'B01001_033E',  # Female: 21 years
    'B01001_034E',  # Female: 22 to 24 years
    'B01001_035E',  # Female: 25 to 29 years
    'B01001_036E',  # Female: 30 to 34 years
    'B01001_037E',  # Female: 35 to 39 years
    'B01001_038E',  # Female: 40 to 44 years
    'B01001_039E',  # Female: 45 to 49 years
    'B01001_040E',  # Female: 50 to 54 years
    'B01001_041E',  # Female: 55 to 59 years
    'B01001_042E',  # Female: 60 and 61 years
    'B01001_043E',  # Female: 62 to 64 years
    'B01001_044E',  # Female: 65 and 66 years
    'B01001_045E',  # Female: 67 to 69 years
    'B01001_046E',  # Female: 70 to 74 years
    'B01001_047E',  # Female: 75 to 79 years
    'B01001_048E',  # Female: 80 to 84 years
    'B01001_049E',  # Female: 85 years and over

    # Income and Earnings
    'B19013_001E',  # Median household income
    'B19001_001E',  # Total households with income
    'B19001_002E',  # Less than $10,000
    'B19001_003E',  # $10,000 to $14,999
    'B19001_004E',  # $15,000 to $19,999
    'B19001_005E',  # $20,000 to $24,999
    'B19001_006E',  # $25,000 to $29,999
    'B19001_007E',  # $30,000 to $34,999
    'B19001_008E',  # $35,000 to $39,999
    'B19001_009E',  # $40,000 to $44,999
    'B19001_010E',  # $45,000 to $49,999
    'B19001_011E',  # $50,000 to $59,999
    'B19001_012E',  # $60,000 to $74,999
    'B19001_013E',  # $75,000 to $99,999
    'B19001_014E',  # $100,000 to $124,999
    'B19001_015E',  # $125,000 to $149,999
    'B19001_016E',  # $150,000 to $199,999
    'B19001_017E',  # $200,000 or more
    
    # Poverty Status
    'B17001_001E',  # Total population for poverty status
    'B17001_002E',  # Income below poverty level
    
    # Educational Attainment (25 years and over)
    'B15003_001E',  # Total population 25 years and over
    'B15003_002E',  # No schooling completed
    'B15003_003E',  # Nursery school
    'B15003_004E',  # Kindergarten
    'B15003_005E',  # 1st grade
    'B15003_006E',  # 2nd grade
    'B15003_007E',  # 3rd grade
    'B15003_008E',  # 4th grade
    'B15003_009E',  # 5th grade
    'B15003_010E',  # 6th grade
    'B15003_011E',  # 7th grade
    'B15003_012E',  # 8th grade
    'B15003_013E',  # 9th grade
    'B15003_014E',  # 10th grade
    'B15003_015E',  # 11th grade
    'B15003_016E',  # 12th grade, no diploma
    'B15003_017E',  # Regular high school diploma
    'B15003_018E',  # GED or alternative credential
    'B15003_019E',  # Some college, less than 1 year
    'B15003_020E',  # Some college, 1 or more years, no degree
    'B15003_021E',  # Associate's degree
    'B15003_022E',  # Bachelor's degree
    'B15003_023E',  # Master's degree
    'B15003_024E',  # Professional school degree
    'B15003_025E',  # Doctorate degree
    
    # Household Size and Type
    'B11001_001E',  # Total households
    'B11001_002E',  # Family households
    'B11001_003E',  # Married-couple family
    'B11001_004E',  # Other family
    'B11001_005E',  # Nonfamily households
    'B11001_006E',  # Householder living alone
    'B11001_007E',  # Householder not living alone
    
    # Employment Status
    'B23025_002E',  # In labor force
    'B23025_003E',  # Civilian labor force
    'B23025_004E',  # Civilian labor force employed
    'B23025_005E',  # Civilian labor force unemployed
    
    # Housing
    'B25003_001E',  # Total occupied housing units
    'B25003_002E',  # Owner occupied
    'B25003_003E',  # Renter occupied
    
    # Transportation to Work
    'B08301_001E',  # Total workers 16 years and over
    'B08301_002E',  # Car, truck, or van
    'B08301_010E',  # Public transportation
    'B08301_018E',  # Bicycle
    'B08301_019E',  # Walked
    'B08301_021E',  # Worked from home
    
    # Internet Access
    'B28002_001E',  # Total households
    'B28002_002E',  # With an Internet subscription
    'B28002_013E',  # No Internet access
 ]  # Population variables
    )

    # Convert the data to a DataFrame
    df = pd.DataFrame(data).reset_index()

    # Rename columns for clarity
    df.columns = ['District',
    'Total_Population',
    
    # Immigration and Citizenship
    'Total_Pop_Citizenship',
    'US_Born_Citizen',
    'US_Territory_Born_Citizen',
    'US_Born_Abroad_Citizen',
    'Naturalized_Citizen',
    'Non_Citizen',
    
    # Place of Birth
    'Total_Pop_Birth',
    'Native_Born',
    'Foreign_Born',
    
    # Year of Entry
    'Total_Foreign_Born',
    'Entered_2010_Later',
    'Entered_2000_2009',
    'Entered_Before_2000',
    
    # Language
    'Pop_5Years_Over',
    'English_Only',
    'Spanish_Speaker',
    'Indo_European_Lang',
    'Asian_Pacific_Lang',
    'Other_Languages',
    
    # Race and Ethnicity
    'White_Alone',
    'Black_Alone',
    'Native_American_Alone',
    'Asian_Alone',
    'Pacific_Islander_Alone',
    'Other_Race_Alone',
    'Two_Or_More_Races',
    'Hispanic_Latino',
    
    # Male Age Groups
    'Total_Male',
    'Male_Under_5',
    'Male_5_9',
    'Male_10_14',
    'Male_15_17',
    'Male_18_19',
    'Male_20',
    'Male_21',
    'Male_22_24',
    'Male_25_29',
    'Male_30_34',
    'Male_35_39',
    'Male_40_44',
    'Male_45_49',
    'Male_50_54',
    'Male_55_59',
    'Male_60_61',
    'Male_62_64',
    'Male_65_66',
    'Male_67_69',
    'Male_70_74',
    'Male_75_79',
    'Male_80_84',
    'Male_85_Over',
    
    # Female Age Groups
    'Total_Female',
    'Female_Under_5',
    'Female_5_9',
    'Female_10_14',
    'Female_15_17',
    'Female_18_19',
    'Female_20',
    'Female_21',
    'Female_22_24',
    'Female_25_29',
    'Female_30_34',
    'Female_35_39',
    'Female_40_44',
    'Female_45_49',
    'Female_50_54',
    'Female_55_59',
    'Female_60_61',
    'Female_62_64',
    'Female_65_66',
    'Female_67_69',
    'Female_70_74',
    'Female_75_79',
    'Female_80_84',
    'Female_85_Over',
    
    # Income and Earnings
    'Median_Household_Income',
    'Total_Households_Income',
    'Income_Less_10000',
    'Income_10000_14999',
    'Income_15000_19999',
    'Income_20000_24999',
    'Income_25000_29999',
    'Income_30000_34999',
    'Income_35000_39999',
    'Income_40000_44999',
    'Income_45000_49999',
    'Income_50000_59999',
    'Income_60000_74999',
    'Income_75000_99999',
    'Income_100000_124999',
    'Income_125000_149999',
    'Income_150000_199999',
    'Income_200000_Plus',
    
    # Poverty Status
    'Total_Pop_Poverty',
    'Below_Poverty_Level',
    
    # Educational Attainment
    'Pop_25_Over',
    'No_Schooling',
    'Nursery_School',
    'Kindergarten',
    'Grade_1',
    'Grade_2',
    'Grade_3',
    'Grade_4',
    'Grade_5',
    'Grade_6',
    'Grade_7',
    'Grade_8',
    'Grade_9',
    'Grade_10',
    'Grade_11',
    'Grade_12_No_Diploma',
    'High_School_Diploma',
    'GED',
    'Some_College_Less_1yr',
    'Some_College_1yr_Plus',
    'Associates_Degree',
    'Bachelors_Degree',
    'Masters_Degree',
    'Professional_Degree',
    'Doctorate_Degree',
    
    # Household Composition
    'Total_Households',
    'Family_Households',
    'Married_Couple_Family',
    'Other_Family',
    'Nonfamily_Households',
    'Living_Alone',
    'Not_Living_Alone',
    
    # Employment
    'In_Labor_Force',
    'Civilian_Labor_Force',
    'Employed',
    'Unemployed',
    
    # Housing
    'Total_Housing_Units',
    'Owner_Occupied',
    'Renter_Occupied',
    
    # Transportation
    'Workers_16_Over',
    'Commute_Car',
    'Commute_Public_Transit',
    'Commute_Bicycle',
    'Commute_Walk',
    'Work_From_Home',
    
    # Internet Access
    'Total_Households_Internet',
    'Has_Internet',
    'No_Internet'
]
    
    # Add a Year column
    df['Year'] = year
    
    df['Dist_clean'] = df['District'].apply(
    lambda x: int(str(x)[23:25].strip()) if pd.notnull(x) and len(str(x)) >= 24 else None)

    # Append to all_data DataFrame
    all_data = pd.concat([all_data, df], ignore_index=True)

# Save to CSV
all_data.to_csv('il_congressional_districts_acs_2016_2018_2022.csv', index=False)

print("Data saved to il_congressional_districts_acs_2016_2018_2022.csv")

