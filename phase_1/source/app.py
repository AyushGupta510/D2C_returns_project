
import logging

import streamlit as st

from investigation import investigate_business_question


# Configure logging so application errors can be debugged in the terminal.
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configure the Streamlit page before rendering other elements.
st.set_page_config(
    page_title="D2C Returns Intelligence",
    page_icon="📊",
    layout="wide",
)


# Display the application title and purpose.
st.title("D2C Returns Intelligence")
st.caption(
    "Investigate e-commerce returns using Supabase analytics, "
    "policy evidence, and GenAI-powered analysis."
)

st.divider()


# Let users enter a business question.
question = st.text_area(
    "Ask a business question",
    placeholder=(
        "Example: Why should we investigate high return rates "
        "across product categories?"
    ),
    height=120,
)


# Run the investigation when the user clicks the button.
if st.button("Investigate", type="primary"):
    if not question.strip():
        st.warning("Please enter a business question.")

    else:
        try:
            # Show progress while analytics, retrieval, and Groq run.
            with st.spinner(
                "Analyzing business data and retrieving policy evidence..."
            ):
                result = investigate_business_question(
                    question.strip()
                )

            # Display the generated investigation report.
            st.subheader("Investigation Report")
            st.markdown(result["report"])

            # Display the database results used in the report.
            with st.expander("View supporting analytics"):
                st.caption(
                    f"Approved query: {result['query_name']}"
                )
                st.dataframe(
                    result["analytics"],
                    use_container_width=True,
                    hide_index=True,
                )

            # Display the answer generated from retrieved policy evidence.
            with st.expander("View policy evidence"):
                st.write(result["policy_evidence"])

        except Exception:
            # Record the traceback in the terminal for debugging.
            logger.exception("Business investigation failed")

            # Show a user-friendly message without exposing internal details.
            st.error(
                "The investigation failed. Check the VS Code terminal "
                "for the detailed error."
            )
