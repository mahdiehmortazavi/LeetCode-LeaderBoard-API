# KPI & Score Calculation
## prerequisite
#set column of problems to rank users

# Select the specific sheet within the spreadsheet
sheet_name2 = "your sheet name" # Replace with your sheet name
sheet2 = spreadsheet.worksheet(sheet_name2)

# Specify the range to get values from
problem_range_name = "your column range" # Replace with your column range
week_range_name = "your column range" # Replace with your column range
# Get values from the specified range for titles
titles = sheet2.get_values(problem_range_name)
titles = pd.DataFrame(titles)
titles = titles[0].unique()
# Get values from the specified range for weeks
weeks = sheet2.get_values(week_range_name)
weeks = pd.DataFrame(weeks)
weeks = weeks[0].unique()
# From the LeetCode dataset, we want only runtime and memory numbers, so remove any string data associated with it.

# Convert the 'runtime' column to string and then replace ' ms' with ''
df_unique['runtime'] = df_unique['runtime'].astype(str).str.replace(' ms', '')

# Replace non-numeric values such as "N/A" with NaN
df_unique['runtime'] = pd.to_numeric(df_unique['runtime'], errors='coerce')


df_unique['memory'] = df_unique['memory'].astype(str).str.replace(' MB', '').str.replace('B', '')

# Replace non-numeric values such as "N/A" with NaN
df_unique['memory'] = pd.to_numeric(df_unique['memory'], errors='coerce')
## kpi_runtime
# Initialize the dictionary to store minimum runtimes for each title
min_runtimes = {}
min_runtime_user = {}
# Create an empty dictionary to store the KPI for each user
user_kpi = {}

# Filter the DataFrame for rows where the language is python3 and the status is Accepted for each user in each problem.
df_unique = df_unique[(df_unique['lang'] == 'python3') & (df_unique['statusDisplay'] == 'Accepted')]


# Iterate through each title to find the minimum runtime
for title in titles:
    # Filter the DataFrame for rows where the title matches the current title in the loop
    title_data = df_unique[df_unique['title'] == title]

    # Find the minimum runtime for the current title
    if not title_data.empty:
        min_runtime = title_data['runtime'].min()
        # Store the minimum runtime in the dictionary
        min_runtimes[title] = min_runtime

# Group the DataFrame by username and title and find the minimum runtime for each group
for (username, title), group in df_unique.groupby(['username', 'title']):
    #Find the minimum runtime for the current user-title combination
    min_runtime_user[(username, title)] = group['runtime'].min()


# Iterate through each row in the DataFrame to calculate the KPI
for index, row in df_unique.iterrows():
    user = row['username']
    title = row['title']
    runtime = row['runtime']

    # Calculate the KPI for the current user and title
    if title in min_runtimes:
        min_runtime = min_runtimes[title]
        user_title_runtime = min_runtime_user.get((user, title), None)

        if runtime == min_runtime:
            kpi = 1

        elif user_title_runtime is not None:
            kpi = (user_title_runtime - min_runtime) / user_title_runtime
        else:
            kpi = 0  # Default KPI if user_title_runtime is None (shouldn't happen)

        # Store the KPI in the dictionary
        if user not in user_kpi:
            user_kpi[user] = {}
        user_kpi[user][title] = kpi


# Convert the user KPI dictionary into a DataFrame
kpi_runtime = pd.DataFrame(user_kpi).transpose()

# Fill NaN values with 0
kpi_runtime = kpi_runtime.fillna(0)
users = []
titles = []
kpis = []

# Iterate through the user_kpi dictionary to populate lists
for user, kpi_data in user_kpi.items():
    for title, kpi in kpi_data.items():
        users.append(user)
        titles.append(title)
        kpis.append(kpi)

# Create DataFrame from lists
kpi_runtime = pd.DataFrame({
    'User': users,
    'Problem': titles,
    'KPI': kpis
})
kpi_runtime['criteria']='runtime'
## kpi_memory

# Create an empty dictionary to store the memory  for each title
min_memories = {}

# Filter the DataFrame for rows where the language is python3 and the status is Accepted for each user in each problem.
df_unique = df_unique[(df_unique['lang'] == 'python3') & (df_unique['statusDisplay'] == 'Accepted')]


# Iterate through each title to find the minimum memory
for title in titles:
    # Filter the DataFrame for rows where the title matches the current title in the loop
    title_data = df_unique[df_unique['title'] == title]

    # Drop rows with NaN values in the 'memory' column
    title_data = title_data.dropna(subset=['memory'])

    # Find the minimum memory for the current title
    if not title_data.empty:
        min_memory = title_data['memory'].min()
        # Store the minimum memory in the dictionary
        min_memories[title] = min_memory

# Create an empty dictionary to store the minimum memory for each user-title combination
min_memory_user = {}

# Group the DataFrame by username and title and find the minimum memory for each group
for (username, title), group in df_unique.groupby(['username', 'title']):
    # Find the minimum memory for the current user-title combination
    min_memory_user[(username, title)] = group['memory'].min()

# Create an empty dictionary to store the KPI for each user
user_kpi = {}

# Iterate through each row in the DataFrame to calculate the KPI
for index, row in df_unique.iterrows():
    user = row['username']
    title = row['title']
    memory = row['memory']

    # Calculate the KPI for the current user and title
    if title in min_memories:
        min_memory = min_memories[title]
        user_title_memory = min_memory_user.get((user, title), None)

        if memory == min_memory:
            kpi = 1
        elif user_title_memory is not None:
            kpi = (user_title_memory - min_memory) / user_title_memory
        else:
            kpi = 0  # Default KPI if user_title_memory is None (shouldn't happen)

        # Store the KPI in the dictionary
        if user not in user_kpi:
            user_kpi[user] = {}
        user_kpi[user][title] = kpi
# Convert the user KPI dictionary into a DataFrame
kpi_memory = pd.DataFrame(user_kpi).transpose()

# Fill NaN values with 0
kpi_memory = kpi_memory.fillna(0)
users = []
titles = []
kpis = []

# Iterate through the user_kpi dictionary to populate lists
for user, kpi_data in user_kpi.items():
    for title, kpi in kpi_data.items():
        users.append(user)
        titles.append(title)
        kpis.append(kpi)

# Create DataFrame from lists
kpi_memory = pd.DataFrame({
    'User': users,
    'Problem': titles,
    'KPI': kpis
})
kpi_memory['criteria']='memory'
## merge kpi's
# Merge the two DataFrames on the 'title' column
merged_kpi=pd.concat([kpi_memory,kpi_runtime],axis='rows')
merged_kpi.reset_index(drop=True, inplace=True)
## Calculate Score for  each user based on rank in each week
# Open the Google Sheets by name
sheet1 = client.open("your Google Sheet").worksheet("Problem")

# Convert sheet data to DataFrame
data1 = pd.DataFrame(sheet1.get_all_records())

merged_kpi = pd.merge(merged_kpi,
                      data1,
                      on ='Problem',
                      how ='inner')
# Calculate the number of unique tasks per user for each week
unique_weeks_per_user = merged_kpi.groupby(['User','Week No.'])['Task No.'].nunique().reset_index()
# Create a pivot table with the sum of KPI values for each user, week, and criteria
pivot_merged_kpi = merged_kpi.groupby(['Week No.', 'User', 'criteria'])['KPI'].sum().unstack(fill_value=0)
# Reset the index of the pivot table to convert the index into columns
pivot_merged_kpi = pivot_merged_kpi.reset_index() 
# Merge the unique weeks per user with the pivot table on 'User' and 'Week No.' using an outer join
merged_kpi = pd.merge(unique_weeks_per_user, pivot_merged_kpi, on=['User', 'Week No.'], how='outer')
# Calculate the raw score components by summing up the 'Task No.' value, 
# the sigmoid transformation of the 'memory' column, and the sigmoid transformation of the 'runtime' column
raw_score_components = merged_kpi['Task No.'] + \
                       1 / (1 + np.exp(-merged_kpi['memory'])) + \
                       1 / (1 + np.exp(-merged_kpi['runtime']))

# Create a new column 'Raw Score' in the DataFrame to store the calculated raw score
merged_kpi['Raw Score'] = raw_score_components
# Sort by Week No., then by User, and finally by Raw Score within each group
merged_kpi_sorted = merged_kpi.sort_values(by=['Week No.', 'Raw Score'], ascending=[True, False])

# Calculate rank within each week with highest Raw Score receiving rank 1
merged_kpi_sorted['Rank'] = merged_kpi_sorted.groupby('Week No.', sort=False)['Raw Score'].rank(method='min', ascending=False)
# Define a function to calculate the score based on the rank
def calculate_score(rank):
    if rank <= 3:
        return 3
    elif rank <= 10:
        return 2
    elif rank <= 20:
        return 1
    else:
        return 0

# Apply the function to create the 'Rank-Reward Score' column by adding the calculated score to the 'Raw Score'
merged_kpi_sorted['Rank-Reward Score'] = merged_kpi_sorted['Rank'].apply(calculate_score) + merged_kpi_sorted['Raw Score']
## Calculate Score for  each user based on presentation in each week
# Open the Google Sheets by name
sheet2 = client.open("your Google Sheet").worksheet("Problem") #my sheet name is "Problem"
# Convert sheet data to DataFrame
data2 = pd.DataFrame(sheet2.get_all_records())

# Assuming 'User' column is the key for merging
merged_kpi_sorted = merged_kpi_sorted.merge(data2[['User', 'Pres. Score']], on='User', how='left')

# Fill any missing values in the 'Pres. Score' column with 0
merged_kpi_sorted['Pres. Score'] = merged_kpi_sorted['Pres. Score'].fillna(0)

# Function to check if user ID is in the presenters list for the given week
def apply_bonus(user_id, week):
    return user_id in data2[data2['Week No.'] == week]['User'].values

# Apply the function to create the 'Bonus' column. 'Bonus' column shows True if a user has a presentation, otherwise False
merged_kpi_sorted['Bonus'] = merged_kpi_sorted.apply(lambda row: apply_bonus(row['User'], row['Week No.']), axis=1)

# Define a function to apply the score calculation based on bonus
def calculate_score(rank_reward_score, bonus, additional_score):
    return rank_reward_score + additional_score if bonus else rank_reward_score

# Apply the function to create the 'Rank&Presentation-Reward Score' column
merged_kpi_sorted['Rank&Presentation-Reward Score'] = merged_kpi_sorted.apply(
    lambda row: calculate_score(row['Rank-Reward Score'], row['Bonus'], row['Pres. Score']), axis=1
)

# Drop the 'Rank-Reward Score' and 'Pres. Score' columns
merged_kpi_sorted = merged_kpi_sorted.drop(['Rank-Reward Score', 'Pres. Score'], axis=1)

## Transfer to googlesheet
# Convert the transposed DataFrame to a dictionary
data = merged_kpi_sorted.to_dict()

# Select the specific sheet
worksheet_name = "your sheet name"
worksheet = spreadsheet.worksheet(worksheet_name)

# Clear existing content in the sheet
worksheet.clear()

# Update the sheet with the DataFrame's column names and values
worksheet.update([merged_kpi_sorted.columns.tolist()] + merged_kpi_sorted.values.tolist())
