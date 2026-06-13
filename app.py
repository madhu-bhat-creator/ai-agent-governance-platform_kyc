import streamlit as st
from openai import OpenAI

st.set_page_config(layout="wide")

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

st.title("AI KYC Agent Governance Simulator")

case = st.text_area(
    "KYC Remediation Case",
    value="Customer 12345 missing beneficial owner information"
)

policy = st.selectbox(
    "Policy",
    [
        "Traditional Broad Access",
        "Zero Standing Privilege + JIT"
    ]
)

if st.button("Run Agent"):

    prompt = f"""
    You are a KYC remediation AI agent.

    KYC Case:
    {case}

    Policy:
    {policy}

    Provide:

    Issue
    Action
    Remediation
    Scope
    Access
    Duration
    Risk

    Keep response concise.
    """

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    st.subheader("Agent Analysis")

    st.write(
        response.choices[0].message.content
    )

    st.subheader("Business Impact")

    if policy == "Traditional Broad Access":

        st.error(
            "Potential Exposure: 1,000,000 Customer Records"
        )

    else:

        st.success(
            "Potential Exposure: 1 Customer Record"
        )

    st.subheader("Policy Comparison")

    st.table({
        "Attribute":[
            "Scope",
            "Duration",
            "Risk"
        ],
        "Traditional":[
            "All Customers",
            "Permanent",
            "High"
        ],
        "ZSP + JIT":[
            "Customer 12345",
            "60 Minutes",
            "Low"
        ]
    })
