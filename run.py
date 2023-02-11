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

        if validate_csv(dinners_split):
            print("\nInput is valid!\n")
            break

    dinners_int = [int(dinner) for dinner in dinners_split]

    return dinners_int


def validate_csv(csv_input):
    print("Validating input...\n")
    try:
        for value in csv_input:
            int(value)

        if len(csv_input) != 7:
            raise ValueError(
                f"You must enter exactly 7 choices, you entered {len(csv_input)}"
            )

        for value in csv_input:
            if int(value) < 1 or int(value) > len(ingredients.row_values(1)):
                raise ValueError(
                    f"Input must correspond with options listed, {value} is not an option"
                )

    except ValueError as e:
        print(f"Input was not valid: {e}, please try again.\n")
        return False

    return True


def calculate_shopping_list(dinner_picks):

    shopping_list = dict()

    print("Calculating Shopping list...\n")

    for dinner in dinner_picks:

        ing_data = ingredients.col_values(dinner)
        quan_data = quantities.col_values(dinner)

        ing_data.pop(0)
        quan_data.pop(0)

        recipe_dict = dict(zip(ing_data, quan_data))

        for ing, quan in recipe_dict.items():
            if ing in shopping_list:
                shopping_list[ing] = shopping_list.get(ing) + int(quan)
            else:
                shopping_list[ing] = int(quan)

    return shopping_list


def main():
    """
    Run all program fuctions
    """
    dinners_string = generate_dinners_string()
    dinner_picks = get_dinner_picks(dinners_string)
    shopping_list = calculate_shopping_list(dinner_picks)


print("Welcome to my shopping list generator!\n")
main()
