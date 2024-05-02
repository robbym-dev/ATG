from linear_tools import fetch_teams, create_ticket_in_linear
from ticket_generation import call_language_model

def select_team(teams):
    """
    Facilitates the selection of a team from a provided list of teams.

    Parameters:
    - teams (list): A list of dictionaries representing teams, where each dictionary contains 'name' and 'id' keys representing the name and ID of the team respectively.

    Returns:
    - int or None: The ID of the selected team. Returns None if input is invalid.
    """
    for idx, team in enumerate(teams, 1):
        print(f"{idx}. {team['name']} (ID: {team['id']})")
    try:
        choice = int(input("Select a team to create the issue in (enter number): "))
        if choice < 1 or choice > len(teams):
            raise IndexError("Selected team number out of range.")
        return teams[choice - 1]['id']  # returns the chosen team's ID
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return None
    except IndexError as e:
        print(e)
        return None

def main():
    """
    Pulls together program and conducts ticket creation in Linear.

    Fetches teams, prompts for selection.
    Validates inputs, generates ticket text.
    Attempts to create ticket, prints result.
    """
    
    print("Fetching teams...")
    teams = fetch_teams()
    if not teams:
        print("Could not fetch teams or no teams available.")
        return

    team_id = select_team(teams)
    if not team_id:
        return  # Exit if no valid team has been selected

    ticket_title = input("Enter the task title: ")
    if len(ticket_title) < 4:
        print("Task title must be at least 4 characters long.")
        return

    try:
        priority = int(input("Enter the priority (1=Urgent, 2=High, 3=Medium, 4=Low): "))
        if priority not in [1, 2, 3, 4]:
            print("Invalid priority level. Please enter a valid number (1-4).")
            return
    except ValueError:
        print("Invalid input. Please enter a number for the priority.")
        return

    ticket_text = call_language_model(ticket_title)
    if not ticket_text:
        print("Failed to generate ticket text.")
        return

    linear_response = create_ticket_in_linear(ticket_title, ticket_text, team_id, priority)
    if 'errors' in linear_response:
        print(f"Failed to create ticket: {linear_response['errors']}")
    else:
        print("Ticket created in Linear")

if __name__ == "__main__":
    main()