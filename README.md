# Autonomous Ticket Generator (ATG) for Linear!

The Autnomous Ticket Generator (ATG) is a Python script that allows users to make issues in Linear, a modern issue tracking tool, right from the command line. It gives users options for picking out their issue's priority level and team it will be assigned to. The program can also create good-scoped issue descriptions on its own using a Language Model.

## How it Works

### Linear Integration

The script integrates with Linear's GraphQL API to fetch teams and create issues. It uses API calls to fetch a list of teams available in the workspace and allows users to select a team from the list. Once a team is selected, the user can input the task title and priority of the issue.

### User Input

Users are prompted to enter the task title, ensuring that it is at least 4 characters long. They are then asked to select the priority level of the issue from the following options:

1. Urgent
2. High
3. Medium
4. Low

### Issue Creation

Once the user provides the necessary information, the script generates a detailed issue description using a Language Model (LLM) and submits the well-scoped issue to Linear with the specified priority and team assignment.

## Language Model (LLM)

The Language Model (LLM) utilized in this project is GPT3.5. To generate high-quality tickets, it is always few-shot prompted with high-quality [ticket examples](https://github.com/robbym-dev/ATG/blob/main/ticket_few_shot) to ensure accurate and well-scoped ticket generation.

### Ticket Generation

The LLM understands the context of issue creation and is few-shot prompted to generate well-scoped issue descriptions based on the provided task title. It takes into account various factors such as project context, task details, and other tickets to produce comprehensive and actionable issue descriptions; ensuring there is little to no room for ambiguity with the ticket details.

## Installation

To use the Linear Ticket Creator, follow these steps:

1. Clone the repository to your local machine.
```python 
git clone https://github.com/robbym-dev/ATG.git
```
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Initialize OpenAI and Linear API Key with the following command: 
```python
export OPENAI_API_KEY=<your key here>
export LINEAR_API_KEY=<your key here>
```
4. Run the `main.py` script using `python main.py` and follow the on-screen instructions to create an issue.

## Conclusion

ATG provides a seamless way to create well-scoped issues in Linear directly from the command line. With its integration with Linear's API and the power of the Language Model, users can efficiently create detailed and actionable tickets with minimal effort.
