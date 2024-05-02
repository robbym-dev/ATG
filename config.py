"""
Linear API Configuration

This script contains configuration settings for interacting with the Linear API.

Dependencies: os module

Configuration Settings:
- GRAPHQL_ENDPOINT (str): The endpoint URL for the Linear API's GraphQL interface.
- LINEAR_API_KEY (str): The API key required for authorization, obtained from environment variables.

"""

import os

# Configuration Settings
GRAPHQL_ENDPOINT = 'https://api.linear.app/graphql'
LINEAR_API_KEY = os.environ["LINEAR_API_KEY"]