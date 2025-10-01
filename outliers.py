import pandas as pd
import numpy as np
import os
import shutil
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def create_cleaned_directory():
    if os.path.exists('datas_cleaned'):
        shutil.rmtree('datas_cleaned')
    os.makedirs('datas_cleaned')

def detect_and_clean_duplicates(df, is_keeper=False):
    if df.empty:
        return df
    
    if 'Player' not in df.columns:
        return df.drop_duplicates()
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if is_keeper:
        if len(df[df.duplicated(['Player'], keep=False)]) > 0:
            agg_dict = {}
            for col in numeric_cols:
                if col in ['Age', 'Born', 'Rk']:
                    agg_dict[col] = 'first'
                else:
                    agg_dict[col] = 'sum'
            
            for col in df.columns:
                if col not in numeric_cols and col != 'Player':
                    agg_dict[col] = 'first'
            
            df = df.groupby('Player').agg(agg_dict).reset_index()
    else:
        if len(df[df.duplicated(['Player'], keep=False)]) > 0:
            agg_dict = {}
            for col in numeric_cols:
                if col in ['Age', 'Born', 'Rk']:
                    agg_dict[col] = 'first'
                else:
                    agg_dict[col] = 'sum'
            
            for col in df.columns:
                if col not in numeric_cols and col != 'Player':
                    agg_dict[col] = 'first'
            
            df = df.groupby('Player').agg(agg_dict).reset_index()
    
    return df

def identify_outliers(df, method='iqr'):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers_info = {}
    
    for col in numeric_cols:
        if col in ['Age', 'Born', 'Rk']:
            continue
            
        values = df[col].dropna()
        if len(values) == 0:
            continue
            
        if method == 'iqr':
            Q1 = values.quantile(0.25)
            Q3 = values.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = values[(values < lower_bound) | (values > upper_bound)]
        else:
            mean = values.mean()
            std = values.std()
            outliers = values[np.abs(values - mean) > 3 * std]
        
        if len(outliers) > 0:
            outliers_info[col] = len(outliers)
    
    return outliers_info

def clean_outliers(df, method='iqr'):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df_cleaned = df.copy()
    
    for col in numeric_cols:
        if col in ['Age', 'Born', 'Rk']:
            continue
            
        values = df_cleaned[col].dropna()
        if len(values) == 0:
            continue
            
        if method == 'iqr':
            Q1 = values.quantile(0.25)
            Q3 = values.quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            df_cleaned.loc[df_cleaned[col] < lower_bound, col] = lower_bound
            df_cleaned.loc[df_cleaned[col] > upper_bound, col] = upper_bound
        else:
            mean = values.mean()
            std = values.std()
            lower_bound = mean - 3 * std
            upper_bound = mean + 3 * std
            
            df_cleaned.loc[df_cleaned[col] < lower_bound, col] = lower_bound
            df_cleaned.loc[df_cleaned[col] > upper_bound, col] = upper_bound
    
    return df_cleaned

def handle_missing_values(df):
    df_cleaned = df.copy()
    
    for col in df_cleaned.columns:
        missing_pct = df_cleaned[col].isnull().sum() / len(df_cleaned) * 100
        
        if missing_pct > 50:
            df_cleaned = df_cleaned.drop(columns=[col])
        elif df_cleaned[col].dtype in ['object', 'string']:
            df_cleaned[col] = df_cleaned[col].fillna('Unknown')
        else:
            if missing_pct > 0:
                df_cleaned[col] = df_cleaned[col].fillna(df_cleaned[col].median())
    
    return df_cleaned

def create_derived_variables(df, filename):
    df_enhanced = df.copy()
    
    try:
        if 'Born' in df_enhanced.columns:
            current_year = datetime.now().year
            df_enhanced['Calculated_Age'] = current_year - df_enhanced['Born']
        
        if filename == 'top5-players.csv':
            if 'Min' in df_enhanced.columns and 'Gls' in df_enhanced.columns:
                df_enhanced['Goals_per_minute'] = df_enhanced['Gls'] / (df_enhanced['Min'] + 1)
            
            if 'Gls' in df_enhanced.columns and '90s' in df_enhanced.columns:
                df_enhanced['Goals_per_90'] = df_enhanced['Gls'] / (df_enhanced['90s'] + 0.01)
            
            if 'Ast' in df_enhanced.columns and '90s' in df_enhanced.columns:
                df_enhanced['Assists_per_90'] = df_enhanced['Ast'] / (df_enhanced['90s'] + 0.01)
        
        if filename == 'Passing.csv':
            if 'Cmp' in df_enhanced.columns and 'Att' in df_enhanced.columns:
                df_enhanced['Pass_accuracy'] = df_enhanced['Cmp'] / (df_enhanced['Att'] + 1) * 100
        
        if filename == 'Defensive.csv':
            if 'TklW' in df_enhanced.columns and 'Tkl' in df_enhanced.columns:
                df_enhanced['Tackle_success_rate'] = df_enhanced['TklW'] / (df_enhanced['Tkl'] + 1) * 100
        
        if filename == 'keepers.csv':
            if 'Saves' in df_enhanced.columns and 'SoTA' in df_enhanced.columns:
                df_enhanced['Save_percentage'] = df_enhanced['Saves'] / (df_enhanced['SoTA'] + 1) * 100
    except Exception as e:
        print(f"Warning: Could not create all derived variables for {filename}: {e}")
    
    return df_enhanced

def clean_column_names(df):
    df_cleaned = df.copy()
    
    new_columns = []
    for col in df_cleaned.columns:
        if str(col).startswith('Unnamed:'):
            new_columns.append(f'Col_{len(new_columns)}')
        else:
            new_columns.append(str(col).strip())
    
    df_cleaned.columns = new_columns
    
    if 'Col_0' in df_cleaned.columns and df_cleaned['Col_0'].dtype == 'int64':
        df_cleaned = df_cleaned.drop(columns=['Col_0'])
    
    return df_cleaned

def remove_specific_columns(df, filename):
    if filename == 'keepers.csv':
        columns_to_remove = ['Penalty Kicks', 'Col_3', 'Col_11', 'Penalty Kicks.3', 'Col_27']
        existing_columns = [col for col in columns_to_remove if col in df.columns]
        if existing_columns:
            df = df.drop(columns=existing_columns)
    return df

def process_file(filepath, filename):
    try:
        if filename.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        else:
            df = pd.read_csv(filepath)
        
        if df.empty:
            return df
        
        df = clean_column_names(df)
        df = remove_specific_columns(df, filename)
        
        is_keeper = filename == 'keepers.csv'
        df = detect_and_clean_duplicates(df, is_keeper)
        
        outliers_info = identify_outliers(df)
        if outliers_info:
            print(f"✓ {filename} - outliers cleaned")
        
        df = clean_outliers(df)
        df = handle_missing_values(df)
        df = create_derived_variables(df, filename)
        
        return df
        
    except Exception as e:
        print(f"✗ Error: {filename}")
        return pd.DataFrame()

def main():
    try:
        create_cleaned_directory()
        
        data_files = [f for f in os.listdir('datas') if f.endswith(('.csv', '.xlsx'))]
        
        for filename in data_files:
            filepath = os.path.join('datas', filename)
            
            if not os.path.exists(filepath):
                print(f"File {filename} not found, skipping...")
                continue
            
            print(f"Processing {filename}...")
            
            cleaned_df = process_file(filepath, filename)
            
            if not cleaned_df.empty:
                output_path = os.path.join('datas_cleaned', filename)
                
                if filename.endswith('.xlsx'):
                    cleaned_df.to_excel(output_path, index=False)
                else:
                    cleaned_df.to_csv(output_path, index=False)
                
                print(f"✓ {filename} cleaned and saved")
            else:
                print(f"✗ {filename} could not be processed")
        
        print("\nData cleaning completed successfully!")
        print("Cleaned files saved in 'datas_cleaned' directory")
        
    except Exception as e:
        print(f"Error in main process: {e}")

if __name__ == "__main__":
    main()