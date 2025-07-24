# # streamlit_interface.py

# import streamlit as st
# from travel_graph import build_conversation_graph
# from llm_provider import ACTIVE_LLM
# from langchain_core.messages import HumanMessage

# # --- Helper to summarize the conversation ---
# def summarize_conversation(messages, existing_summary=""):
#     """
#     Summarizes the conversation by combining the existing summary with the latest user message.
#     """
#     latest_user_message = messages[-1]["content"] if messages else ""
#     prompt = (
#         "You are a conversation summarizer. Combine the existing summary and the latest user message "
#         "to produce a concise summary that retains key context for the next agent.\n\n"
#         f"Existing Summary:\n{existing_summary}\n\n"
#         f"Latest Message:\n{latest_user_message}\n\n"
#         "Updated Summary:"
#     )
#     response = ACTIVE_LLM.invoke([HumanMessage(content=prompt)])
#     return response.content.strip()

# # --- Streamlit UI Setup ---
# st.set_page_config(page_title="Travel Planner Bot", page_icon="✈️")
# st.title("✈️ Travel Planning Multi-Agent Chatbot")
# st.write("_Type your travel requests below. Example: Plan a 5-day luxury trip to Japan._")

# # Initialize Graph and Session State
# graph = build_conversation_graph()
# if "messages" not in st.session_state:
#     st.session_state["messages"] = []
# if "summary" not in st.session_state:
#     st.session_state["summary"] = ""

# # Toggle for Showing Summary
# show_summary = st.checkbox("Show Conversation Summary", value=False)

# # Display Chat History
# for msg in st.session_state["messages"]:
#     role_display = "🧑‍💼 You" if msg["role"] == "user" else "🤖 Bot"
#     st.markdown(f"**{role_display}:** {msg['content']}")

# # Optional Summary Display
# if show_summary and st.session_state["summary"]:
#     st.markdown("### 📝 Conversation Summary")
#     st.write(st.session_state["summary"])

# # Input Box and Buttons
# user_input = st.text_input("Your message", key="user_input")
# col1, col2 = st.columns(2)
# with col1:
#     send_button = st.button("Send", use_container_width=True)
# with col2:
#     reset_button = st.button("Reset Conversation", use_container_width=True)

# # Reset Conversation
# if reset_button:
#     st.session_state["messages"] = []
#     st.session_state["summary"] = ""
#     st.rerun()

# # Process User Input
# if send_button and user_input.strip():
#     # Store user message
#     st.session_state["messages"].append({"role": "user", "content": user_input.strip()})

#     # Generate updated summary
#     summary = summarize_conversation(st.session_state["messages"], st.session_state["summary"])
#     st.session_state["summary"] = summary

#     # Prepare state with conversation and summary
#     state = {
#         "messages": st.session_state["messages"],
#         "summary": st.session_state["summary"]
#     }

#     # Run the Graph
#     result = graph.invoke(state)

#     # Extract latest bot response safely
#     bot_messages = result.get("messages", [])
#     response_text = bot_messages[-1].content if bot_messages else "Sorry, I couldn’t process that."

#     # Store bot response
#     st.session_state["messages"].append({"role": "assistant", "content": response_text})

#     # Rerun to refresh chat view
#     st.rerun()


# # streamlit_interface.py

# import streamlit as st
# from travel_graph import build_conversation_graph

# # Page Config
# st.set_page_config(page_title="Travel Planner Bot", page_icon="✈️")

# st.title("✈️ Travel Planning Multi-Agent Chatbot")
# st.write("_Type your travel requests below. Example: Plan a 5-day luxury trip to Japan._")

# # Initialize the graph
# graph = build_conversation_graph()

# # Initialize session state
# if "messages" not in st.session_state:
#     st.session_state["messages"] = []
# if "travel_preferences" not in st.session_state:
#     st.session_state["travel_preferences"] = {}

# # Display conversation history
# for msg in st.session_state["messages"]:
#     role_display = "🧑‍💼 You" if msg["role"] == "user" else "🤖 Bot"
#     st.markdown(f"**{role_display}:** {msg['content']}")

# # User Input Box
# user_input = st.text_input("Your message", key="user_input")

# # Action Buttons
# col1, col2 = st.columns(2)
# with col1:
#     send_button = st.button("Send", use_container_width=True)
# with col2:
#     reset_button = st.button("Reset Conversation", use_container_width=True)

# # Reset conversation state
# if reset_button:
#     st.session_state["messages"] = []
#     st.session_state["travel_preferences"] = {}
#     st.rerun()

# # Handle user input
# if send_button and user_input.strip():
#     # Append user message
#     st.session_state["messages"].append({"role": "user", "content": user_input.strip()})

#     # Prepare state with conversation and preferences
#     state = {
#         "messages": st.session_state["messages"],
#         "preferences": st.session_state.get("travel_preferences", {})
#     }

#     # Run the graph
#     result = graph.invoke(state)

#     # Extract bot response
#     bot_messages = result.get("messages", [])
#     response_text = bot_messages[-1].content if bot_messages else "Sorry, I couldn’t process that."

#     # Append bot response
#     st.session_state["messages"].append({"role": "assistant", "content": response_text})

#     # Rerun to show response
#     st.rerun()

# # Check if itinerary is ready and ask for travel preferences
# if st.session_state["messages"]:
#     last_message = st.session_state["messages"][-1]["content"].lower()
#     if "itinerary" in last_message:
#         st.markdown("**✈️ Let's finalize your travel details.**")
#         travelers = st.text_input("How many travelers?", key="travelers")
#         flight_class = st.selectbox("Preferred flight class?", ["Economy", "Premium Economy", "Business", "First"], key="flight_class")
#         hotel_rating = st.selectbox("Preferred hotel rating?", ["3-star", "4-star", "5-star"], key="hotel_rating")

#         confirm_preferences = st.button("Confirm Preferences")

#         if confirm_preferences:
#             st.session_state["travel_preferences"] = {
#                 "travelers": travelers,
#                 "flight_class": flight_class,
#                 "hotel_rating": hotel_rating
#             }
#             st.success("Preferences saved! You can now proceed with flight or hotel options.")

# import streamlit as st
# from travel_graph import build_conversation_graph

# # Page Config
# st.set_page_config(page_title="Travel Planner Bot", page_icon="✈️")

# st.title("✈️ Travel Planning Multi-Agent Chatbot")
# st.write("_Type your travel requests below. Example: Plan a 5-day luxury trip to Japan._")

# # Initialize the graph
# graph = build_conversation_graph()

# # Initialize session state if not already present
# if "messages" not in st.session_state:
#     st.session_state["messages"] = []
# if "preferences" not in st.session_state:
#     st.session_state["preferences"] = {
#         "destination": None,
#         "days": None,
#         "budget": None,
#         "departure_city": None,
#         "travel_dates": None,
#         "hotel_rating": None,
#         "travelers": None,
#         "flight_class": None,
#     }

# # Display conversation history
# for msg in st.session_state["messages"]:
#     role_display = "🧑‍💼 You" if msg["role"] == "user" else "🤖 Bot"
#     st.markdown(f"**{role_display}:** {msg['content']}")

# # User Input Box
# user_input = st.text_input("Your message", key="user_input")

# # Action Buttons
# col1, col2 = st.columns(2)
# with col1:
#     send_button = st.button("Send", use_container_width=True)
# with col2:
#     reset_button = st.button("Reset Conversation", use_container_width=True)

# # Reset conversation state
# if reset_button:
#     st.session_state["messages"] = []
#     st.session_state["preferences"] = {
#         "destination": None,
#         "days": None,
#         "budget": None,
#         "departure_city": None,
#         "travel_dates": None,
#         "hotel_rating": None,
#         "travelers": None,
#         "flight_class": None,
#     }
#     st.rerun()

# # Process user input
# if send_button and user_input.strip():
#     # Append user message to session state
#     st.session_state["messages"].append({"role": "user", "content": user_input.strip()})

#     # Prepare state with conversation history
#     state = {"messages": st.session_state["messages"]}

#     # Run the graph
#     result = graph.invoke(state)

#     # Extract and save the bot's reply
#     bot_messages = result.get("messages", [])
#     response_text = bot_messages[-1].content if bot_messages else "Sorry, I couldn’t process that."
#     st.session_state["messages"].append({"role": "assistant", "content": response_text})

#     # Show updated chat
#     st.rerun()

# # Display current preferences summary if available
# preferences = st.session_state["preferences"]
# if any(preferences.values()):
#     st.markdown("### ✍️ Your Current Preferences")
#     for key, value in preferences.items():
#         if value:
#             st.write(f"- **{key.replace('_', ' ').capitalize()}**: {value}")

#     st.markdown("### 🚀 What would you like to do next?")
#     col3, col4, col5 = st.columns(3)
#     with col3:
#         if st.button("Check Flights", key="check_flights"):
#             st.session_state["messages"].append({"role": "user", "content": "Check flights based on my preferences."})
#             st.rerun()
#     with col4:
#         if st.button("Review Hotels", key="review_hotels"):
#             st.session_state["messages"].append({"role": "user", "content": "Show me hotel options based on my preferences."})
#             st.rerun()
#     with col5:
#         if st.button("Finalize Booking", key="finalize_booking"):
#             st.session_state["messages"].append({"role": "user", "content": "Let's finalize the booking."})
#             st.rerun()



####################
import streamlit as st
from fpdf import FPDF
from datetime import datetime
from travel_graph import build_conversation_graph

# Page Configuration
st.set_page_config(page_title="Travel Planner", page_icon="✈️")
st.title("✈️ Travel Planning Multi-Agent Chatbot")

# Build Graph Once
graph = build_conversation_graph()

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "graph_state" not in st.session_state:
    st.session_state["graph_state"] = {"messages": []}
if "summary" not in st.session_state:
    st.session_state["summary"] = ""

# Display Chat History
for msg in st.session_state["messages"]:
    role_display = "🧑‍💼 You" if msg["role"] == "user" else "🤖 Bot"
    st.markdown(f"**{role_display}:** {msg['content']}")

# User Input
user_input = st.text_input("Type your travel request below")

# Buttons
col1, col2 = st.columns(2)
with col1:
    send_button = st.button("Send")
with col2:
    reset_button = st.button("Reset Conversation")

# Toggle Debug Mode
debug_mode = st.checkbox("Enable Debug Mode", value=False)

# Handle Reset
if reset_button:
    st.session_state["messages"] = []
    st.session_state["graph_state"] = {"messages": []}
    st.session_state["summary"] = ""
    st.experimental_rerun()

# Process User Input
if send_button and user_input.strip():
    user_msg = {"role": "user", "content": user_input.strip()}
    st.session_state["messages"].append(user_msg)
    st.session_state["graph_state"]["messages"].append(user_msg)

    result = graph.invoke(st.session_state["graph_state"])
    bot_messages = result.get("messages", [])

    if bot_messages:
        latest_bot_msg = getattr(bot_messages[-1], 'content', str(bot_messages[-1]))
        bot_msg = {"role": "assistant", "content": latest_bot_msg}
        st.session_state["messages"].append(bot_msg)
        st.session_state["graph_state"]["messages"].append(bot_msg)
        st.session_state["summary"] = "\n".join(getattr(m, 'content', str(m)) for m in bot_messages)

    # Debug Output
    if debug_mode:
        st.markdown("---")
        st.markdown("### 🐛 Debug Log")
        for idx, msg in enumerate(bot_messages):
            role = getattr(msg, 'role', 'Unknown')
            content = getattr(msg, 'content', str(msg))
            st.text(f"[{idx + 1}] {role}: {content}")
        st.markdown("---")

    st.rerun()

# Summary Toggle
if st.session_state["summary"]:
    show_summary = st.checkbox("Show Conversation Summary", value=False)
    if show_summary:
        st.markdown("### 📝 Conversation Summary")
        st.text(st.session_state["summary"])

# PDF Export Utility
class CustomPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Travel Conversation Summary', ln=True, align='C')
        self.ln(10)

    def add_section(self, title, content):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True)
        self.set_font('Arial', '', 10)
        self.multi_cell(0, 10, content)
        self.ln(5)

def export_pdf(summary: str) -> str:
    pdf = CustomPDF()
    pdf.add_page()
    pdf.add_section("Summary", summary or "No content.")
    filename = f"travel_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf.output(filename)
    return filename

# PDF Export Button
if st.session_state["summary"]:
    if st.button("Export Conversation as PDF"):
        filename = export_pdf(st.session_state["summary"])
        with open(filename, "rb") as file:
            st.download_button(
                label="Download Conversation Summary",
                data=file,
                file_name=filename,
                mime="application/pdf"
            )


# # PDF Export Function
def export_pdf(itinerary="", hotel_options="", food_suggestions=""):
    pdf = CustomPDF()
    pdf.add_section("Itinerary", itinerary or "Not specified.")
    pdf.add_section("Hotel Options", hotel_options or "Not specified.")
    pdf.add_section("Food Suggestions", food_suggestions or "Not specified.")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"travel_plan_{timestamp}.pdf"
    pdf.output(file_path)
    return file_path

# # Process User Input
if send_button and user_input.strip():
    st.session_state["messages"].append({"role": "user", "content": user_input.strip()})
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    state = {"messages": st.session_state["messages"],
             "current_date": current_date}
    result = graph.invoke(state)
    
    # Extract Bot Response
    bot_messages = result.get("messages", [])
    if bot_messages:
        last_response = bot_messages[-1].content if hasattr(bot_messages[-1], 'content') else str(bot_messages[-1])
    else:
        last_response = "Sorry, I couldn’t process that."

    st.session_state["messages"].append({"role": "assistant", "content": last_response})
    st.rerun()

# PDF Export Option
if st.session_state["messages"]:
    if st.button("Export as PDF"):
        conversation_text = "\n\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in st.session_state["messages"]])
        file_path = export_pdf(itinerary=conversation_text)
        with open(file_path, "rb") as file:
            st.download_button(label="Download Travel Plan as PDF", data=file, file_name=file_path, mime="application/pdf")

# import streamlit as st
# from fpdf import FPDF
# from datetime import datetime
# from travel_graph import build_conversation_graph

# # Page Configuration
# st.set_page_config(page_title="Travel Planner", page_icon="✈️")
# st.title("✈️ Travel Planning Multi-Agent Chatbot")

# # Build Graph Once
# graph = build_conversation_graph()

# # Initialize Session State
# if "messages" not in st.session_state:
#     st.session_state["messages"] = []
# if "graph_state" not in st.session_state:
#     st.session_state["graph_state"] = {"messages": []}
# if "summary" not in st.session_state:
#     st.session_state["summary"] = ""

# # Display Chat History
# for msg in st.session_state["messages"]:
#     role_display = "🧑‍💼 You" if msg["role"] == "user" else "🤖 Bot"
#     st.markdown(f"**{role_display}:** {msg['content']}")

# # User Input
# user_input = st.text_input("Type your travel request below")

# # Buttons
# col1, col2 = st.columns(2)
# with col1:
#     send_button = st.button("Send")
# with col2:
#     reset_button = st.button("Reset Conversation")

# # Handle Reset
# if reset_button:
#     st.session_state["messages"] = []
#     st.session_state["graph_state"] = {"messages": []}
#     st.session_state["summary"] = ""
#     st.rerun()

# # Process User Input
# if send_button and user_input.strip():
#     user_msg = {"role": "user", "content": user_input.strip()}
#     st.session_state["messages"].append(user_msg)
#     st.session_state["graph_state"]["messages"].append(user_msg)

#     # Invoke Graph
#     result = graph.invoke(st.session_state["graph_state"])
#     bot_messages = result.get("messages", [])

#     # Gracefully extract latest bot message
#     if bot_messages:
#         latest_bot_msg = getattr(bot_messages[-1], 'content', str(bot_messages[-1]))
#         bot_msg = {"role": "assistant", "content": latest_bot_msg}
#         st.session_state["messages"].append(bot_msg)
#         st.session_state["graph_state"]["messages"].append(bot_msg)
#         st.session_state["summary"] = "\n".join(getattr(m, 'content', str(m)) for m in bot_messages)

#     st.rerun()

# # Summary Toggle
# if st.session_state["summary"]:
#     show_summary = st.checkbox("Show Conversation Summary", value=False)
#     if show_summary:
#         st.markdown("### 📝 Conversation Summary")
#         st.text(st.session_state["summary"])

# # PDF Export Utility
# class CustomPDF(FPDF):
#     def header(self):
#         self.set_font('Arial', 'B', 16)
#         self.cell(0, 10, 'Travel Conversation Summary', ln=True, align='C')
#         self.ln(10)

#     def add_section(self, title, content):
#         self.set_font('Arial', 'B', 12)
#         self.cell(0, 10, title, ln=True)
#         self.set_font('Arial', '', 10)
#         self.multi_cell(0, 10, content)
#         self.ln(5)

# def export_pdf(summary: str) -> str:
#     pdf = CustomPDF()
#     pdf.add_page()
#     pdf.add_section("Summary", summary or "No content.")
#     filename = f"travel_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
#     pdf.output(filename)
#     return filename

# # PDF Export Button
# if st.session_state["summary"]:
#     if st.button("Export Conversation as PDF"):
#         filename = export_pdf(st.session_state["summary"])
#         with open(filename, "rb") as file:
#             st.download_button(
#                 label="Download Conversation Summary",
#                 data=file,
#                 file_name=filename,
#                 mime="application/pdf"
#             )
