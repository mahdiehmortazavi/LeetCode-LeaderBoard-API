# Set up the credentials and the Google Sheets API client
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('path of your credentials Google Sheet', scope)
client = gspread.authorize(creds)

# Open the Google Sheet by its name or URL
spreadsheet_name = "your Google Sheet"
spreadsheet = client.open(spreadsheet_name)

# Select the specific sheet within the spreadsheet
sheet_name = "your sheet name"  # Replace with your sheet name
sheet = spreadsheet.worksheet(sheet_name)

# Get the data from a specific column (e.g., column "A")
column_letter = "your desired column letter"  # Replace with the desired column letter
column_data = sheet.col_values(gspread.utils.a1_to_rowcol(f"{column_letter}1")[1])

# Convert the column data to a pandas DataFrame
df_column_data = pd.DataFrame(column_data, columns=[column_letter])

# Extract the data from the specified column in the DataFrame and convert it to a list
usernames = df_column_data['your desired column letter'].tolist()
