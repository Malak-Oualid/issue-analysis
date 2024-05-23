import os
import time
from dotenv import load_dotenv
import pandas as pd
from github import Github
from github.GithubException import RateLimitExceededException
import matplotlib.pyplot as plt
import socket

# Load environment variables from .env file
load_dotenv()
token = os.getenv('GITHUB_TOKEN')

# Use the token to authenticate with GitHub
g = Github(token)

# Access the Apache Doris repository
repo = g.get_repo("apache/doris")

# Function to handle rate limiting
def handle_rate_limiting():
    rate_limit = g.get_rate_limit().core
    if rate_limit.remaining == 0:
        reset_timestamp = rate_limit.reset.timestamp()
        sleep_time = max(reset_timestamp - time.time(), 0)
        print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
        time.sleep(sleep_time + 5)  # Add a buffer of 5 seconds

# Get all closed issues with rate limit handling and pagination
closed_issues = []
page = 0

while True:
    try:
        issues_page = repo.get_issues(state='closed').get_page(page)
        if not issues_page:
            break
        closed_issues.extend(issues_page)
        page += 1
        
        if len(closed_issues) % 100 == 0:  # Check rate limit every 100 issues
            handle_rate_limiting()
    except RateLimitExceededException:
        print("Rate limit exceeded while fetching issues. Handling rate limit.")
        handle_rate_limiting()
        continue  # Retry fetching the current page after handling rate limit
    except socket.error as e:
        print(f"Network error: {e}. Retrying...")
        time.sleep(5)
        continue  # Retry fetching the current page after a network error

print(f"Total closed issues: {len(closed_issues)}")

issue_submitters = {}

for issue in closed_issues:
    submitter = issue.user.login
    if submitter in issue_submitters:
        issue_submitters[submitter] += 1
    else:
        issue_submitters[submitter] = 1

sorted_submitters = sorted(issue_submitters.items(), key=lambda x: x[1], reverse=True)
print(sorted_submitters)

# Create a DataFrame to hold issue data
data = []

for issue in closed_issues:
    submitter = issue.user.login
    created_at = issue.created_at
    data.append({'submitter': submitter, 'created_at': created_at})

df = pd.DataFrame(data)
df['created_at'] = pd.to_datetime(df['created_at'])
df['month'] = df['created_at'].dt.to_period('M')

# Calculate the number of issues per submitter per month
submitter_monthly = df.groupby(['submitter', 'month']).size().unstack(fill_value=0)

# Calculate the average issues per month
submitter_avg_monthly = submitter_monthly.mean(axis=1).sort_values(ascending=False)

print(submitter_avg_monthly)

# Total submissions plot
plt.figure(figsize=(10, 5))
plt.bar(*zip(*sorted_submitters[:10]))  # Top 10 submitters
plt.xticks(rotation=45)
plt.xlabel('Submitter')
plt.ylabel('Total Submissions')
plt.title('Top 10 Submitters by Total Submissions')
plt.show()

# Average submissions per month plot
submitter_avg_monthly[:10].plot(kind='bar', figsize=(10, 5))
plt.xticks(rotation=45)
plt.xlabel('Submitter')
plt.ylabel('Average Submissions per Month')
plt.title('Top 10 Submitters by Average Submissions per Month')
plt.show()
