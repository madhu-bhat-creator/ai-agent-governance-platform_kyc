import streamlit as st
import pandas as pd
import json
from openai import OpenAI

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="AI Agent Governance Platform",
    layout="wide"
)

# -----------------------------------
# OPENAI CLIENT
# -----------------------------------

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

# -----------------------------------
# HEADER
# -----------------------------------

st.title(
    "AI Agent Governance Platform"
)

st.markdown(
    """
    Demonstrating how governance policies influence
    AI KYC remediation agent behavior,
    access decisions and risk posture.
    """
)

# -----------------------------------
# SECTION 1
# KYC CASE INPUT
# -----------------------------------

st.header("1. KYC Remediation Case")

case = st.text_area(
    "Enter KYC Case",
    value="Customer 12345 missing beneficial owner information."
)

# -----------------------------------
# SECTION 2
# POLICY SELECTION
# -----------------------------------

st.header("2. Governance Policy")

policy = st.selectbox(
    "Select Policy",
    [
        "Traditional Broad Access",
        "Role Based Access",
        "Attribute Based Access",
        "Zero Standing Privilege + JIT"
    ]
)

# -----------------------------------
# SECTION 3
# RUN AGENT
# -----------------------------------

run_agent = st.button(
    "Run Agent"
)

# -----------------------------------
# EVERYTHING BELOW RUNS
# ONLY AFTER BUTTON CLICK
# -----------------------------------

if run_agent:

    # -----------------------------------
    # OPENAI PROMPT
    # -----------------------------------

    prompt = f"""
    You are an AI KYC remediation agent.

    Case:
    {case}

    Policy:
    {policy}

    Determine:

    1. KYC Issue
    2. Required Action
    3. Required Data
    4. Recommended Remediation
    5. Customer Scope
    6. Required Privileges
    7. Access Duration
    8. Risk Score
    9. Business Justification

    Return JSON only.
    """

    # -----------------------------------
    # CALL OPENAI
    # -----------------------------------

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    result = json.loads(
        response.choices[0].message.content
    )

    # -----------------------------------
    # SECTION 4
    # AGENT WORKFLOW
    # -----------------------------------

    st.header("3. Agent Workflow")

    st.markdown("""
    KYC Case
        ↓
    Agent Analysis
        ↓
    Policy Evaluation
        ↓
    Access Decision
        ↓
    Risk Assessment
        ↓
    Remediation
        ↓
    Access Revocation
    """)

    # -----------------------------------
    # SECTION 5
    # AGENT ANALYSIS
    # -----------------------------------

    st.header("4. Agent Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("Issue")

        st.write(
            result["issue"]
        )

        st.subheader("Required Action")

        st.write(
            result["action"]
        )

    with col2:

        st.subheader("Required Data")

        st.write(
            result["required_data"]
        )

    # -----------------------------------
    # SECTION 6
    # REMEDIATION PLAN
    # -----------------------------------

    st.header("5. KYC Remediation Plan")

    st.write(
        result["remediation"]
    )

    # -----------------------------------
    # SECTION 7
    # POLICY EVALUATION
    # -----------------------------------

    st.header("6. Policy Evaluation")

    st.write(
        f"Policy Selected: {policy}"
    )

    # -----------------------------------
    # SECTION 8
    # ACCESS DECISION
    # -----------------------------------

    st.header("7. Access Decision")

    st.write(
        f"Customer Scope: {result['scope']}"
    )

    st.write(
        f"Duration: {result['duration']}"
    )

    st.subheader(
        "Granted Privileges"
    )

    for privilege in result["privileges"]:

        st.write(
            f"• {privilege}"
        )

    # -----------------------------------
    # SECTION 9
    # RISK ASSESSMENT
    # -----------------------------------

    st.header("8. Risk Assessment")

    st.metric(
        "Risk Score",
        result["risk"]
    )

    # -----------------------------------
    # SECTION 10
    # BUSINESS IMPACT
    # -----------------------------------

    st.header("9. Business Impact")

    if policy == "Traditional Broad Access":

        st.error(
            "Potential Exposure: 1,000,000 Customer Records"
        )

    elif policy == "Zero Standing Privilege + JIT":

        st.success(
            "Potential Exposure: 1 Customer Record"
        )

    # -----------------------------------
    # SECTION 11
    # COMPARISON TABLE
    # -----------------------------------

    st.header("10. Policy Comparison")

    comparison = pd.DataFrame({

        "Attribute":[
            "Customer Scope",
            "Duration",
            "Privileges",
            "Revocation",
            "Risk"
        ],

        "Traditional":[
            "All Customers",
            "Permanent",
            "Broad",
            "Manual",
            "High"
        ],

        "RBAC":[
            "Role Based",
            "Business Hours",
            "Role Scoped",
            "Manual",
            "Medium"
        ],

        "ABAC":[
            "Attribute Based",
            "Dynamic",
            "Conditional",
            "Automatic",
            "Medium-Low"
        ],

        "ZSP + JIT":[
            "Single Customer",
            "60 Minutes",
            "Minimal",
            "Automatic",
            "Low"
        ]
    })

    st.dataframe(
        comparison,
        use_container_width=True
    )

    # -----------------------------------
    # SECTION 12
    # AUDIT RECORD
    # -----------------------------------

    st.header("11. Audit Record")

    audit = pd.DataFrame({

        "Field":[
            "Policy",
            "Customer Scope",
            "Duration",
            "Risk"
        ],

        "Value":[
            policy,
            result["scope"],
            result["duration"],
            result["risk"]
        ]
    })

    st.dataframe(
        audit,
        use_container_width=True
    )

    # -----------------------------------
    # SECTION 13
    # GOVERNANCE RECOMMENDATION
    # -----------------------------------

    st.header("12. Governance Recommendation")

    st.info(
        result["justification"]
    )
