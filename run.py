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

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus of the day
    Negative surplus = no waste (additional sandwhiches made for customers)
    Positive surplus = waste (everything in the stock not sold)
    """
    print("Calculating surplus data")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = [int(i) for i in stock[-1]]
    surplus_data = [(x-y) for x,y in zip(stock_row,sales_row)]

    return surplus_data

def update_worksheet(data, name):
    """ 
    Update worksheet, add a new row with list data provided
    """
    print(f"Updating {name} worksheet...\n")
    worksheet = SHEET.worksheet(name)
    worksheet.append_row(data)
    print(f"{name} worksheet updated successfully")

def get_last_5_entries_sales():
    """
    Colects columns of data from sales worksheet,
    collecting the last 5 enteries for each sandwich and returns 
    the data as a list of lists
    """ 
    sales = SHEET.worksheet('sales')
    #columns = sales.col_values()
    columns = []
    for i in range(1,7):
        columns.append(sales.col_values(i)[-5:])
    pprint(columns)
    

def main(): 
    """
    Run all program functions
    """   
    data = get_sales_data()
    sales_data = [int(i) for i in data]
    update_worksheet(sales_data, 'sales')
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, 'surplus')

get_last_5_entries_sales()
#main()