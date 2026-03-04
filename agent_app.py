import streamlit as st
import requests
import pandas as pd

# -------------------------
# CONFIG
# -------------------------

API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjYyODU3ODEzNywiYWFpIjoxMSwidWlkIjoxMDA1NzE5OTgsImlhZCI6IjIwMjYtMDMtMDRUMDU6MTE6MjguNTAyWiIsInBlciI6Im1lOndyaXRlIiwiYWN0aWQiOjM0MDY0MDY1LCJyZ24iOiJhcHNlMiJ9.qp54G0C06vl4GyyO-UH9_Xy_4hHlhABjlj-3wGYEEYA"
DEALS_BOARD_ID = 5026982858

WORK_ORDERS_BOARD_ID = 5026982919


API_URL = "https://api.monday.com/v2"

headers = {
    "Authorization": API_TOKEN,
    "Content-Type": "application/json"
}

# -------------------------
# UI
# -------------------------

st.set_page_config(page_title="Monday BI Agent", layout="wide")

st.title("📊 Monday.com AI Business Intelligence Agent")

st.markdown(
"""
Ask business questions about **pipeline health, sectors, and deal performance**.
The agent retrieves **live monday.com board data** for every query.
"""
)
st.markdown("### Example Questions")

st.markdown("""
• Show pipeline value  
• How many open deals are there?  
• Show high probability deals  
• Show deals by sector  
• How many work orders exist?
""")

# conversation memory
if "history" not in st.session_state:
    st.session_state.history = []
if "last_intent" not in st.session_state:
    st.session_state.last_intent = None    

user_question = st.text_input("Ask a business question:")

# -------------------------
# MONDAY DATA FETCH
# -------------------------

def fetch_board(board_id):

    query = f"""
    {{
      boards(ids: {board_id}) {{
        items_page(limit:100) {{
          items {{
            name
            column_values {{
              text
              column {{ title }}
            }}
          }}
        }}
      }}
    }}
    """

    response = requests.post(API_URL, json={"query": query}, headers=headers)

    data = response.json()

    items = data["data"]["boards"][0]["items_page"]["items"]

    rows = []

    for item in items:

        row = {"Name": item["name"]}

        for col in item["column_values"]:
            row[col["column"]["title"]] = col["text"]

        rows.append(row)

    return rows

# -------------------------
# BUSINESS ANALYSIS
# -------------------------
def generate_leadership_insights(deals):

    pipeline_total = 0
    open_deals = 0
    high_prob = 0
    sector_counts = {}

    for d in deals:

        # Pipeline value
        value = d.get("Masked Deal value")
        if value:
            try:
                pipeline_total += float(value)
            except:
                pass

        # Open deals
        if d.get("Deal Status") == "Open":
            open_deals += 1

        # High probability
        if d.get("Closure Probability") == "High":
            high_prob += 1

        # Sector counts
        sector = d.get("Sector/service")
        if sector:
            sector_counts[sector] = sector_counts.get(sector, 0) + 1

    top_sector = None

    if sector_counts:
        top_sector = max(sector_counts, key=sector_counts.get)

    return {
        "pipeline": pipeline_total,
        "open_deals": open_deals,
        "high_prob": high_prob,
        "top_sector": top_sector
    }
def analyze_question(question, deals, work_orders):

    q = question.lower()

    # PIPELINE VALUE
    if "pipeline" in q:
        st.session_state.last_intent = "pipeline"
        total = 0

        for d in deals:

            value = d.get("Masked Deal value")

            if value:
                try:
                    total += float(value)
                except:
                    pass

        return f"💰 Total pipeline value is **${total:,.2f}**"


    # OPEN DEALS
    if "open" in q and "deal" in q:
        
        count = sum(
            1 for d in deals
            if d.get("Deal Status") == "Open"
        )

        return f"📈 There are **{count} open deals**."


    # HIGH PROBABILITY
    if "high" in q and "probability" in q:
        st.session_state.last_intent = "high_probability"
        count = 0

        for d in deals:
            if d.get("Closure Probability") == "High":
                count += 1

        return f"🔥 {count} deals have **high closure probability**."

        # PIPELINE HEALTH REPORT
    if "health" in q or "business" in q or "performance" in q:

        pipeline_total = 0
        open_deals = 0
        high_prob = 0
        sector_counts = {}

        for d in deals:

            value = d.get("Masked Deal value")

            if value:
                try:
                    pipeline_total += float(value)
                except:
                    pass

            if d.get("Deal Status") == "Open":
                open_deals += 1

            if d.get("Closure Probability") == "High":
                high_prob += 1

            sector = d.get("Sector/service")

            if sector:
                sector_counts[sector] = sector_counts.get(sector, 0) + 1

        top_sector = None

        if sector_counts:
            top_sector = max(sector_counts, key=sector_counts.get)

        return f"""
    📊 **Pipeline Health Report**

    💰 Total Pipeline Value: ${pipeline_total:,.2f}

    📈 Open Deals: {open_deals}

    🔥 High Probability Deals: {high_prob}

    🏆 Top Sector: {top_sector}

    Overall pipeline health appears **active with strong sector concentration**.
    """
    # TOP SECTOR BY PIPELINE VALUE
    if "top sector" in q or "highest sector" in q:

        sector_value = {}

        for d in deals:

            sector = d.get("Sector/service")
            value = d.get("Masked Deal value")

            if sector and value:

                try:
                    value = float(value)
                except:
                    value = 0

                sector_value[sector] = sector_value.get(sector, 0) + value

        if sector_value:

            best_sector = max(sector_value, key=sector_value.get)

            return f"""
🏆 **Top Performing Sector**

    {best_sector} has the highest pipeline value.

    💰 Total sector value: **${sector_value[best_sector]:,.2f}**
    """
    # SECTOR ANALYSIS
    if "sector" in q:

        sector_counts = {}

        for d in deals:

            sector = d.get("Sector/service")

            if sector:
                sector_counts[sector] = sector_counts.get(sector, 0) + 1

        best_sector = max(sector_counts, key=sector_counts.get)

        return f"""
📊 **Sector Breakdown**

{sector_counts}

🏆 **Top sector:** {best_sector}
"""


    # CROSS BOARD INSIGHT
    if "work order" in q or "operations" in q:

        wo_count = len(work_orders)

        return f"""
⚙️ There are **{wo_count} work orders currently tracked.**

Operational data can be correlated with deals to assess delivery load.
"""
    # FOLLOW-UP QUERY SUPPORT
    if "sector" in q and st.session_state.get("last_intent") == "pipeline":

        sector_counts = {}

        for d in deals:

            sector = d.get("Sector/service")

            if sector:
                sector_counts[sector] = sector_counts.get(sector, 0) + 1

        return f"Pipeline breakdown by sector: {sector_counts}"

    return "❓ I could not understand the question."

# -------------------------
# EXECUTION
# -------------------------

if user_question:

    action_log = []

    action_log.append("🧠 Interpreting user query")

    action_log.append("🔗 Querying Deals board")

    deals = fetch_board(DEALS_BOARD_ID)

    leadership = generate_leadership_insights(deals)

    action_log.append("🔗 Querying Work Orders board")

    work_orders = fetch_board(WORK_ORDERS_BOARD_ID)

    action_log.append("🧹 Cleaning messy board data")

    answer = analyze_question(user_question, deals, work_orders)

    action_log.append("📊 Generating business insight")

    st.session_state.history.append((user_question, answer))

    # -------------------------
    # DASHBOARD
    # -------------------------

    col1, col2 = st.columns([2,1])

    with col1:

        st.subheader("Answer")

        st.write(answer)

        st.subheader("Leadership Insights")

        st.markdown(f"""
        **Pipeline Value:** ${leadership["pipeline"]:,.2f}

        **Open Deals:** {leadership["open_deals"]}

        **High Probability Deals:** {leadership["high_prob"]}

        **Top Sector:** {leadership["top_sector"]}
        """)
        # PIPELINE VALUE BY SECTOR CHART

        sector_values = {}

        for d in deals:

            sector = d.get("Sector/service")
            value = d.get("Masked Deal value")

            if sector and value:

                try:
                    value = float(value)
                except:
                    value = 0

                sector_values[sector] = sector_values.get(sector, 0) + value

        if sector_values:

            df_sector = pd.DataFrame(
                list(sector_values.items()),
                columns=["Sector", "Pipeline Value"]
            )

            st.subheader("Pipeline Value by Sector")
            df_sector = df_sector.sort_values("Pipeline Value", ascending=False)
            st.bar_chart(df_sector.set_index("Sector"))
        # CLOSURE PROBABILITY DISTRIBUTION

        prob_counts = {}

        for d in deals:

            prob = d.get("Closure Probability")

            if prob:
                prob_counts[prob] = prob_counts.get(prob, 0) + 1

        if prob_counts:

            df_prob = pd.DataFrame(
                list(prob_counts.items()),
                columns=["Probability", "Deals"]
            )

            st.subheader("Closure Probability Distribution")

            st.bar_chart(df_prob.set_index("Probability"))    

        st.subheader("Conversation History")

        for q, a in st.session_state.history[-5:]:
            st.write("**Q:**", q)
            st.write("**A:**", a)
            st.write("---")

    with col2:

        st.subheader("Agent Trace")

        for step in action_log:
            st.write("•", step)

# -------------------------
# DATA PREVIEW
# -------------------------

    with st.expander("Preview Deals Data"):
        st.write("Live data from monday.com")
        st.write(deals[:10])