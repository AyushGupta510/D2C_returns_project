
import streamlit as st

# Configure the page before displaying other Streamlit elements.
st.set_page_config(
    page_title="D2C Returns Intelligence",
    page_icon="📊",
    layout="wide",
)

# Display the project title and explain its purpose.
st.title("D2C Returns Intelligence")
st.write(
    "Investigate return-rate patterns using business analytics "
    "and evidence from return-policy documents."
)

# Let the user enter a business question.
question = st.text_area(
    "Ask a business question",
    placeholder=(
        "Example: Why should we investigate high return rates "
        "across product categories?"
    ),
)

# Add a button to start the investigation.
if st.button("Investigate", type="primary"):
    if question.strip():
        st.info("Your question is ready for investigation.")
    else:
        st.warning("Please enter a business question first.")
