import matplotlib.pyplot as plt

# Define parameters and their respective weightages
parameters = ["Avg Speed", "Acceleration", "Jerk", "Curvature", "Straightness", "Jitter", "Direction Changes"]
weights = [20, 10, 12, 15, 15, 15, 13]  # Corresponding weightage values

# Define colors: Darker green for higher weightage, lighter green for lower weightage
colors = ["#004d00", "#66ff66", "#33cc33", "#66ff66", "#009900", "#004d00", "#008000"]

# Set background color to match slide background (adjusted from observed tone)
background_color = "#1a1a1a"  # Darker grayish-black for better contrast

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 8), facecolor=background_color)  # Adjusted background

# Create the pie chart with matrix green theme
wedges, texts, autotexts = ax.pie(
    weights, labels=parameters, autopct='%1.1f%%', colors=colors, startangle=140,
    wedgeprops={'edgecolor': 'black'}, textprops={'color': "#00ff00", 'fontsize': 12}
)

# Change the numerical weightage to black for contrast
for autotext in autotexts:
    autotext.set_color("black")

# Set title with matrix green color
plt.title("Bot Detection Parameter Weight Distribution", fontsize=14, color="#00ff00")

# Show the chart
plt.show()
