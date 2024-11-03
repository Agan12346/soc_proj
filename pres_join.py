import pandas as pd

def combine_district_data(demographics_data, voting_data, output_path='combined_district_data_pres.csv'):
    
    df_demographics = pd.read_csv("combined_district_data.csv")
    df_voting = pd.read_csv("pres_data.csv")
    
    #Extract district number
    df_demographics['District'] = df_demographics['Dist_clean'].astype(int)
    
    #Check year and district type
    df_demographics['Year'] = df_demographics['Year'].astype(int)
    df_voting['District'] = df_voting['District'].astype(int)
    
    df_voting = df_voting.rename(columns={
        'D': 'Votes Blue',
        'R': 'Votes Red',
        'Winner': 'Winning Party'
    })
    
    # Merge on year and district
    combined_df = pd.merge(
        df_demographics,
        df_voting,
        on=['Year', 'District'],
        how='inner'
    )
    
    # Reorder
    first_cols = ['Year', 'District', 'Winning Party', 'Votes Blue', 'Votes Red', 'Total']
    other_cols = [col for col in combined_df.columns if col not in first_cols]
    combined_df = combined_df[first_cols + other_cols]
    
    combined_df.to_csv(output_path, index=False)
    print(f"\nData saved to: {output_path}")
    
    return combined_df

try:
    result = combine_district_data('combined_district_data.csv', 'pres_data.csv', 'combined_district_data_pres.csv')   
except Exception as e:
    print(f"An error occurred: {str(e)}")