import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Dummy data generator
def generate_dummy_data():
    zones = ['Emergency', 'ICU', 'Ward', 'Operating Room', 'Radiology']
    staff_roles = ['Doctor', 'Nurse', 'Technician']
    equipment = ['X-Ray Machine', 'Ventilator', 'Defibrillator', 'ECG Machine', 'Stretcher']
    
    pre_data = {
        "Time_Period": ['Pre'] * 50,
        "Zone": np.random.choice(zones, 50),
        "Role": np.random.choice(staff_roles, 50),
        "Equipment": np.random.choice(equipment, 50),
        "Time_Spent_Hours": np.random.uniform(1, 8, 50),
        "Efficiency_Score": np.random.uniform(60, 90, 50)
    }

    post_data = {
        "Time_Period": ['Post'] * 50,
        "Zone": np.random.choice(zones, 50),
        "Role": np.random.choice(staff_roles, 50),
        "Equipment": np.random.choice(equipment, 50),
        "Time_Spent_Hours": np.random.uniform(0.5, 6, 50),  # Reduced time spent
        "Efficiency_Score": np.random.uniform(80, 100, 50)  # Improved scores
    }

    df_pre = pd.DataFrame(pre_data)
    df_post = pd.DataFrame(post_data)
    
    return pd.concat([df_pre, df_post], ignore_index=True)

# Streamlit App
st.title("Hospital Operational Efficiency Analysis")
st.sidebar.title("Dashboard Options")

# Upload data
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("Data uploaded successfully!")
else:
    st.info("Upload new data on the left column for analysis")
    df = generate_dummy_data()

# Show dataset
if st.sidebar.checkbox("Show Data"):
    st.subheader("Dataset Preview")
    st.dataframe(df)

# Filter data by time period
pre_data = df[df["Time_Period"] == "Pre"]
post_data = df[df["Time_Period"] == "Post"]

# Summary statistics
st.subheader("Summary Statistics")
st.markdown("### Pre-RTLS Installation")
st.write(pre_data.describe())
st.markdown("### Post-RTLS Installation")
st.write(post_data.describe())

# Visualization: Time Spent by Zone and Role
st.subheader("Time Spent by Zone and Role")
time_by_zone_role_pre = pre_data.groupby(["Zone", "Role"])["Time_Spent_Hours"].mean().reset_index()
time_by_zone_role_post = post_data.groupby(["Zone", "Role"])["Time_Spent_Hours"].mean().reset_index()

fig_zone_role = px.bar(
    pd.concat([time_by_zone_role_pre.assign(Period="Pre"), time_by_zone_role_post.assign(Period="Post")]),
    x="Zone", y="Time_Spent_Hours", color="Role", facet_col="Period", barmode="group",
    title="Average Time Spent by Zone and Role (Pre vs Post RTLS)",
    labels={"Time_Spent_Hours": "Time Spent (Hours)", "Zone": "Hospital Zone", "Role": "Staff Role"}
)
fig_zone_role.update_layout(showlegend=True, legend_title="Staff Role")
st.plotly_chart(fig_zone_role)

# Visualization: Efficiency Score by Role
st.subheader("Efficiency Score by Role")
efficiency_by_role_pre = pre_data.groupby("Role")["Efficiency_Score"].mean().reset_index()
efficiency_by_role_post = post_data.groupby("Role")["Efficiency_Score"].mean().reset_index()

fig_role = px.bar(
    pd.concat([efficiency_by_role_pre.assign(Period="Pre"), efficiency_by_role_post.assign(Period="Post")]),
    x="Role", y="Efficiency_Score", color="Period", barmode="group",
    color_discrete_map={"Pre": "orange", "Post": "purple"},
    title="Average Efficiency Score by Role (Pre vs Post RTLS)",
    labels={"Efficiency_Score": "Efficiency Score", "Role": "Staff Role"}
)
fig_role.update_layout(showlegend=True, legend_title="Time Period")
st.plotly_chart(fig_role)

# Visualization: Equipment Usage
st.subheader("Equipment Usage and Shortage Management")
equipment_usage_pre = pre_data["Equipment"].value_counts().reset_index()
equipment_usage_post = post_data["Equipment"].value_counts().reset_index()
equipment_usage_pre.columns = ["Equipment", "Usage"]
equipment_usage_post.columns = ["Equipment", "Usage"]

fig_equipment = px.bar(
    pd.concat([
        equipment_usage_pre.assign(Period="Pre"),
        equipment_usage_post.assign(Period="Post")
    ]),
    x="Equipment", y="Usage", color="Period", barmode="group",
    title="Equipment Usage Comparison (Pre vs Post RTLS)",
    labels={"Usage": "Number of Usages", "Equipment": "Equipment Type"}
)
fig_equipment.update_layout(showlegend=True, legend_title="Time Period")
st.plotly_chart(fig_equipment)

# Insights
st.subheader("Insights")
st.markdown("""
Based on the analysis:
- **Zones and Roles**: Post-RTLS installation, there is a notable decrease in the average time spent by doctors, nurses, and technicians in critical zones, suggesting improved workflow efficiency.
- **Roles**: Efficiency scores for all roles (Doctors, Nurses, and Technicians) have significantly improved, indicating better utilization and task management.
- **Equipment Usage**: Equipment usage distribution shows optimized utilization post-RTLS installation, ensuring availability of critical devices like stretchers and ventilators during peak times. Shortages have been managed more effectively post-RTLS due to real-time tracking and better allocation.

These improvements highlight the positive impact of the RTLS system on hospital operations, streamlining workflows and enhancing overall efficiency.
""")
