"""
ticket_generation.py - 
Ticket Generation Functions

This script contains functions for generating ticket prompts and calling the OpenAI language model to generate ticket text.

Dependencies: OpenAI library (openai), ticket_few_shot file

Functions:
- generate_prompt(ticket_title): Generates a prompt for the OpenAI language model based on the task title.
- call_language_model(ticket_title): Calls the OpenAI language model to generate ticket text based on the task title.

"""
from openai import OpenAI

def generate_prompt(ticket_title):
    """
    Generates a prompt for the OpenAI language model based on the task title.

    Parameters:
    - ticket_title (str): The title of the task.

    Returns:
    - str: A prompt containing examples and a template filled with the task title.
    """
    
    with open('ticket_few_shot', 'r') as file:
        content = file.read()

    # Split the content into sections
    sections = content.split('---')
    
    examples = sections[:-1]  # All sections except the last one are examples
    template = sections[-1].strip()  # The last section is the template
    
    # Combine examples and the template, replacing the placeholder in the template
    filled_template = template.format(ticket_title=ticket_title)
    full_prompt = '\n---\n'.join(examples) + '\n---\n' + filled_template
    
    return full_prompt



def call_language_model(ticket_title):
    """
    Calls the OpenAI LLM to generate ticket text based on the task title.

    Parameters:
    - task_title (str): The title of the task.

    Returns:
    - str: Generated ticket text.
    """
    client = OpenAI()

    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": generate_prompt(ticket_title)},
        {"role": "user", "content": ticket_title}
    ]
    )
    return completion.choices[0].message.content