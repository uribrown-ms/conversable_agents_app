import os
import streamlit as st
from autogen import ConversableAgent

def create_agent(name, system_message):
    return ConversableAgent(
        name=name,
        system_message=system_message,
        llm_config={"config_list": [{"model": "gpt-4", "temperature": 0.9, "api_key": os.environ.get("OPENAI_API_KEY")}]},
        human_input_mode="NEVER",
    )

# Initialize session state for conversation log if it doesn't exist
if 'conversation_log' not in st.session_state:
    st.session_state['conversation_log'] = ""

# Streamlit app
st.title("Conversable Agents Duo")

# Sidebar configuration for Agent 1
st.sidebar.header("Agent 1 Configuration")
agent1_name = st.sidebar.text_input("Agent 1 Name", value="Cathy")
agent1_system_message = st.sidebar.text_area("Agent 1 System Message", value="Your name is Cathy and you are a part of a duo of comedians.")

# Sidebar configuration for Agent 2
st.sidebar.header("Agent 2 Configuration")
agent2_name = st.sidebar.text_input("Agent 2 Name", value="Joe")
agent2_system_message = st.sidebar.text_area("Agent 2 System Message", value="Your name is Joe and you are a part of a duo of comedians.")

# Sidebar option for max turns
max_turns = st.sidebar.number_input("Max Turns", min_value=1, max_value=50, value=2)
initial_message = st.sidebar.text_input("Initial Message", value="Cathy, tell me a joke.")

# Run the conversation when the button is pressed
if st.button("Run Conversation"):
    with st.spinner("Running agents..."):
        agent1 = create_agent(agent1_name, agent1_system_message)
        agent2 = create_agent(agent2_name, agent2_system_message)

        # Initiate conversation
        result = agent2.initiate_chat(agent1, message=initial_message, max_turns=max_turns)
        
        # Map roles to names
        role_to_name = {
            "assistant": agent1_name,
            "user": agent2_name
        }

        # Display the conversation result using text_area
        st.subheader("Conversation Result")
        try:
            # Check if result has 'chat_history' and it's a list
            if hasattr(result, 'chat_history') and isinstance(result.chat_history, list):
                conversation = "\n".join([f"{role_to_name.get(turn.get('role', ''), turn.get('role', ''))}: {turn.get('content', '[No content]')}" for turn in result.chat_history])
                st.session_state['conversation_log'] += conversation + "\n"  # Store conversation in session state
            else:
                st.error("Conversation history is not available or not structured as expected.")
        except (TypeError, AttributeError, KeyError) as e:
            st.error(f"Error parsing the conversation result: {e}")

# Display the conversation log
st.text_area("Conversation Log", st.session_state['conversation_log'], height=300)

# Clear conversation button
if st.button("Clear Conversation"):
    st.session_state['conversation_log'] = ""  # Reset the conversation log
