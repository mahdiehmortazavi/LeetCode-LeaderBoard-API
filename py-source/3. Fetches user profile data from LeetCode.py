def get_user_profile(username):
    """
    Fetches user profile data from LeetCode using the GraphQL API.
    
    Parameters:
    username (str): The username of the LeetCode user.

    Returns:
    dict: The JSON response containing user profile data.
    """


    url = "https://leetcode.com/graphql"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "query": """
        query getUserProfile($username: String!) {
          allQuestionsCount {
            difficulty
            count
          }
          matchedUser(username: $username) {
            contributions {
              points
            }
            profile {
              reputation
              ranking
            }
            submissionCalendar
            submitStats {
              acSubmissionNum {
                difficulty
                count
                submissions
              }
              totalSubmissionNum {
                difficulty
                count
                submissions
              }
            }
          }
        }
        """,
        "variables": {
            "username": username
        }
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch user profile for {username}. Status code: {response.status_code}")
        return None

def color_rows(row, user_colors):
    """
    Applies background color to DataFrame rows based on username.

    Parameters:
    row (pd.Series): The DataFrame row.
    user_colors (dict): A dictionary mapping usernames to colors.

    Returns:
    list: A list of background color styles for the row.
    """

    color = user_colors[row['username']]
    return ['background-color: {}'.format(color) for _ in row]



all_users_data = []

# Loop through the list of usernames to fetch their profiles and aggregate the data
for username in usernames:
    try:
        user_profile = get_user_profile(username)
        if user_profile and 'data' in user_profile and 'matchedUser' in user_profile['data']:
            data = user_profile['data']
            matched_user = data['matchedUser']
            ac_submission_num = matched_user['submitStats']['acSubmissionNum']
            total_submission_num = matched_user['submitStats']['totalSubmissionNum']

            # Extracting relevant data into a list of dictionaries
            for ac_entry, total_entry in zip(ac_submission_num, total_submission_num):
                all_users_data.append({
                    'username': username,
                    'difficulty': ac_entry['difficulty'],
                    'ac_count': ac_entry['count'],
                    'ac_submissions': ac_entry['submissions'],
                    'total_count': total_entry['count'],
                    'total_submissions': total_entry['submissions'],
                    'points': matched_user['contributions']['points'],
                    'reputation': matched_user['profile']['reputation'],
                    'ranking': matched_user['profile']['ranking'],

                })
        else:
            print(f"No data available for {username}")
    except Exception as e:
        print(f"An error occurred for {username}: {e}")

# Create DataFrame
df_all_users_data = pd.DataFrame(all_users_data)

# Assign a random color to each username
user_colors = {username: "#%06x" % random.randint(0, 0xFFFFFF) for username in usernames}

# Function to convert profile_link column to clickable link with username as link name
def make_clickable(row):
    username = row['username']
    link_name = f"{username}'s Profile"
    profile_link = f"https://leetcode.com/{username}"
    return profile_link

# Apply the clickable link formatting
df_all_users_data['profile_link'] = df_all_users_data.apply(make_clickable, axis=1)

# Apply the styling function
df_all_users_data_styled = df_all_users_data.style.apply(lambda row: color_rows(row, user_colors), axis=1)
