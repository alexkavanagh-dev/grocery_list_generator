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


def get_dinner_picks(dinners_string):
    while True:
        print("Please use the corresponding numbers to select your dinners for the next 7 days")
        print("Your input must be seven numbers seperated by commas.\n")
        print("Example input: 1,2,3,4,5,6,7\n")
        print(dinners_string)

        dinners_input = input('Enter selections here:')

        dinners_split = dinners_input.split(',')

    dinners_int = [int(dinner) for dinner in dinners_split]

    return dinners_int


def main():
    """
    Run all program fuctions
    """
    dinners_string = generate_dinners_string()
    dinner_picks = get_dinner_picks(dinners_string)


print("Welcome to my shopping list generator!\n")
main()
