import matplotlib
import matplotlib.pyplot as plt
import numpy as np

labels = ["Perceived \nSpeed", "Perceived \nAccuracy", "Fatigue", "Overall \nPreference"]
# hv_avg = [3.58,3.17,2,3.25]
# hv_std = [0.90,0.72,0.85,1.14]

# pl_avg = [3.08,3.25,3.67,3.58]
# pl_std = [0.79,0.97,0.78,0.79]

pp_avg = [4.5,4.3,3.5,4.6]
pp_std = [0.527,0.67,0.85,0.52]

rc_avg = [2.6,2.8,3.3,2.8]
rc_std = [0.84, 1.23,0.95,1.14]

ge_avg = [3.8,3.5,3.4,3.6]
ge_std = [0.63, 0.527,0.699,0.516]

font = {'family' : 'Arial',
    'weight' : 'bold',
    }

x = np.arange(len(labels))  # the label locations
print(x)
width = 0.25  # the width of the bars

fig, ax = plt.subplots()

fig.set_figwidth(6.5)
fig.set_figheight(4 * 0.75)

ax.set_ylim(0, 5.2)

ax.yaxis.grid(True)
ax.set_axisbelow(True)

rects3 = ax.bar(x - width, pp_avg, width, label='PalmPad', color="#e24a33")
rects2 = ax.bar(x, ge_avg, width, label='General', color="#348abd")
rects1 = ax.bar(x + width, rc_avg, width, label='Rectangle', color="#238e23")



ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.errorbar(x-width, pp_avg, yerr = pp_std, fmt = 's', capsize = 5, elinewidth = 2.5, capthick = 2.5, antialiased = True, color="black")
ax.errorbar(x, ge_avg, yerr = ge_std, fmt = 's', capsize = 5, elinewidth = 2.5, capthick = 2.5, antialiased = True, color="black")
ax.errorbar(x+width, rc_avg, marker='s',yerr = rc_std, fmt = 's', linewidth = 2.5, capsize = 5, elinewidth = 2.5, capthick = 2.5, antialiased = True, zorder = 2, color="black")





# ax.xaxis.set_axisline_style("->", size = 1.0)
# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Subjective Rating', font, fontsize=15)
# ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels, font, fontsize=15)
ax.set_yticklabels([0,1,2,3,4,5], font, fontsize=15)
ax.legend(frameon = False, prop = {'family': 'Arial', 'style':'italic', 'weight':'bold', 'size':16}, handlelength = 1, bbox_to_anchor=(0.96,0.8))


# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')


# autolabel(rects1)
# autolabel(rects2)

fig.tight_layout()

plt.show()
plt.savefig('rating.png', bbox_inches = 'tight')
# label = ["Perceived Speed", "Perceived Accuracy", "Fatigue", "Overall"]
# hv_avg = [3.58,3.17,2,3.25]
# hv_std = [0.90,0.72,0.85,1.14]

# pl_avg = [3.08,3.25,3.67,3.58]
# pl_std = [0.79,0.97,0.78,0.79]
