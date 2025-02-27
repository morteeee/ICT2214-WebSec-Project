import matplotlib.pyplot as plt

# Define categories and their corresponding score ranges
categories = ["Basic Bot", "Intermediate Bot", "Advanced Bot (Human-like)"]
score_ranges = ["0-50", "51-69", "70-100"]
score_widths = [50, 19, 31]  # Heights of each score range
score_starts = [0, 51, 70]  # Starting values of score ranges

# Define colors (darker green for higher categories, lighter green for lower ones)
colors = ["#66ff66", "#008000", "#004d00"]

# Create a stacked vertical bar chart
fig, ax = plt.subplots(figsize=(3, 8), facecolor="black")

# Plot each category as a segment in the stacked bar
bottom = 0
for i in range(len(categories)):
    ax.bar(1, score_widths[i], color=colors[i], edgecolor="black", bottom=bottom, width=0.3)
    bottom += score_widths[i]

# Add labels inside the bars with category and score range
bottom = 0
for i in range(len(categories)):
    ax.text(1, bottom + score_widths[i] / 2, f"{categories[i]}\n({score_ranges[i]})",
            fontsize=12, fontweight="bold", color="black", va="center", ha="center")

    bottom += score_widths[i]

# Customize the chart appearance
ax.set_xticks([])  # Remove x-axis labels
ax.set_yticks(range(0, 101, 10))  # Y-axis ticks from 0 to 100
ax.set_yticklabels(range(0, 101, 10), color="#00ff00")  # Set tick label color
ax.set_ylim(0, 100)  # Limit y-axis from 0 to 100
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.spines["left"].set_visible(False)

# Set title with neon green color
plt.title("Bot Detection Categorization", fontsize=14, color="#00ff00")

# Add label for y-axis
ax.set_ylabel("Score Range", fontsize=12, color="#00ff00")

# Show the corrected stacked bar graph
plt.show()
