# trip_agents.py
from crewai import Agent
from langchain_community.llms import OpenAI

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools

class TripAgents():
    def city_selection_agent(self):
        return Agent(
            role='City Selection Expert',
            goal='Select the best city based on weather, season, and prices',
            backstory='An expert in analyzing travel data to pick ideal destinations',
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
            verbose=True)

    def local_expert(self):   
        return Agent(
            role='Local Expert at this city',
            goal='Provide the BEST insights about the selected city',
            backstory="""A knowledgeable local guide with extensive information
            about the city, it's attractions and customs""",
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
            verbose=True)

    def travel_concierge(self):
        return Agent(
            role='Amazing Travel Concierge',
            goal="""Create the most amazing travel itineraries with budget and 
            packing suggestions for the city, including optimal transportation logistics""",
            backstory="""Specialist in travel planning and logistics with 
            decades of experience, adept at finding the best transportation options 
            like flights, trains, buses, and car rentals for any trip""",
            tools=[
                SearchTools.search_internet,
                CalculatorTools.calculate,
                BrowserTools.scrape_and_summarize_website,
            ],
            verbose=True
        )