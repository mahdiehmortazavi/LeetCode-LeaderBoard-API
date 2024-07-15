# LeetCode LeaderBoard

This project demonstrates how to interact with the LeetCode API to fetch user profiles and recent submissions using Python and make an internal LeaderBoard based on LeetCode data. The code is structured to handle authentication, fetch data, and process it into a usable format.

## Features

- Fetch user profile data from LeetCode
- Retrieve recent accepted submissions for multiple users
- Handle and process JSON responses from the LeetCode GraphQL API
- Aggregate and analyze user data

## Internal Leaderboard

Together with my teacher Reza Shokrzad ([rezashokrzad](https://github.com/rezashokrzad)), we created an internal leaderboard for our community, DSLanders. This leaderboard uses LeetCode data to rank users based on their performance in terms of best runtime and memory usage for each LeetCode task. Additionally, users earn extra points for giving presentations about a LeetCode task or related concepts such as Algorithms or Data Structures during the week.

## LeetCode GraphQL API

The project utilizes the GraphQL API from [alfa-leetcode-api](https://github.com/alfa-leetcode-api) user on GitHub to fetch user profile and recent submission data from LeetCode.

## Prerequisites

Before running the code, ensure you have the following installed:

- Python 3.x
- Required Python packages (can be installed via `pip`)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/leetcode-api-project.git
    ```
2. Change to the project directory:
    ```bash
    cd leetcode-api-project
    ```
3. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Set up your API credentials in the `config.py` file:
    ```python
    API_KEY = 'your_api_key'
    ```
2. Run the script to fetch user data:
    ```bash
    python fetch_data.py
    ```

## Examples


Here’s how you can use the project to fetch and display user data:

```python
from leetcode_api import LeetCodeClient

client = LeetCodeClient(api_key='your_api_key')
profile = client.get_user_profile('username')
print(profile)



