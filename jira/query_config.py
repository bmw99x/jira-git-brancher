"""
JIRA QUERY CONFIGURABLES
"""

ANY_TASK = '(Bug, "Bug 🐞", Epic, Research, Story, Task, Sub-task, Subtask)'
NON_COMPLETED_STATUSES = '(Backlog, "In Progress", Scope, "Up Next")'
# Put your name here so that only your tickets are picked up
JQL = f'project = ENG AND assignee = "" AND status in {NON_COMPLETED_STATUSES}'

