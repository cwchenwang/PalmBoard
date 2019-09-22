import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import MaxNLocator

def draw(pl_avg, pl_se, hv_avg, hv_se):
    # plt.rcParams["font.family"] = "Times New Roman"
    # plt.rcParams["font.weight"] = "bold"
    plt.style.use('seaborn')
    plt.rcParams['savefig.dpi'] = 600 #图片像素
    # plt.set_size_inches(18.5, 10.5)
    # plt.rcParams['figure.dpi'] = 200 #分辨率
    font = {'family' : 'Arial',
        'weight' : 'bold',
        }
    # matplotlib.rc('font', **font)
    f = plt.figure()
    f.set_figwidth(6)
    f.set_figheight(4 * 0.75)
    ax = f.gca()

    # ax.axis[:].set_visible(True)
    
    ax.plot([1,2,3,4], hv_avg, '-o', markerfacecolor='w', color = '#348abd', linewidth = 2.5, markersize = 5.5, markeredgewidth = 2.5, label = 'Hover', antialiased = True, zorder = 1)
    ax.plot([1,2,3,4], pl_avg, '-s', markerfacecolor='w', color = '#e24a33', linewidth = 2.5, markersize = 5.5, markeredgewidth = 2.5, label = 'Placed', antialiased = True, zorder = 2)
    
    ax.errorbar([1,2,3,4], pl_avg, yerr = pl_se, fmt = 's', color = '#e24a33', markerfacecolor='w', linewidth = 2.5, capsize = 5, elinewidth = 2.5, capthick = 2.5, markersize = 6, markeredgewidth = 2.5, antialiased = True, zorder = 2)
    ax.errorbar([1,2,3,4], hv_avg, yerr = hv_se, fmt = 'o', color = '#348abd', markerfacecolor='w', linewidth = 2.5, capsize = 5, elinewidth = 2.5, capthick = 2.5, markersize = 6, markeredgewidth = 2.5, antialiased = True, zorder = 1)
    
    
    plt.legend(loc = 'lower right', frameon = False, prop = {'family': 'Arial', 'style':'italic', 'weight':'bold', 'size':16}, handlelength = 1, bbox_to_anchor=(0.8, 0.08))
    ax.grid(linestyle = '-', axis = 'y')
    yminorLocator = matplotlib.ticker.MultipleLocator(10)
    # ax.yaxis.grid(True, which = 'minor', linestyle = '--')
    # ax.yaxis.grid(True, which = 'major', linestyle = '-')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_major_locator(yminorLocator)
    # ax.tick_params(top = False, bottom = False, left = False, right = False)
    ax.set_xticks([1,2,3,4])
    # ax.set_ylim(0, 1.2)
    ax.set_ylim(0, 50)
    # ax.set_title("Time cost of blindcommand and\n speech in 4 sessions", fontsize = 14)
    plt.ylabel('Speed (WPM)', font, fontsize = 15)
    plt.xlabel('Block', font, fontsize = 15)
    label = ax.set_xlabel('Block', fontsize = 15)
    ax.xaxis.set_label_coords(0.5, -0.1)

    plt.yticks(fontweight = 'bold', fontfamily = 'Cambria', fontsize = 15)
    plt.xticks(fontweight = 'bold', fontfamily = 'Cambria', fontsize = 15)
    plt.tick_params(labelsize = 15, length = 0)
    # plt.savefig('final.png', bbox_inches = 'tight')
    plt.savefig('eva-cer.png', bbox_inches = 'tight')

# hv_avg = [34.58, 34.17, 34.75, 34.67]
# hv_se = [12.41, 12.36, 11.27, 10.67]

# pl_avg = [30.58, 34, 35.5, 36.42]
# pl_se = [9.40, 11.29, 11.18, 9.64]

# pp_avg = [31.10,31.97,34.24,32.73,34.02]
# pp_std = [5.01, 5.14,4.49,5.27,5.22]
# rc_avg = [22.19,22.71,23.99,23.57,24.899]
# rc_std = [5.07,5.27,4.79,5.43,5.29]
# ge_avg = [25.96,28.23,28.04,29.53,30.29]
# ge_std = [5.50,6.63,5.61,5.79,4.57]

pp_avg = [0.56,0.79,0.278,0.87,0.52]
pp_std = [1.188,1.28,0.89,1.9,1.11]
rc_avg = [1.9,2.39,2.22,2.5,1.35]
rc_std = [2.9,1.9,3.657,4.11,2.63]
ge_avg = [2.56,1.9,1.35,1.45,1.0965]
ge_std = [4.14,0.022,1.9,2.45,1.9]

plt.style.use('seaborn')
plt.rcParams['savefig.dpi'] = 600 #图片像素
# plt.set_size_inches(18.5, 10.5)
# plt.rcParams['figure.dpi'] = 200 #分辨率
font = {'family' : 'Arial',
    'weight' : 'bold',
    }
# matplotlib.rc('font', **font)
f = plt.figure()
f.set_figwidth(6)
f.set_figheight(4 * 0.75)
ax = f.gca()

# ax.axis[:].set_visible(True)]
ax.plot([1,2,3,4,5], pp_avg, '-s', markerfacecolor='w', color = '#e24a33', linewidth = 2.5, markersize = 5.5, markeredgewidth = 2.5, label = 'PalmPad', antialiased = True, zorder = 2)
ax.plot([1,2,3,4,5], ge_avg, '-o', markerfacecolor='w', color = '#348abd', linewidth = 2.5, markersize = 5.5, markeredgewidth = 2.5, label = 'General', antialiased = True, zorder = 1)
ax.plot([1,2,3,4,5], rc_avg, '-v', markerfacecolor='w', color = '#238323', linewidth = 2.5, markersize = 5.5, markeredgewidth = 2.5, label = 'Rectangle', antialiased = True, zorder = 1)



ax.errorbar([1,2,3,4,5], rc_avg, yerr = rc_std, fmt = 'v', color = '#238e23', markerfacecolor='w', linewidth = 2.5, capsize = 5, elinewidth = 2.5, capthick = 2.5, markersize = 6, markeredgewidth = 2.5, antialiased = True, zorder = 2)
ax.errorbar([1,2,3,4,5], pp_avg, yerr = pp_std, fmt = 's', color = '#e24a33', markerfacecolor='w', linewidth = 2.5, capsize = 5, elinewidth = 2.5, capthick = 2.5, markersize = 6, markeredgewidth = 2.5, antialiased = True, zorder = 2)
ax.errorbar([1,2,3,4,5], ge_avg, yerr = ge_std, fmt = 'o', color = '#348abd', markerfacecolor='w', linewidth = 2.5, capsize = 5, elinewidth = 2.5, capthick = 2.5, markersize = 6, markeredgewidth = 2.5, antialiased = True, zorder = 1)


plt.legend(loc = 'lower right', frameon = False, prop = {'family': 'Arial', 'style':'italic', 'weight':'bold', 'size':12}, handlelength = 1, bbox_to_anchor=(1.02, 0.6))
ax.grid(linestyle = '-', axis = 'y')
yminorLocator = matplotlib.ticker.MultipleLocator(2)
# ax.yaxis.grid(True, which = 'minor', linestyle = '--')
# ax.yaxis.grid(True, which = 'major', linestyle = '-')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.yaxis.set_major_locator(yminorLocator)
# ax.tick_params(top = False, bottom = False, left = False, right = False)
ax.set_xticks([1,2,3,4,5])
ax.set_ylim(-2, 8)
# ax.set_ylim(-0.2, 1, 0.1)
# ax.set_title("Time cost of blindcommand and\n speech in 4 sessions", fontsize = 14)
plt.ylabel('CER (%)', font, fontsize = 15)
plt.xlabel('Block', font, fontsize = 15)
label = ax.set_xlabel('Block', fontsize = 15)
ax.xaxis.set_label_coords(0.5, -0.1)

plt.yticks(fontweight = 'bold', fontfamily = 'Cambria', fontsize = 15)
plt.xticks(fontweight = 'bold', fontfamily = 'Cambria', fontsize = 15)
plt.tick_params(labelsize = 15, length = 0)
# plt.savefig('final.png', bbox_inches = 'tight')
plt.savefig('eva-cer.png', bbox_inches = 'tight')

# draw(pl_avg, pl_se, hv_avg, hv_se)