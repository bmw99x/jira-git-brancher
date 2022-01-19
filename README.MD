# JIRA Git brancher

## What is the JIRA Git Brancher?

The JIRA Git Brancher is a plugin for JIRA that automatically creates a new branch in your Git repository based on the JIRA issue key.
It then checks out that branch and launches VS Code and the appropriate git repository in a directory configured by the user.

For now, it is run from the command line.

## **Requirements**

To install the requirements for the project, run: pip install -r requirements.txt, preferably in a virtual environment.

## **Instructions**

1. Install the requirements as outlined above.
2. Activate the virtual environment that the requirements were installed in
3. Obtain an API token from your JIRA workspace and configure jira/auth/api_config.py to have your credentials.
4. Configure the VSCODE_PATTERN_MAPPING list in vscode/vscode_directories.py to contain a pattern
   mapping which will be used to determine the VSCode directory to use for a given JIRA project.
5. Run scripts/end_to_end_flow.sh via command line.
