# Final Leaderboard 
# Group by 'User' and calculate the sum of 'Rank&Presentation-Reward Score' for each user
user_scores = merged_kpi_sorted.groupby('User')['Rank&Presentation-Reward Score'].sum().reset_index()

# Rank the users based on their 'Rank&Presentation-Reward Score' in descending order, using dense ranking
user_scores['Rank'] = user_scores['Rank&Presentation-Reward Score'].rank(ascending=False, method='dense').astype(int)

# Select only the 'Rank', 'User', and 'Rank&Presentation-Reward Score' columns
user_scores = user_scores[['Rank', 'User', 'Rank&Presentation-Reward Score']]

# Sort the users by their rank
user_scores = user_scores.sort_values(by='Rank')
# Import the set_with_dataframe function from the gspread_dataframe module
# This function is used to write a pandas DataFrame to a Google Sheets worksheet
from gspread_dataframe import set_with_dataframe

# Select the specific sheet
worksheet_name = "your sheet name"
worksheet = spreadsheet.worksheet(worksheet_name)

# Clear existing content in the sheet
worksheet.clear()

# Set DataFrame to the Google Sheet without including the index
set_with_dataframe(worksheet, user_scores, include_index=False)
