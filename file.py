import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")

df["smoothed_fuel"] = df["fuel"].rolling(3).mean()
df["change"] = df["smoothed_fuel"].diff()
df["drop_flag"] = df["change"]<-3
df["confirmed_drop"]=df["drop_flag"] & df["drop_flag"].shift(1)
df["increase_flag"]= df["change"]>3
df["confirmed_increase"] = df["increase_flag"] & df["increase_flag"].shift(1)
    
if not df[df["confirmed_drop"]].empty:
     print("Sudden drops found:")
     print(df[df["confirmed_drop"]])

if not df[df["confirmed_increase"]].empty:
     print("sudden increase happened:")
     print(df[df["confirmed_increase"]])     

x= df["timestamp"]
y= df["smoothed_fuel"]
plt.plot(x,y)
plt.scatter(
     df[df["confirmed_drop"]]["timestamp"],
     df[df["confirmed_drop"]]["smoothed_fuel"],
      color="red",
      label="drop"

     )
plt.scatter(
     df[df["confirmed_increase"]]["timestamp"],
     df[df["confirmed_increase"]]["smoothed_fuel"],
      color="green",
       label="Refill")
plt.xticks(rotation=60)
plt.title("Fuel Level Over Time")
plt.xlabel("time")
plt.ylabel("fuel")
plt.legend()
plt.show()