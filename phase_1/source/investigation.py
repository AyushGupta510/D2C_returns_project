
import json

from langchain_groq import ChatGroq

from config import GROQ_API_KEY
from analytics import run_business_query
from rag import answer_policy_question


# Use the Groq model you previously tested.
GROQ_MODEL = "openai/gpt-oss-120b"


def investigate_business_question(question: str) -> dict:
    """Combine business analytics and policy evidence into a report."""

    # Reject empty questions before making database or API calls.
    if not question or not question.strip():
        raise ValueError("Please enter a business question.")

    # Ask Groq to select only an approved analytics query.
    router = ChatGroq(
        api_key=GROQ_API_KEY,
        model=GROQ_MODEL,
        temperature=0,
    )

    routing_prompt = f"""
Choose the single best query for this business question.

Available query names:
- overall_returns
- category_returns
- shipping_returns

Return only the query name, with no explanation.

Question: {question}
"""

    routing_response = router.invoke(routing_prompt)
    query_name = routing_response.content.strip()

    # Validate the model's choice before running a database query.
    allowed_queries = {
        "overall_returns",
        "category_returns",
        "shipping_returns",
    }

    if query_name not in allowed_queries:
        query_name = "overall_returns"

    # Retrieve measured business data from Supabase.
    analytics_df = run_business_query(query_name)

    # Retrieve relevant evidence from the return-policy document.
    policy_evidence = answer_policy_question(question)

    # Convert the SQL results into readable JSON for the report prompt.
    analytics_json = analytics_df.to_json(
        orient="records",
        indent=2,
    )

    # Ask Groq to explain the evidence without inventing causation.
    report_prompt = f"""
You are a business returns investigation analyst.

Analyze the question using only the supplied analytics and policy answer.

Rules:
- Distinguish measured facts from hypotheses.
- Do not claim that a factor caused returns unless the evidence proves it.
- If evidence is insufficient, explicitly say so.
- Recommend practical next investigations.

Business question:
{question}

Analytics query used:
{query_name}

Analytics results:
{analytics_json}

Policy evidence:
{policy_evidence}

Return a report with these sections:
1. Key findings
2. Relevant policy evidence
3. What the data does and does not establish
4. Recommended next investigations
"""

    report_response = router.invoke(report_prompt)

    # Return structured components so Streamlit can display them separately.
    return {
        "question": question,
        "query_name": query_name,
        "analytics": analytics_df,
        "policy_evidence": policy_evidence,
        "report": report_response.content,
    }
