import pandas as pd
import re
import os

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

def process_excel(file_path):
    try:
        print(f"Processing: {file_path}")
        df = pd.read_excel(file_path, dtype=str) # Read as string to preserve leading zeros in ZIPs if any
        
        if 'ZIP' not in df.columns:
            # Try case-insensitive search
            cols = [c for c in df.columns if c.upper() == 'ZIP CODE']
            if cols:
                zip_col = cols[0]
            else:
                return False, "Column 'ZIP Code' not found in the Excel file."
        else:
            zip_col = 'ZIP Code'
            
        # Clean the column
        df[zip_col] = df[zip_col].apply(clean_zipcode)
        
        # Save to a new file
        base, ext = os.path.splitext(file_path)
        output_path = f"{base}_cleaned{ext}"
        
        df.to_excel(output_path, index=False)
        print(f"Saved to: {output_path}")
        return True, output_path
        
    except Exception as e:
        return False, str(e)

def main():
    import tkinter as tk
    from tkinter import filedialog, messagebox

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

    success, message = process_excel(file_path)
    
    if success:
        messagebox.showinfo("Success", f"File processed successfully!\nSaved to: {message}")
    else:
        messagebox.showerror("Error", f"An error occurred:\n{message}")

if __name__ == "__main__":
    main()
