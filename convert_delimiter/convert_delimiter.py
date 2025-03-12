from os import listdir
from csv import Sniffer


PREV_DELIMITER = ','
NEW_DELIMITER = ';'
QUOTE_CHAR = '"'
FOLDER = './'


def get_CSV_files()->list[str]:
    '''
    search in the same folder of this script for all the csv files
    store the name of these files in the variable files and return this list
    '''
    try:
        all_files = listdir(FOLDER)
        return [filename for filename in all_files if filename.endswith('.csv')]
    except Exception as e:
        raise OSError(f"Error obtaining CSV files: {str(e)}")


def detect_delimiter(file_path: str) -> str:
    '''
    Detects the delimiter used in the CSV file
    '''
    with open(file_path, 'r') as file:
        sample = ''.join(file.readline() for _ in range(1))
        if not sample:
            raise ValueError("The file is empty")
            
        try:
            return Sniffer().sniff(sample).delimiter
        except Exception as e:
            raise ValueError(f"Error detecting delimiter: {str(e)}")


def check_delimiter(delimiter: str) -> None:
    '''
    Check if the delimiter is the new one
    Args:
        delimiter (str): the delimiter to check
    Returns:
        None
    '''
    if delimiter == NEW_DELIMITER:
        raise ValueError("The file already uses the new delimiter")


def convert_delimiter(filename: str) -> list:
    '''
    Convert the delimiter of the CSV file
    Args:
        filename (str): the name of the file to convert
    Returns:
        newContent (list): the content of the file with the new delimiter
    '''
    try:    
        with open(filename, 'r') as file:
            lines = file.readlines()

            newContent = []
            for line in lines:
                row = line.strip().split(PREV_DELIMITER)
                newRow = map(parse_cell, row)
                newContent.append(NEW_DELIMITER.join(newRow))
        return newContent
    except FileNotFoundError:
        print('FILE NOT FOUND. CHECK FILE NAME')


def parse_cell(cell: str) -> str:
    '''
    If cell have coma inside, csv will generate missfunctions.
    This function wrap that cell. P.ex "cell"
    Args:
        cell (str): initial content of a cell
    Returns:
        cell (str): same content wraped with "" to aboid missfuntionalities 
    '''
    try:
        if NEW_DELIMITER in cell or PREV_DELIMITER in cell or QUOTE_CHAR in cell:
            cell = (QUOTE_CHAR + cell.replace(QUOTE_CHAR,
                    QUOTE_CHAR+QUOTE_CHAR) + QUOTE_CHAR)
        return cell
    except:
        print('ERROR: Could not parse cell')


def refill_CSV(file: str, content: list) -> None:
    '''
    generates or regenerates the File Document with the content
    Args:
        content (list): the content to fill the document
    Use of Global variables:
        FILENAME (str): the name of the file to extract data and refill
    Returns:
        None
    '''

    try:
        with open(file, 'w') as file:
            file.write('\n'.join(content))
    except:
        print('ERROR: Could not write the file')


if __name__ == '__main__':
    try:
        CSV_files = get_CSV_files()
        for file in CSV_files:
            current_delimiter = detect_delimiter(file_path=file)
            check_delimiter(delimiter=current_delimiter)
            
            new_content = convert_delimiter(filename=file)
            refill_CSV(file, new_content)
            print(f'Delimiters of {file} successfully changed')
    except Exception as e:
        print(f'Error: {e}')
