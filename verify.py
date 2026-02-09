from main import process_excel
import pandas as pd
import os

# Create test data
import create_test_data

# Run processing
input_file = 'test_data.xlsx'
success, output_file = process_excel(input_file)

if success:
    print(f"Processing successful: {output_file}")
    
    # Verify content
    df = pd.read_excel(output_file, dtype=str)
    print("Output DataFrame:")
    print(df)
    
    zips = df['ZIP'].tolist()
    expected = ['12345', '12345', '98765', '12345']
    
    # Clean up for float conversion or string inconsistencies
    cleaned_zips = [str(z).replace('.0', '') for z in zips] 
    
    if cleaned_zips == expected:
        print("VERIFICATION PASSED: ZIP codes match expected values.")
    else:
        print(f"VERIFICATION FAILED: Expected {expected}, got {cleaned_zips}")
else:
    print(f"Processing failed: {output_file}")
