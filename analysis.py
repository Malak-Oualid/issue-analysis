import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('GITHUB_TOKEN')

from github import Github
g = Github(token)

repo = g.get_repo("apache/doris")

closed_issues = repo.get_issues(state='closed')

print(f"Total closed issues: {closed_issues.totalCount}")
