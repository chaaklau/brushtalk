import pandas as pd
import numpy as np

try:
    df = pd.read_csv('/Users/chaak/brushtalk-davidli/source.csv', header=None, nrows=500)
    
    # Get unique field names from column 2 (index 1)
    # Convert all to strings to avoid mixed types, treating NaN separately
    unique_vals = df[1].unique()
    field_names = [f for f in unique_vals if pd.notna(f)]
    
    token_fields = []
    metadata_fields = []

    for field in field_names:
        # Filter rows for this field
        field_rows = df[df[1] == field]
        
        has_multiple_cols = False
        # Check if there are any columns from index 3 (4th column) onwards
        if field_rows.shape[1] > 3:
            subset = field_rows.iloc[:, 3:]
            # Check if any value is not NaN
            if subset.notna().any().any():
                 has_multiple_cols = True
        
        if has_multiple_cols:
            token_fields.append(field)
        else:
            metadata_fields.append(field)

    print('Token Fields:', sorted(token_fields))
    print('Metadata Fields:', sorted(metadata_fields))
    
    # Check for NaN rows (potential irregularities or empty lines)
    nan_rows = df[df[1].isna()]
    if not nan_rows.empty:
        print(f'Irregularity: {len(nan_rows)} rows found with no field name (NaN in column 2).')
        # Check if they have content in column 3 (index 2) onwards
        if nan_rows.iloc[:, 2:].notna().any().any():
             print('  - These rows contain some data.')
        else:
             print('  - These rows appears to be empty or separators.')
             
except Exception as e:
    print(f"Error: {e}")
