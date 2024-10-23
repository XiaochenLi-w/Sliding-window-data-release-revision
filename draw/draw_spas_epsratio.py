#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

#plt.rcParams['pdf.use14corefonts'] = True
font = {'family': 'Helvetica'}
plt.rc('font', **font)

#plt.style.use("seaborn-whitegrid")
sns.set_style("whitegrid")
# -------------------------------------------------------
color_list = sns.color_palette("deep", 8)
fig = plt.figure(figsize=(10, 3))

ax1 = plt.subplot(1, 2, 1)
size = 5
x_label = ['Otp', 'Dth', 'Uem', 'Syn1', 'Syn2']
x = np.arange(size)

eps4 = [0.1156419372001547, 4.822941332230727, 0.23249906132973716, 1.1790809861168394, 1.8465253293071284]
eps3 = [0.13643183327952557, 4.341798444699267, 0.25079613135494033, 1.148763508895514, 2.06095555977867]
eps2 = [0.17036190950061603, 5.882121126047221, 0.2945362281933583, 1.2926718883829338, 2.108964741835579]

total_width, n = 0.8, 3
width = total_width / n
x = x - (total_width - width) / 2

l1 = ax1.bar(x, eps4,  width=width, color=color_list[0], label='w')
l2 = ax1.bar(x + width, eps3, width=width, color=color_list[1], label='2w')
l3 = ax1.bar(x + 2 * width, eps2, width=width, color=color_list[2], label='3w')
# l4 = ax1.bar(x + 3 * width, BufferLdp_ndcg, width=width, color=color_list[3], label='BufferLdpPD')
plt.xticks(x + 0.25, x_label, rotation=0)
ax1.set_ylabel("MRE", fontsize=14)
ax1.set_xlabel("One-dimensional datasets", fontsize=12)

ax2 = plt.subplot(1, 2, 2)
size2 = 5
x_label2 = ['Fmd', 'Tdv', 'Syn3', 'Syn4', 'Ret']
x2 = np.arange(size2)

x2 = x2 - (total_width - width) / 2


eps4_multi = [5.387654092939334, 1.1663210447896735, 0.14368105016407587, 0.21858722760575872, 11.033251205585389]
eps3_multi = [6.530666041810166, 1.20993685055941, 0.17892910915493915, 0.3095433754808183, 15.809794215546162]
eps2_multi = [7.5376991324858835, 1.2080484186224725, 0.2588924976163684, 0.31857137920149786, 21.95010704577332]

ax2.bar(x2, eps4_multi,  width=width, color=color_list[0], label='w')
ax2.bar(x2 + width, eps3_multi, width=width, color=color_list[1], label='2w' )
ax2.bar(x2 + 2 * width, eps2_multi, width=width, color=color_list[2], label='3w')
#ax2.bar(x + 3 * width, BufferLdp_re, width=width, color=color_list[3], label='BufferLdpPD')
plt.xticks(x2 + 0.25, x_label2, rotation=0)
ax2.set_ylabel("MRE", fontsize=14)
ax2.set_xlabel("Multi-dimensional datasets", fontsize=12)

# fig.legend(loc='center', bbox_to_anchor=(0.25, 0.78), ncol=1, prop={'size': 10}, frameon=True, edgecolor='gray')
legend_list = [r'$\epsilon_s/\epsilon_p=1/3$', r'$\epsilon_s/\epsilon_p=1/2$', r'$\epsilon_s/\epsilon_p=1/1$']
fig.legend([l1, l2, l3], labels=legend_list, loc='upper center', bbox_to_anchor=(0.5, 0.99),
           ncol=4, prop={'size': 12}, frameon=True, edgecolor='gray')
fig.tight_layout()
fig.subplots_adjust(left=0.076, bottom=0.147, right=0.96, top=0.844, wspace=0.236, hspace=0.2)

plt.show()
# ----------------------------------------------

fig.savefig("./fig/sup_fig/spas_eps_ratio.pdf")