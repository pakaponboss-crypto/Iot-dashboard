import streamlit as st
import pandas as pd

st.set_page_config(page_title="IOT Dashboard", layout="wide")
st.title("💡 IOT Lighting Dashboard")

file = st.file_uploader("อัปโหลด Excel", type=["xlsx"])

if file:
    df = pd.read_excel(file)
    df.columns = df.columns.str.replace('"', '').str.strip()

    df = df.rename(columns={
        "เลขที่สัญญา": "Contract",
        "ผู้รับเหมา": "Contractor",
        "จำนวนโคม": "Lamp"
    })

    st.sidebar.header("Filter")

    if "Contractor" in df.columns:
        contractor = st.sidebar.multiselect(
            "ผู้รับเหมา",
            df["Contractor"].dropna().unique(),
            default=df["Contractor"].dropna().unique()
        )
        df = df[df["Contractor"].isin(contractor)]

    # ===== KPI =====
    st.subheader("📊 Summary")

    contract_count = df[['Contractor','Contract']].drop_duplicates() \
                        .groupby('Contractor')['Contract'].count()

    lamp_per_contract = df.drop_duplicates(subset=['Contract'])

    col1, col2 = st.columns(2)
    col1.metric("จำนวนสัญญารวม", int(contract_count.sum()))
    col2.metric("จำนวนโคมรวม", int(lamp_per_contract['Lamp'].sum()))

    # ===== Table =====
    st.subheader("จำนวนสัญญาต่อผู้รับเหมา")
    st.dataframe(contract_count.reset_index())

    st.subheader("จำนวนโคมต่อสัญญา")
    st.dataframe(lamp_per_contract[['Contract','Lamp']])

    # ===== Chart =====
    st.bar_chart(contract_count)
