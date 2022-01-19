from jira.auth.api_config import jira_client
from collections import defaultdict
from typing import DefaultDict

SPRINT_FIELD = "customfield_10021"
EPIC_FIELD = "customfield_10022"

def _filter_bad_symbols(str_to_filter) -> bool:
    """Return symbols which should be filtered out."""
    bad_symbols = ["-", "(", ")", "[", "]", ":"]
    return True if str_to_filter not in bad_symbols else False

def _filter_bad_characters(str_to_filter) -> bool:
    """Return characters which should be filtered out."""
    # Although we use c to represent chars, they are technically strings
    passes_filter = all([c.isalpha() or c.isnumeric() or c == '.' for c in str_to_filter])
    return passes_filter

def get_epic_name(ticket_number: str) -> str:
    """
    Get the name/summary of the ticket which is an epic
    """
    if not ticket_number:
        return ""
    ticket = jira_client.search_issues(f"key = '{ticket_number}'")[0]
    return ticket.raw["fields"]["summary"]


def extract_tickets_metadata_from_query(jql: str) -> DefaultDict:
    """
    Given a JQL query, search for tickets relating to that
    query and return a dictionary containing metadata relating to the tickets.
    """
    tickets = jira_client.search_issues(jql)
    tickets_metadata = defaultdict(dict)
    sprint_name = None
    for ticket in tickets:
        raw = ticket.raw["fields"]
        status = raw.get("status")
        sprint = raw.get(SPRINT_FIELD)
        epic_ticket_number = raw.get(EPIC_FIELD)
        if sprint and isinstance(sprint, list):
            sprint_name = sprint[0].get("name")
        tickets_metadata[ticket.key] = {
                "issuetype": raw.get("issuetype").get("name").lower(),
                "status": status.get("name") if status else "N/A",
                "statusChangeDate": raw.get("statuscategorychangedate"),
                "summary": raw.get("summary"),
                "sprint": sprint_name,
                "epic": get_epic_name(epic_ticket_number),
                "labels": raw.get("labels"),
        }
    return tickets_metadata

def append_branch_names_to_metadata(tickets_metadata) -> None:
    """
    Given a tickets metadata defaultdict, append new branch names
    for each issue that can be validly turned into a git branch.
    """
    for ticket_number, metadata in tickets_metadata.items():
        ticket_type = metadata.get("issuetype")
        if ticket_type == "investigation":
            continue        
        uncleaned_words = list(filter(_filter_bad_symbols, metadata["summary"].strip().replace('/', '').split(" ")))
        cleaned_words = list(filter(_filter_bad_characters, uncleaned_words))
        new_branch_summary = "_".join([word.lower() for word in cleaned_words])
        # Avoid creating branches for investigation tickets
        new_branch_name = f"{ticket_type}/{new_branch_summary}/{ticket_number}"
        tickets_metadata[ticket_number]["branch_name"] = new_branch_name

