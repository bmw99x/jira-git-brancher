# Define regexes which will determine if there is a corresponding
# vscode directory from which we can open with bash command code .
# Note: (?i) means case insensitive, so .*(?i)test.* matches
# any sprint or epic name with test, tEsT, TEST with any suffix, prefix.
from typing import Dict, List, Tuple
from re import match

VSCODE_PATTERN_MAPPING: List[Tuple[List, str]] = [
	# Define your pattern maps here: Epic name, Sprint name, Label Name
]
UNMATCHED_TICKET_EXC_MSG = (
	"No regex patterns match the epic name or sprint name for a ticket.",
	"Please configure vscode_directories.py to contain a valid mapping for your ticket."
)

def get_vscode_dir_for_ticket(ticket: Dict[str, str]) -> str:
	"""
	Get the vscode directory which is mapped for a particular
	regex pattern which could match an epic name and sprint name
	in the ticket dict
	"""
	epic_name = ticket.get("epic") or ""
	sprint_name = ticket.get("sprint") or ""
	labels = ticket.get("labels") or ""
	for patterns, vscode_dir in VSCODE_PATTERN_MAPPING:
		for pattern in patterns:
			epic_match = match(pattern, epic_name)
			sprint_match = match(pattern, sprint_name)
			label_match = any([match(pattern, label) for label in labels])
			if epic_match or sprint_match or label_match:
				return vscode_dir
	raise Exception(UNMATCHED_TICKET_EXC_MSG)
