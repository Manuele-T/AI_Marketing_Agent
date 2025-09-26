# ui.py
"""
This file creates a user-friendly web interface for the AI Marketing Assistant using Streamlit.

It allows users to:
1.  View and edit the cafe's marketing playbook.
2.  Trigger the AI agent workflow to generate a new marketing brief.
3.  View the final, formatted marketing recommendations.
"""

import streamlit as st
from app import run_workflow

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Daily Marketing Brief Generator",
    page_icon="🤖",
    layout="centered"
)

# --- UI Elements ---

# 1. Display the application title
st.title("🤖 AI Daily Marketing Brief Generator")

# 2. Show instructions to the user
st.info("Click the button below to get a fresh marketing brief from the AI agents. It will analyze today's weather, events, and news to give you tailored post ideas.")

# 3. Create the workflow button
if st.button("Generate Today's Brief", type="primary"):
    # Show a loading spinner while the workflow is running
    with st.spinner("The AI agents are brainstorming..."):
        final_brief = run_workflow()
    
    # --- Display the Final Output ---
    if final_brief:
        st.success("Briefing complete! Here are your marketing ideas:")

        # Weather-Based Post Section
        st.subheader("Weather-Based Post")
        weather_summary = final_brief.get("weather_summary", "Not available.")
        food_recommendation = final_brief.get("food_recommendation", "Not available.")
        st.markdown(f"**Weather:** {weather_summary}")
        st.info(f"**Recommendation:** {food_recommendation}")

        # Event-Based Post Ideas Section
        st.subheader("Event-Based Post Ideas")
        events = final_brief.get("events", [])
        message_ideas = final_brief.get("message_ideas", [])

        if events and message_ideas:
            for i, event in enumerate(events):
                event_title = event.get('title', 'N/A')
                event_postcode = event.get('postcode', 'N/A')
                message = message_ideas[i] if i < len(message_ideas) else "No message idea for this event."
                
                postcode_info = f" (Postcode: {event_postcode})" if event_postcode and event_postcode != "Not found" else ""
                
                st.markdown(f"**Event:** {event_title}{postcode_info}")
                st.info(f"**Idea:** {message}")
        else:
            st.warning("No event-based post ideas were generated.")
    else:
        st.error("The workflow failed to generate a brief. Please check the console for errors.")

# 4. Display the Cafe's Playbook in a collapsible section
with st.expander("View & Edit Cafe Playbook"):
    try:
        with open("cafe_context.md", "r", encoding="utf-8") as f:
            playbook_content = f.read()
        
        edited_playbook = st.text_area(
            "Cafe Playbook Content",
            value=playbook_content,
            height=300
        )

        if st.button("Save Changes"):
            try:
                with open("cafe_context.md", "w", encoding="utf-8") as f:
                    f.write(edited_playbook)
                st.success("Playbook saved successfully!")
            except Exception as e:
                st.error(f"Failed to save playbook: {e}")

    except FileNotFoundError:
        st.error("cafe_context.md not found. Please create this file.")
    except Exception as e:
        st.error(f"An error occurred: {e}")
