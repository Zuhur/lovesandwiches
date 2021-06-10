import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('lovesandwiches/creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """ 
    Get sales figures input from the user
    """
    while True:
        print(f'Please enter sales data from the last market')
        print(f'Data should be six numbers, separated by commas')
        print(f'Example: 10,20,30,40,50,60\n')

        data_str = input("Enter data here: ")
        sales_data = data_str.split(',')

        if validate_data(sales_data):
            print('data is valid')
            break
        
    return sales_data

def validate_data(values):
    """
    Inside try, converts all strings into integers.
    Raises ValueError if strings cannot be converted into int,
    or if their arent exactly 6 values.
    """
    try:
        [int(i) for i in values]
        if len(values) != 6:
            raise ValueError(f"Exactly 6 values required, you provided {len(values)}")
    except ValueError as e:
        print(f'Invalid data: {e}, please try again. \n')
        return False
    return True


def update_sales_worksheet(data):
    """ 
    Update sales worksheet, add a new row with list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet('sales')
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully")

def calculate_surplus_data():
    """
    Compare sales with stock and calculate the surplus of the day
    Negative surplus = no waste (additional sandwhiches made for customers)
    Positive surplus = waste (everything in the stock not sold)
    """
    print("Calculating surplus data")
    stock = SHEET.worksheet('stock').get_all_values()
    pprint(stock)
    stock_row = stock[0:-1]
    print(stock_row)




def main(): 
    """
    Run all program functions
    """   
    data = get_sales_data()
    sales_data = [int(i) for i in data]
    update_sales_worksheet(sales_data)
    calculate_surplus_data()

main()