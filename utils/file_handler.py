def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues.
    Returns: list of raw lines (strings)
    """
    encodings = ['utf-8', 'latin-1', 'cp1252'] # Required encodings to try 
    
    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file: # Use 'with' statement 
                # Read all lines
                lines = file.readlines()
                
                # Requirements: 
                # 1. Skip the header row (first line)
                # 2. Remove empty lines (strip whitespace and filter)
                data_lines = [line.strip() for line in lines[1:] if line.strip()]
                
                return data_lines
                
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.") # Handle FileNotFoundError 
            return []
        except UnicodeDecodeError:
            # If this encoding fails, the loop continues to the next one
            continue
            
    print("Error: Could not read the file with supported encodings.")
    return []