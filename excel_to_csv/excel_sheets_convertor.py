import os
import pandas as pd


def find_xls_files() -> list:
    xls_files = []
    for file in os.listdir():
        if file.endswith('.xls') or file.endswith('.xlsx'):
            xls_files.append(file)
    if not xls_files:
        raise FileNotFoundError("No files with .xls or .xlsx extension found in the folder.")
    return xls_files


def evaluate_engine(file: str) -> str:
    file_extension = os.path.splitext(file)[1]

    if file_extension == '.xlsx':
        engine = 'openpyxl'
    elif file_extension == '.xls':
        engine = 'xlrd'
    else:
        raise ValueError("File format not supported. Must be .xls or .xlsx.")
    
    return engine


def get_xls_active_sheet(xls_file: str) -> list:
    try:
        engine = evaluate_engine(xls_file)
        excel_file = pd.ExcelFile(xls_file, engine=engine)
        sheets_with_content = []
        
        for sheet_name in excel_file.sheet_names:
            df = pd.read_excel(excel_file, sheet_name=sheet_name)
            if not df.empty:
                sheets_with_content.append({
                    'name': sheet_name,
                    'content': df
                })
        
        if not sheets_with_content:
            raise ValueError("Excel file does not contain sheets with data.")
            
        return sheets_with_content
    except Exception as e:
        raise RuntimeError(f"Error reading Excel file: {e}")


def convert_to_csv(xls_file: str, sheets: list) -> None:
    base_name = os.path.splitext(xls_file)[0]
    
    if len(sheets) == 1:
        csv_file = f"{base_name}.csv"
        sheets[0]['content'].to_csv(csv_file, index=False, encoding='utf-8')
        print(f"File converted: {csv_file}")
    if len(sheets) > 1:
        for sheet in sheets:
            sheet_name = sheet['name']
            csv_file = f"{base_name}_{sheet_name}.csv"
            sheet['content'].to_csv(csv_file, index=False, encoding='utf-8')
            print(f"File converted: {csv_file}")


if __name__ == "__main__":
    try:
        xls_files = find_xls_files()
        for xls_file in xls_files:
            print(f"\nProcessing file: {xls_file}")
            xls_sheets = get_xls_active_sheet(xls_file)
            convert_to_csv(xls_file, xls_sheets)
        print("\nProcess completed successfully.")
    except Exception as e:
        print(f"ERROR: {e}")