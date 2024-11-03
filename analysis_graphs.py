import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def clean_numeric_string(value):
    if isinstance(value, str):
        #Clean
        cleaned = value.replace(',', '').replace('(', '').replace(')', '').replace('+/-', '').strip()
        try:
            return float(cleaned)
        except ValueError:
            return None
    return value

def process_csv(data):
    processed_data = []
    
    for _, row in data.iterrows():
        subject = row['Subject']
        title = row['Title']
        
        # Extract district estimates
        for i in range(1, 18):
            district_col = f'District {i:02d} Estimate'
            if district_col in row:
                value = clean_numeric_string(row[district_col])
                if value is not None:
                    processed_data.append({
                        'Subject': subject,
                        'Title': title,
                        'District': f'District {i:02d}',
                        'Value': value
                    })
                
    return pd.DataFrame(processed_data)

def create_visualizations(df):
    # Get unique subjects and districts
    subjects = df['Subject'].unique()
    districts = sorted(df['District'].unique())
    
    #Plot each subj
    for subject in subjects:
        if subject == "Total Population":
            continue

        subject_data = df[df['Subject'] == subject]
        
        #Rows and columns for subplots
        n_plots = len(districts)
        n_cols = 2  # You can adjust this
        n_rows = (n_plots + n_cols - 1) // n_cols
        
        # Create plot
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 5*n_rows))
        fig.suptitle(f'{subject} by District', fontsize=16, y=1.02)
        
        # Handle case where there's only one row
        if n_rows == 1 and n_cols == 1:
            axes = np.array([[axes]])
        elif n_rows == 1:
            axes = np.array([axes])
        
        # Bar plot for each district
        for idx, district in enumerate(districts):
            row = idx // n_cols
            col = idx % n_cols
            
            district_data = subject_data[subject_data['District'] == district]
            
            # Create bar plot
            bars = axes[row, col].bar(range(len(district_data)), district_data['Value'], color='skyblue')
            axes[row, col].set_title(f'{district}', pad=10, fontsize=12)
            
            #x-axis labels
            axes[row, col].set_xticks(range(len(district_data)))
            axes[row, col].set_xticklabels(district_data['Title'], rotation=45, ha='right')
            plt.setp(axes[row, col].xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            axes[row, col].set_xlabel('')
            axes[row, col].set_ylabel('Population', fontsize=10)
            
            # Format y-axis with comma separator for thousands
            axes[row, col].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                axes[row, col].text(bar.get_x() + bar.get_width()/2., height,
                                  f'{int(height):,}',
                                  ha='center', va='bottom', fontsize=8)
            
            # Add grid
            axes[row, col].grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Remove empty subplots if any
        for idx in range(len(districts), n_rows * n_cols):
            row = idx // n_cols
            col = idx % n_cols
            if col < axes.shape[1]:  # Check if the column exists
                fig.delaxes(axes[row, col])
        
        # Adjust layout
        plt.tight_layout()
        plt.savefig(f'{subject.lower().replace(" ", "_")}_by_district_analysis.png', 
                   bbox_inches='tight', dpi=300)
        plt.close()


def main():
    try:
        print("Reading CSV file...")
        data = pd.read_csv('Illinois_District_all.csv', dtype=str)  # Force string reading

        print("Processing data...")
        processed_df = process_csv(data)
        
        if processed_df.empty:
            print("Error: No data")
            return
        
        create_visualizations(processed_df)

        for subject in processed_df['Subject'].unique():
            print(f"- {subject}")
        
    except FileNotFoundError:
        print("Error: Could not find")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()