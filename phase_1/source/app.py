
import logging

import streamlit as st
import plotly.express as px

from analytics import run_business_query
from investigation import investigate_business_question
from rag import answer_policy_question


# ============================================================
# 1. APPLICATION CONFIGURATION
# ============================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="D2C Returns Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. CUSTOM UI STYLING
# ============================================================

st.markdown("""
<style>

/* Main page */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Sidebar */
[data-testid="stSidebar"] {
    border-right: 1px solid rgba(128, 128, 128, 0.2);
}

/* Main hero section */
.hero {
    padding: 35px;
    border-radius: 20px;
    background: linear-gradient(120deg, #111827, #172554, #1e3a8a);
    color: white;
    margin-bottom: 22px;
    border: 1px solid rgba(129, 140, 248, 0.25);
}

.hero h1 {
    color: white;
    font-size: 36px;
    font-weight: 750;
    margin-bottom: 10px;
}

.hero p {
    color: #c7d2fe;
    font-size: 15px;
    margin-bottom: 0;
}

/* AI launch card */
.ai-launch-card {
    background: linear-gradient(120deg, #111827, #172554, #312e81);
    border: 1px solid rgba(129, 140, 248, 0.4);
    border-radius: 20px;
    padding: 25px 28px;
    margin: 12px 0 20px 0;
    box-shadow: 0 8px 30px rgba(49, 46, 129, 0.22);
}

.ai-launch-card h2 {
    color: #ffffff;
    font-size: 25px;
    margin: 0 0 8px 0;
}

.ai-launch-card p {
    color: #c7d2fe;
    font-size: 14px;
    margin: 0;
}

.ai-icon {
    font-size: 34px;
    margin-bottom: 12px;
}

/* Metrics */
div[data-testid="stMetric"] {
    padding: 18px;
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 14px;
}

/* Section descriptions */
.section-description {
    color: #8b949e;
    margin-top: -8px;
    margin-bottom: 20px;
}

/* Primary buttons */
.stButton > button[kind="primary"] {
    border-radius: 10px;
    font-weight: 650;
    min-height: 44px;
    transition: all 0.2s ease;
}

.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 18px rgba(99, 102, 241, 0.3);
}

/* Charts and dataframes */
[data-testid="stPlotlyChart"],
[data-testid="stDataFrame"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. CACHED DATABASE ANALYTICS
# ============================================================

@st.cache_data(ttl=300)
def get_dashboard_data():
    """
    Fetch approved analytics from Supabase.
    Results are cached for five minutes.
    """

    overall = run_business_query("overall_returns")
    categories = run_business_query("category_returns")
    shipping = run_business_query("shipping_returns")

    return overall, categories, shipping


# ============================================================
# 4. NAVIGATION FUNCTIONS
# ============================================================

def open_ai_investigation():
    """Navigate directly to the AI Investigation page."""

    st.session_state["page"] = "AI Investigation"


# ============================================================
# 5. SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.title("📊 D2C Intelligence")

    st.caption("Returns Investigation Platform")

    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "Overview",
            "AI Investigation",
            "Policy Explorer",
        ],
        key="page",
    )

    st.divider()

    st.caption("CONNECTED SERVICES")

    st.write("🟢 Supabase PostgreSQL")
    st.write("🟢 Groq AI")
    st.write("🟢 RAG Policy Retrieval")

    st.divider()

    if st.button(
        "🔄 Refresh Dashboard",
        use_container_width=True,
    ):
        get_dashboard_data.clear()
        st.rerun()

    st.caption("D2C Returns Intelligence · Prototype")


# ============================================================
# 6. OVERVIEW DASHBOARD
# ============================================================

if page == "Overview":

    # Main hero
    st.markdown("""
    <div class="hero">
        <h1>D2C Returns Intelligence</h1>
        <p>
            Understand return patterns, explore business metrics,
            and discover what needs your attention.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------------------------------------
    # AI LAUNCH CARD
    # --------------------------------------------------------

    st.markdown("""
    <div class="ai-launch-card">
        <div class="ai-icon">✦</div>
        <h2>Your business. Meet your AI analyst.</h2>
        <p>
            Ask business questions, uncover return patterns,
            and get evidence-backed insights from your data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Actual interactive navigation button
    _, button_col = st.columns([4, 1])

    with button_col:
        st.button(
            "✦ Launch AI Analyst",
            on_click=open_ai_investigation,
            type="primary",
            use_container_width=True,
        )

    st.divider()

    # --------------------------------------------------------
    # LOAD BUSINESS DATA
    # --------------------------------------------------------

    st.subheader("Business Overview")

    st.markdown(
        '<p class="section-description">'
        'A snapshot of your order and return performance.'
        '</p>',
        unsafe_allow_html=True,
    )

    try:

        with st.spinner("Loading business analytics..."):

            overall, categories, shipping = get_dashboard_data()

        if overall.empty:

            st.warning("No order data is currently available.")

        else:

            metrics = overall.iloc[0]

            total_orders = int(metrics["total_orders"] or 0)
            returned_orders = int(metrics["returned_orders"] or 0)
            return_rate = float(
                metrics["return_rate_percent"] or 0
            )

            non_returned = total_orders - returned_orders

            # ------------------------------------------------
            # KPI CARDS
            # ------------------------------------------------

            col1, col2, col3, col4 = st.columns(4)

            col1.metric(
                "Total Orders",
                f"{total_orders:,}",
            )

            col2.metric(
                "Returned Orders",
                f"{returned_orders:,}",
            )

            col3.metric(
                "Return Rate",
                f"{return_rate:.2f}%",
            )

            col4.metric(
                "Non-Returned Orders",
                f"{non_returned:,}",
            )

            st.divider()

            # ------------------------------------------------
            # INTERACTIVE ANALYTICS
            # ------------------------------------------------

            st.subheader("Explore Return Patterns")

            category_options = ["All Categories"] + sorted(
                categories["product_category"]
                .dropna()
                .unique()
                .tolist()
            )

            selected_category = st.selectbox(
                "Filter by product category",
                category_options,
            )

            filtered_categories = categories.copy()

            if selected_category != "All Categories":

                filtered_categories = filtered_categories[
                    filtered_categories["product_category"]
                    == selected_category
                ]

            left, right = st.columns(2)

            # Category chart
            with left:

                st.markdown("#### Return Rate by Category")

                if not filtered_categories.empty:

                    category_chart = px.bar(
                        filtered_categories,
                        x="product_category",
                        y="return_rate_percent",
                        color="return_rate_percent",
                        color_continuous_scale="Blues",
                        labels={
                            "product_category": "Product Category",
                            "return_rate_percent": "Return Rate (%)",
                        },
                        hover_data=[
                            "total_orders",
                            "returned_orders",
                        ],
                    )

                    category_chart.update_layout(
                        xaxis_title="Product Category",
                        yaxis_title="Return Rate (%)",
                        coloraxis_showscale=False,
                        template="plotly_dark",
                        margin=dict(l=20, r=20, t=30, b=20),
                    )

                    st.plotly_chart(
                        category_chart,
                        use_container_width=True,
                    )

                else:

                    st.info("No category data available.")

            # Shipping chart
            with right:

                st.markdown("#### Return Rate by Shipping Method")

                if not shipping.empty:

                    shipping_chart = px.bar(
                        shipping,
                        x="shipping_method",
                        y="return_rate_percent",
                        color="return_rate_percent",
                        color_continuous_scale="Teal",
                        labels={
                            "shipping_method": "Shipping Method",
                            "return_rate_percent": "Return Rate (%)",
                        },
                        hover_data=[
                            "total_orders",
                            "returned_orders",
                        ],
                    )

                    shipping_chart.update_layout(
                        xaxis_title="Shipping Method",
                        yaxis_title="Return Rate (%)",
                        coloraxis_showscale=False,
                        template="plotly_dark",
                        margin=dict(l=20, r=20, t=30, b=20),
                    )

                    st.plotly_chart(
                        shipping_chart,
                        use_container_width=True,
                    )

                else:

                    st.info("No shipping data available.")

            # ------------------------------------------------
            # DETAILED ANALYTICS
            # ------------------------------------------------

            st.divider()

            st.subheader("Detailed Analytics")

            tab1, tab2 = st.tabs(
                [
                    "📦 Category Data",
                    "🚚 Shipping Data",
                ]
            )

            with tab1:

                st.dataframe(
                    categories,
                    use_container_width=True,
                    hide_index=True,
                )

            with tab2:

                st.dataframe(
                    shipping,
                    use_container_width=True,
                    hide_index=True,
                )

    except Exception:

        logger.exception("Dashboard loading failed")

        st.error(
            "Unable to load dashboard data. "
            "Check the VS Code terminal for details."
        )


# ============================================================
# 7. AI BUSINESS INVESTIGATION
# ============================================================

elif page == "AI Investigation":

    st.title("✦ AI Business Investigation")

    st.markdown(
        "Your AI analyst helps investigate business questions "
        "using structured analytics and policy evidence."
    )

    st.divider()

    st.markdown("### What would you like to investigate?")

    example_questions = [
        "Show me the overall return rate and total number of orders.",
        "Which product categories have the highest return rates?",
        "Which shipping methods have the highest return rates?",
        "What should we investigate about product returns?",
    ]

    selected_question = st.selectbox(
        "Choose an example question",
        ["Choose a question"] + example_questions,
    )

    question = st.text_area(
        "Your business question",
        value=(
            ""
            if selected_question == "Choose a question"
            else selected_question
        ),
        placeholder=(
            "Example: Which product categories have "
            "the highest return rates?"
        ),
        height=130,
    )

    if st.button(
        "🚀 Run Investigation",
        type="primary",
        use_container_width=True,
    ):

        if not question.strip():

            st.warning("Please enter a business question.")

        else:

            try:

                with st.spinner(
                    "Investigating business data and retrieving evidence..."
                ):

                    result = investigate_business_question(
                        question.strip()
                    )

                st.success("Investigation completed.")

                st.divider()

                st.subheader("📋 Investigation Report")

                st.markdown(result["report"])

                st.divider()

                tab1, tab2 = st.tabs(
                    [
                        "📊 Supporting Analytics",
                        "📚 Policy Evidence",
                    ]
                )

                with tab1:

                    st.caption(
                        f"Approved query: {result['query_name']}"
                    )

                    st.dataframe(
                        result["analytics"],
                        use_container_width=True,
                        hide_index=True,
                    )

                with tab2:

                    st.markdown("### Retrieved Policy Evidence")

                    st.write(result["policy_evidence"])

            except Exception:

                logger.exception("Business investigation failed")

                st.error(
                    "The investigation failed. "
                    "Check the VS Code terminal for details."
                )


# ============================================================
# 8. POLICY EXPLORER
# ============================================================

elif page == "Policy Explorer":

    st.title("📚 Return Policy Explorer")

    st.markdown(
        "Explore your return policy using retrieval-augmented "
        "generation (RAG)."
    )

    st.divider()

    st.markdown("### Ask a policy question")

    policy_question = st.text_area(
        "Your question",
        placeholder=(
            "Example: How many days does a customer "
            "have to return a product?"
        ),
        height=130,
    )

    if st.button(
        "🔍 Search Policy",
        type="primary",
        use_container_width=True,
    ):

        if not policy_question.strip():

            st.warning("Please enter a policy question.")

        else:

            try:

                with st.spinner(
                    "Searching policy documents..."
                ):

                    policy_answer = answer_policy_question(
                        policy_question.strip()
                    )

                st.success("Policy search completed.")

                st.subheader("📖 Policy Answer")

                st.write(policy_answer)

            except Exception:

                logger.exception("Policy retrieval failed")

                st.error(
                    "Unable to retrieve policy information. "
                    "Check the VS Code terminal for details."
                )
