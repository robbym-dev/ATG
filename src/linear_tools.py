"""
linear_tools.py -
Linear Ticket Management Functions

This script contains functions for interacting with the Linear API to manage tickets,
including fetching teams, retrieving the ID of the 'Todo' workflow state for a team,
and creating tickets in Linear.

Dependencies: requests, GRAPHQL_ENDPOINT, LINEAR_API_KEY from config.py

Functions:
- fetch_teams(): Fetches teams from Linear API. Returns teams' IDs and names.
- get_todo_status_id(team_id): Retrieves the ID of the 'Todo' workflow state for a specified team.
- create_ticket_in_linear(title, description, team_id, priority): Creates a ticket in Linear with the specified details.

"""
import requests
from src.config import GRAPHQL_ENDPOINT, LINEAR_API_KEY


def fetch_teams():
    """
    Fetches teams from Linear API.

    Returns teams' IDs and names.
    """

    # Constructs headers with API key and content type for making a request to the Linear API.
    headers = {
        'Authorization': f'{LINEAR_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Constructs a GraphQL query to fetch teams' IDs and names.
    query = '''
    query {
        teams {
            nodes {
                id
                name
            }
        }
    }
    '''
    try:
        # Sends a POST request to the Linear API with the constructed query and headers.
        response = requests.post(GRAPHQL_ENDPOINT, json={'query': query}, headers=headers)

        response.raise_for_status()  # Check for HTTP errors

        teams_data = response.json()
        
        # Checks if there are any errors in the response.
        if 'errors' in teams_data:
            print("Failed to fetch teams:", teams_data['errors'])
            return None
        
        # Extracts the list of teams' data from the response.
        return teams_data['data']['teams']['nodes']
    
    except requests.exceptions.RequestException as e:
        # Handles network errors.
        print("Network error:", e)
        return None

def get_todo_status_id(team_id):
    """
    Retrieves the ID of the 'Todo' workflow state with 'unstarted' type for a specified team.

    Parameters:
    - team_id (str or int): The ID of the team for which to retrieve the 'Todo' state.

    Returns:
    - str or None: The ID of the 'Todo' state with 'unstarted' type, or None if not found or an error occurs.
    """

    # Constructs headers with API key and content type for making a request to the Linear API.
    headers = {
        'Authorization': f'{LINEAR_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Constructs a GraphQL query to fetch workflow states for a specified team ID.
    query = '''
    query GetStates($teamId: ID!) {
       workflowStates(filter: {team: {id: {eq: $teamId}}}) {
            nodes {
                id
                name
                type
            }
        }
    }
    '''
    variables = {'teamId': team_id}

    # Constructs the payload containing the query and variables.
    payload = {
        'query': query,
        'variables': variables
    }
    try:
        # Sends a POST request to the Linear API with the constructed payload and headers.
        response = requests.post(GRAPHQL_ENDPOINT, json=payload, headers=headers)
        response.raise_for_status()
        states_data = response.json()

        # Checks if there are any errors in the response.
        if 'errors' in states_data:
            print("Failed to fetch statuses:", states_data['errors'])
            return None

        # Iterates through the retrieved states data to find the 'Todo' state with 'unstarted' type.
        for state in states_data.get('data', {}).get('workflowStates', {}).get('nodes', []):
            if state['name'].lower() == 'todo' and state['type'] == 'unstarted':
                return state['id']

        print("No 'Todo' state found for the specified team.")
        return None
    except requests.exceptions.RequestException as err:
        # Handles network errors.
        print(f"Error occurred: {err}")
        print(f"Failed request details: {response.text}")
        return None

def create_ticket_in_linear(title, description, team_id, priority):
    """
    Creates a ticket in Linear with the specified title, description, team ID, and priority.

    Parameters:
    - title (str): The title of the ticket.
    - description (str): The description of the ticket.
    - team_id (str or int): The ID of the team in which to create the ticket.
    - priority (int): The priority level of the ticket (1=Urgent, 2=High, 3=Medium, 4=Low).

    Returns:
    - dict or None: A dictionary containing information about the created ticket, or None if an error occurs.
    """

    # Retrieves the ID of the 'Todo' workflow state for a specified team.
    todo_status_id = get_todo_status_id(team_id)
    if not todo_status_id:
        print("Failed to obtain 'Todo' status ID.")
        return None

    # Constructs headers with API key and content type for making a request to the Linear API.
    headers = {
        'Authorization': f'{LINEAR_API_KEY}',
        'Content-Type': 'application/json'
    }

    # Constructs a GraphQL mutation query to create a new issue in Linear.
    query = '''
    mutation CreateIssue($title: String!, $description: String!, $teamId: String!, $priority: Int, $stateId: String!) {
        issueCreate(input: {title: $title, description: $description, teamId: $teamId, priority: $priority, stateId: $stateId}) {
            issue {
                id
                title
                state {
                    name
                }
            }
        }
    }
    '''

    # Specifies the variables to be used in the GraphQL mutation query.
    variables = {
        'title': title,
        'description': description,
        'teamId': team_id,
        'priority': priority,
        'stateId': todo_status_id  # Use dynamically fetched "Todo" status ID
    }

    # Sends a POST request to the Linear API with the constructed query, variables, and headers.
    response = requests.post('https://api.linear.app/graphql', json={'query': query, 'variables': variables}, headers=headers)

    return response.json()