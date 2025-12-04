import gspread
import pandas as pd

# Load credentials from the JSON file*
gc = gspread.service_account(filename="psyched-bruin-478121-a6-2451b3b9fcb1.json")  # Replace with your JSON file path# Open the Google Sheet by its name*
sh = gc.open("Streamlit_Offers_Log")  # Replace with your sheet’s exact name# Select a worksheet (e.g., "Sheet1")*
worksheet = sh.worksheet("Sheet1")  # Replace with your worksheet name# Fetch all data from the worksheet*
data = worksheet.get_all_records()

# Convert the data into a pandas DataFrame*
df = pd.DataFrame(data)

# Display the DataFrame*
print(df)

worksheet.append_row(["John Doe", 25, "Engineer"])  # Add a new row to the sheet*
