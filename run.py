import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('grocery_list_generator')

ingredients = SHEET.worksheet('INGREDIENT')
quantities = SHEET.worksheet('QUANTITY')


def generate_dinners_string():
    dinner_names = ingredients.row_values(1)

    dinners_string = ""

    for i in range(len(dinner_names)):
        dinners_string += f"{i + 1} - {dinner_names[i]}\n"

    return dinners_string
