

from agno.agent import Agent
from agno.db.postgres import PostgresDb
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.groq import Groq
import os
import logging
from dotenv import load_dotenv

load_dotenv()

db_url = "postgresql://postgres:Roost09qGlvWVkZh@db.nfrzzwohegsqvbvqfwhp.supabase.co:5432/postgres"

db = PostgresDb(db_url=db_url)

agent = Agent(
    model=Groq(id="openai/gpt-oss-120b"),
    db=db,
    tools=[DuckDuckGoTools()],
    add_history_to_context=True,
    enable_agentic_memory=True,
)
agent.print_response("How many people live in Canada?")
agent.print_response("What is their national anthem called?")