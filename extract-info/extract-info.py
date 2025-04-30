import pandas as pd

def extract_info_from_csv(file_path):
    """
    Extracts information from a CSV file and returns it as a DataFrame.
    
    Args:
        file_path (str): The path to the CSV file.
        
    Returns:
        pd.DataFrame: A DataFrame containing the extracted information.
    """
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path)
        
        # Perform any necessary data processing here
        # For example, you might want to filter or transform the data
        
        return df
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return None
    
def main(): 
    # Example usage
    file_path = 'Graderingsmiddag eller Gravöl.csv'
    df = extract_info_from_csv(file_path)
    df = df["Användarnamn"]
    df.to_csv("Användarnamn.csv", index=False)
    
        
if __name__ == "__main__":
    main()  