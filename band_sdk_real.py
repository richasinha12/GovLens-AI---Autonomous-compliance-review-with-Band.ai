"""
Official Band.ai SDK integration example.

This file is a template for a Python 3.10/3.11 environment.
It uses the official `band` package and LangGraph adapter.

It supports loading credentials from `agent_config.yaml` or environment variables.
"""

import os
import asyncio
import logging

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from band import Agent
from band.adapters.langgraph import LangGraphAdapter
from band.config import load_agent_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_agent_credentials():
    load_dotenv()
    band_api_key = os.getenv("BAND_API_KEY")
    band_agent_id = os.getenv("BAND_AGENT_ID")
    if band_api_key and band_agent_id:
        return band_agent_id, band_api_key
    return load_agent_config("my_agent")


async def main():
    agent_id, api_key = get_agent_credentials()

    adapter = LangGraphAdapter(
        llm=ChatOpenAI(model="gpt-4o"),
        checkpointer=InMemorySaver(),
        custom_section="You are a helpful compliance review assistant.",
    )

    agent = Agent.create(
        adapter=adapter,
        agent_id=agent_id,
        api_key=api_key,
    )

    logger.info("Agent is running! Press Ctrl+C to stop.")
    await agent.run()


if __name__ == "__main__":
    asyncio.run(main())
