import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Fuel Monitoring Dashboard")

df = pd.read_csv("data.csv")

df["smoothed_fuel"] = df["fuel"].rolling(3).mean()
df["change"] = df["smoothed_fuel"].diff()
df["drop_flag"] = df["change"]<-3
df["confirmed_drop"]=df["drop_flag"] & df["drop_flag"].shift(1)
df["increase_flag"]= df["change"]>3
df["confirmed_increase"] = df["increase_flag"] & df["increase_flag"].shift(1)

st.subheader("Event summary")

st.write("Total Drops Detected:", df["confirmed_drop"].sum())
st.write("Total Refills Detected:", df["confirmed_increase"].sum())

if st.checkbox("Show Raw Data"):
    st.write(df)

if not df[df["confirmed_drop"]].empty:
     st.write("Sudden drops found:")
     st.write(df[df["confirmed_drop"]])

if not df[df["confirmed_increase"]].empty:
     st.write("sudden increase happened:")
     st.write(df[df["confirmed_increase"]])     

fig, ax = plt.subplots()
x= df["timestamp"]
y= df["smoothed_fuel"]
ax.plot(x,y)
ax.scatter(
     df[df["confirmed_drop"]]["timestamp"],
     df[df["confirmed_drop"]]["smoothed_fuel"],
      color="red",
      label="drop"
     )

ax.scatter(
     df[df["confirmed_increase"]]["timestamp"],
     df[df["confirmed_increase"]]["smoothed_fuel"],
      color="green",
       label="Refill")
ax.tick_params(axis='x', rotation=60)
ax.set_title("Fuel Level Over Time")
ax.set_xlabel("time")
ax.set_ylabel("fuel")
ax.legend()
st.pyplot(fig)