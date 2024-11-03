import pandas as pd

def combine_district_data(demographics_data, voting_data, output_path='combined_district_data_d.csv'):

    df_demographics = pd.read_csv('combined_district_data.csv')
    df_voting = pd.read_csv('cong_voting.csv')
    
    df_demographics['District'] = df_demographics['Dist_clean'].astype(int)
    
    df_demographics['Year'] = df_demographics['Year'].astype(int)
    df_voting['District'] = df_voting['District'].astype(int)
    df_voting['Year'] = df_voting['Year'].astype(int)
    
    combined_df = pd.merge(
        df_demographics,
        df_voting,
        on=['Year', 'District'],
        how='inner'
    )
    
    # Reorder
    first_cols = ['Year', 'District', 'Winning Party', 'Voter Turnout (%)', 'Votes Blue', 'Votes Red']
    other_cols = [col for col in combined_df.columns if col not in first_cols]
    combined_df = combined_df[first_cols + other_cols]
    
    combined_df.to_csv(output_path, index=False)
    print(f"\nData saved to: {output_path}")
    
    return combined_df

result = combine_district_data('paste.txt', 'cong_voting.csv', 'combined_district_data.csv')

