import matplotlib.pyplot as  plt 
import numpy as np

# Plotting a scatter plot
X_data = np.random.random(50000) * 100
Y_data = np.random.random(50000) * 100

# plt.scatter(X_data, Y_data, c = "red", marker = "*", s = 150, alpha=0.01)
#   - You can specify what shape each of the point in the scatter plot is using marker
#   - You can specify the size of the marker using s
#   - You can define the opacity using the alpha command

# Plotting a line chart
Years = [x + 2000 for x in range(20)]
Weight = np.random.random(20) * 300
# plt.plot(Years, Weight, c = "g", lw = 3, linestyle = "--")
#   A specific paramter for this plot is the line style plot which allows you to specify how the liens will be graphed

# Plotting a bar chart
languages = ["C++", "Python", "Java", "JavaScript", "C", "Dart"]
votes = [20, 3, 40, 5, 12, 15,]
# plt.bar(languages, votes, align="edge", color = "red", width = 0.5, edgecolor = "green", lw = 6)
#   - align : this argument specifies where the key for each abr is placed, whether in the center or in the endge
#   - color : this argument specifies the fill color of each bar in the bar chart
#   - width : this argument specifies the width of the bars in tbe bar chart
#   - edgecolor : this argument specifies the color of the edges of each b ar
#   - lw : this argument specifies the width of the edges of each bar in the bar chart

# Pie Chart
#plt.pie(votes, labels=languages, autopct = "%.3f%%")
# - label : this is where you provide all the x values
# - autopct : this argument allows us to add a percent for each of the labels in the pie chart

# Plotting a histogram
Ages = np.random.normal(20, 5, 1000)
#plt.hist(Ages)
# - bins : this argument allows you to either specify a number x wich dictates how many bings the histogram has. Or we can provide a list which specifies what the values ofr the bings are

# PLOT Customization

#plt.plot(Years, Weight, linestyle = "--") # plotting a line plot
#plt.title("Change in Weight of US Population", fontsize = 15)
#plt.xlabel("Year")
#plt.ylabel("Weight of person")
#plt.yticks(Weight, [f"${x}KG" for x in Weight])

# Legends

#Tesla_Stock = np.random.random(10) * 100
#Ford_Stock = np.random.random(10) * 100
#GM_Stock = np.random.random(10) * 100

#plt.plot(Tesla_Stock, label = "Tesla")
#plt.plot(Ford_Stock, label = "Ford")
#plt.plot(GM_Stock, label = "GM")

#plt.legend()

# MULTIPLE PLOTS


# Show the results

plt.show()
