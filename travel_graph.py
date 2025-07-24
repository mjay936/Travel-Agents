import os
import requests
from dotenv import load_dotenv
from llm_provider import ACTIVE_LLM
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

# Load environment variables
load_dotenv()
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY")
AMADEUS_API_SECRET = os.getenv("AMADEUS_API_SECRET")
AVIATIONSTACK_API_KEY = os.getenv("AVIATIONSTACK_API_KEY")


def get_amadeus_access_token():
    """Obtain Amadeus API OAuth2 Access Token."""
    url = "https://test.api.amadeus.com/v1/security/oauth2/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': AMADEUS_API_KEY,
        'client_secret': AMADEUS_API_SECRET
    }
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"Failed to retrieve Amadeus token: {response.text}")


def search_hotels(city_code: str, check_in: str, check_out: str, adults: int = 1) -> str:
    """Search hotels using Amadeus API based on city, dates, and number of adults."""
    token = get_amadeus_access_token()
    url = f"https://test.api.amadeus.com/v2/shopping/hotel-offers?cityCode={city_code}&checkInDate={check_in}&checkOutDate={check_out}&adults={adults}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Failed to retrieve hotels: {response.text}"
    hotels = response.json().get("data", [])
    if not hotels:
        return "No hotels found."
    return "\n".join([
        f"{h['hotel']['name']} - ${h['offers'][0]['price']['total']}"
        for h in hotels[:3]
    ])


def hotel_search_tool(city_code: str, check_in: str, check_out: str, adults: int = 1) -> str:
    """Retrieve hotel options for specified city and dates using Amadeus API."""
    return search_hotels(city_code, check_in, check_out, adults)


def flight_search_tool(query: str) -> str:
    """Search for flights using AviationStack API (static example)."""
    source = "JFK"
    destination = "LHR"
    date = "2025-06-01"
    url = f"http://api.aviationstack.com/v1/flights?access_key={AVIATIONSTACK_API_KEY}&dep_iata={source}&arr_iata={destination}&flight_date={date}"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Failed to fetch flight data: {response.text}"
    flights = response.json().get('data', [])
    if not flights:
        return "No flights found."
    return "\n".join([
        f"{f['airline']['name']} flight {f['flight']['iata']} at {f['departure']['scheduled']}"
        for f in flights[:3]
    ])


# Itinerary Agent Prompt
itinerary_agent_prompt = (
    """
    You are a world-class travel planner.

    Based on:
    - Destination
    - Number of days
    - Budget (budget, mid-range, luxury)

    Generate a **fully detailed day-by-day itinerary** including:
    - Key activities
    - Recommended dining options
    - Cultural highlights
    - Local tips if applicable

    Only return the itinerary content, nothing else.
    """
)

# Fully LLM-Driven Itinerary Agent
itinerary_agent = create_react_agent(
    model=ACTIVE_LLM,
    tools=[],
    prompt=itinerary_agent_prompt,
    name="itinerary_agent"
)

# Flight and Hotel Agents
flight_agent = create_react_agent(
    model=ACTIVE_LLM,
    tools=[flight_search_tool],
    prompt="You are a flight booking assistant. Help users find flights based on destination and travel dates.",
    name="flight_agent"
)

hotel_agent = create_react_agent(
    model=ACTIVE_LLM,
    tools=[hotel_search_tool],
    prompt="You are a hotel booking assistant. Find hotels based on city, check-in, and check-out dates.",
    name="hotel_agent"
)


# ✅ Updated Supervisor Prompt to Ensure Itinerary is Shown
supervisor_prompt = (
    """
    You are a world-class travel planning supervisor.

    🧭 Responsibilities:
    - Collect:
        - Destination
        - Number of Days (default to 3)
        - Budget (budget, mid-range, luxury)

    ✈️ Once collected:
    - HANDOFF to `itinerary_agent`.
    - WAIT for the agent to return a **full, visible itinerary**.

    📋 After presenting the itinerary:
    - Repeat the full itinerary content to the user.
    - THEN ask: "Does this look good to you?". this can not be the first response. 

    ✅ After confirmation ("yes", "looks good", or "finalize itinerary"):
    - Collect:
        - Departure city
        - Travel dates
        - Hotel rating
        - Number of travelers
        - Flight class

    🎯 Then:
    - HANDOFF to `hotel_agent` or `flight_agent` based on user request.
    - Respond only with the agent’s message without extra commentary.
    """
)


def build_conversation_graph():
    """Build the multi-agent graph with itinerary, flight, and hotel agents."""
    supervisor = create_supervisor(
        model=ACTIVE_LLM,
        agents=[itinerary_agent, flight_agent, hotel_agent],
        prompt=supervisor_prompt,
        add_handoff_back_messages=True,
        output_mode="full_history",
    )
    return supervisor.compile()


if __name__ == "__main__":
    graph = build_conversation_graph()
    test_state = {"messages": [{"role": "user", "content": "Plan a 3-day solo budget trip to Bali"}]}
    result = graph.invoke(test_state)
    for msg in result.get("messages", []):
        print(f"{msg['role'].capitalize()}: {msg['content']}")
