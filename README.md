# 📊 Monday.com AI Business Intelligence Agent

This project implements a **Business Intelligence AI agent** that retrieves and analyzes data from monday.com boards using the monday API.

The system allows users to ask **business questions about deals, pipeline health, sectors, and operations**, and generates insights through an interactive dashboard built with **Streamlit**.

The agent queries monday boards in real time and converts raw board data into meaningful business analytics.

---

# 🚀 Features

• Query monday.com boards using the GraphQL API  
• Compute **pipeline value and deal statistics**  
• Identify **open deals and high probability deals**  
• Analyze **sector performance**  
• Generate **leadership insights dashboard**  
• Provide **cross-board insights** (Deals + Work Orders)  
• Show **Agent Trace** explaining internal reasoning  
• Interactive **charts and analytics**

---

# 💬 Example Questions

Users can ask questions such as:

- Show pipeline value  
- How many open deals are there?  
- Show high probability deals  
- Show deals by sector  
- Which sector has the highest pipeline value?  
- What is the average deal size?  
- Show pipeline health  
- How many work orders exist?

---

# 🧠 System Architecture

The system consists of three main components:

### 1. Data Retrieval
The application queries monday.com boards using the **GraphQL API**.

Two boards are used:

- Deals Board
- Work Orders Board

Board data is retrieved dynamically and converted into structured Python dictionaries.

---

### 2. Query Understanding

User questions are interpreted using **keyword-based intent detection**.

Examples:

| Keyword | Agent Action |
|-------|-------------|
| pipeline | Calculate total pipeline value |
| open deals | Count deals with "Open" status |
| sector | Aggregate deals by sector |
| probability | Identify high probability deals |
| work orders | Query operations board |

---

### 3. Business Analytics

The agent processes board data to generate insights including:

- Total pipeline value
- Sector performance
- Deal probability distribution
- Average deal size
- Operational workload

These insights are visualized through charts and dashboards.

---

# 📊 Dashboard Features

The Streamlit interface provides:

### Business Insights
- Pipeline value
- Open deals
- High probability deals
- Top sector

### Analytics Charts
- Pipeline value by sector
- Closure probability distribution

### Agent Trace
Displays the internal reasoning steps of the AI agent:

- Interpreting user query
- Querying monday API
- Cleaning board data
- Generating business insights

### Conversation History
Tracks previous questions and answers.

---

# 🛠 Technologies Used

- **Python**
- **Streamlit**
- **monday.com GraphQL API**
- **Pandas**
- **Requests**

---

# ▶ Running the App Locally

Install the required dependencies:

```
pip install -r requirements.txt
```

Run the Streamlit application:

```
streamlit run agent_app.py
```

The dashboard will open automatically in your browser.

---

## 📂 Project Structure

```
agent_app.py        # Main Streamlit application
requirements.txt    # Python dependencies
README.md           # Project documentation
```

---

## 👩‍💻 Author

**Diksa Pal Chowdhury**  
MSc Data Science  
Chennai Mathematical Institute

Install dependencies:
