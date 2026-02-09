import pandas as pd
import re
import os

import math

def clean_zipcode(value):
    """
    Removes the +4 extension from a zipcode if present.
    Expected format: 12345-6789 -> 12345
    Also handles integers and strings.
    """
    if pd.isna(value):
        return value
    
    str_val = str(value).strip()
    
    # Check for the pattern 12345-6789
    match = re.match(r'^(\d{5})-\d{4}$', str_val)
    if match:
        return match.group(1)
    
    # Also handle if it's just a long string with a hyphen somewhere else, but user asked for -1234 removal specifically.
    # The requirement is "remove the zipcode +4 extension that looks like -1234".
    # So valid zipcodes are 5 digits.
    # If the user has 9 digit zipcodes without hyphen, we might need to handle that too, but let's stick to the prompt: "looks like -1234"
    
    # More robust regex to catch "12345-6789" anywhere? The prompt says "looks like -1234".
    # Let's assume standard US zip codes.
    return str_val.split('-')[0]

def process_excel(file_path, num_files):
    try:
        print(f"Processing: {file_path}")
        df = pd.read_excel(file_path, dtype=str) # Read as string to preserve leading zeros in ZIPs if any
        
        if 'ZIP Code' in df.columns:
            zip_col = 'ZIP Code'
        else:
            cols = [c for c in df.columns if c.upper() == 'ZIP CODE']
            if cols:
                zip_col = cols[0]
            else:
                return False, "Column 'ZIP Code' not found in the Excel file."
            
        # Clean the column
        df[zip_col] = df[zip_col].astype(str).apply(clean_zipcode)
        
        # Calculate padding rows
        total_rows = len(df)
        if num_files > 0:
            rows_per_file = math.ceil(total_rows / num_files)
            target_total = rows_per_file * num_files
            padding_needed = target_total - total_rows
            
            if padding_needed > 0:
                print(f"Adding {padding_needed} padding rows.")
                # Create padding dataframe
                padding_data = {col: [''] * padding_needed for col in df.columns}
                padding_df = pd.DataFrame(padding_data)
                
                # Fill specific columns with dashes
                # First column
                first_col = df.columns[0]
                padding_df[first_col] = '-'
                
                # Top Fold Message
                if "Top Fold Message" not in padding_df.columns:
                    padding_df["Top Fold Message"] = '-'
                    # Also need to add this column to original df if not present, to match concat? 
                    # Actually pd.concat handles column alignment, but good to be consistent.
                    # If the original df doesn't have it, we should probably add it there too or just let concat handle it with NaN (which we can fill)
                else:
                    padding_df["Top Fold Message"] = '-'
                    
                # Bottom Fold Message
                if "Bottom Fold Message" not in padding_df.columns:
                    padding_df["Bottom Fold Message"] = '-'
                else:
                    padding_df["Bottom Fold Message"] = '-'
                
                # Append padding
                df = pd.concat([df, padding_df], ignore_index=True)
                
                # Ensure original df has the new columns if they were created in padding
                if "Top Fold Message" not in df.columns:
                     df["Top Fold Message"] = "" # Or whatever default
                if "Bottom Fold Message" not in df.columns:
                     df["Bottom Fold Message"] = ""

                # Fill NaNs in the new columns for the original rows if they were just created?
                # The user request just said fill dashes for the NEW rows.
                # pd.concat will put NaN for the original rows if column didn't exist.
                # We should probably fill those NaNs with empty string or keep as is.
                # Let's fill NaNs with empty string for cleanliness if we introduced new columns.
                df = df.fillna("")

        # Overwrite the file
        df.to_excel(file_path, index=False)
        print(f"Overwritten: {file_path}")
        return True, file_path
        
    except Exception as e:
        return False, str(e)

def main():
    import tkinter as tk
    from tkinter import filedialog, messagebox, simpledialog

    # Hide the main tkinter window
    root = tk.Tk()
    root.withdraw()
    
    print("Please select an Excel file in the dialog...")
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx")]
    )

    if not file_path:
        print("No file selected.")
        return

    # Ask for number of output files
    num_files = simpledialog.askinteger("Input", "Number of output files you will enter for sign address?")
    
    if num_files is None:
        print("Input cancelled.")
        return

    success, message = process_excel(file_path, num_files)
    
    if success:
        print(f"File processed successfully. (Output files count: {num_files})")
    else:
        messagebox.showerror("Error", f"An error occurred:\n{message}")

if __name__ == "__main__":
    main()
