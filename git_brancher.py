from jira.ticket_queries import append_branch_names_to_metadata, extract_tickets_metadata_from_query
from jira.query_config import JQL
from vscode.vscode_directories import get_vscode_dir_for_ticket
from datetime import datetime
from dateutil.parser import parse

BRANCHES_CREATED_NAME = "BRANCHES_CREATED.txt"
MAXIMUM_TICKET_STARTED_DELTA = 120

class BranchNameWrapper:
    """Wrapper for interacting with the branch name file"""
    @staticmethod
    def branch_name_in_file(branch_name: str) -> bool:
        """
        Return True if the branch name is in the BRANCHES_CREATED_NAME file
        """
        with open(BRANCHES_CREATED_NAME, "r", encoding="utf-8") as branch_file:
            branches = branch_file.read().split("\n")
            return branch_name in branches

    @staticmethod
    def write_branch_name_to_file(branch_name: str) -> None:
        """
        Write the currently opened branch name to the BRANCHES_CREATED_NAME file
        """
        with open(BRANCHES_CREATED_NAME, "a", encoding="utf-8") as branch_file:
            branch_file.write(f"{branch_name}\n")

def git_brancher():
    """
    Main entrypoint for the git brancher - TODO: Turn this into a CLI tool
    """
    tickets_metadata = extract_tickets_metadata_from_query(JQL)
    append_branch_names_to_metadata(tickets_metadata)
    for _, metadata in tickets_metadata.items():
        branch_name = metadata.get('branch_name')
        ticket_change_date = parse(metadata.get('statusChangeDate'))
        ticket_started_delta = datetime.now(ticket_change_date.tzinfo) - ticket_change_date
        if not BranchNameWrapper.branch_name_in_file(branch_name) and ticket_started_delta.total_seconds() <= MAXIMUM_TICKET_STARTED_DELTA:
            vscode_dir = get_vscode_dir_for_ticket(metadata)
            BranchNameWrapper.write_branch_name_to_file(branch_name)
            print(f"{branch_name}|{vscode_dir}")
            exit(1)

if __name__ == "__main__":
    git_brancher()
