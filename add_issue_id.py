#!/usr/bin/env python

# add-issue-id-hook version 1.1.0
#
# Created by Piotr Betkier
# https://github.com/pbetkier/add-issue-id-hook

# customize the final commit message using placeholders:
#  - {issue_id} replaced with discovered issue id
#  - {user_message} replaced with message provided by the user
commit_message_format = '{user_message} {issue_id}'

# you may set this to your custom JIRA project key format
# or explicitly specify a single project name, e.g. 'EXAMPLE'
project_format = '[A-Z]+'  

# if not using JIRA, set this to your ticket system's issue pattern
issue_pattern = '{}-[\d]+'.format(project_format)


import subprocess
import sys
import re
from typing import List

def read_current_message(args: List[str]):
    with open(args[1], 'r') as f:
        return f.read()

def write_message(args: List[str], message):
    with open(args[1], 'w') as f:
        f.write(message)

def contains_message(message):
    return message and not message.isspace()

def remove_editor_help_message(message):
    return message[:message.find("# Please enter the commit message for your changes.")].rstrip()

def read_branch_or_exit():
    try:
        current_ref = subprocess.check_output('git symbolic-ref HEAD', shell=True).decode()
        return current_ref[len('refs/heads/'):]
    except subprocess.CalledProcessError:
        print("add-issue-id-hook: Adding issue id failed. Are you in detached HEAD state?")
        sys.exit()

def main(argv: List[str] = sys.argv) -> int:
    issue_id_match = re.search(issue_pattern, read_branch_or_exit())
    if issue_id_match:
        found_issue_id = issue_id_match.group()
        user_message = remove_editor_help_message(read_current_message(argv))

        if contains_message(user_message) and found_issue_id not in user_message:
            write_message(argv, commit_message_format.format(issue_id=found_issue_id, user_message=user_message))

if __name__ == "__main__":
    main()
