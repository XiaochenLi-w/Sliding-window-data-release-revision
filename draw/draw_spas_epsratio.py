#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

#plt.rcParams['pdf.use14corefonts'] = True
font = {'family': 'Helvetica'}
plt.rc('font', **font)

plt.style.use("seaborn-whitegrid")
# -------------------------------------------------------
color_list = sns.color_palette("deep", 8)
fig = plt.figure(figsize=(10, 3))

ax1 = plt.subplot(1, 2, 1)
size = 5
x_label = ['Otp', 'Dth', 'Uem', 'Syn1', 'Syn2']
x = np.arange(size)

eps4 = [0.11574866755631456, 3.6141724957730013, 0.2312265132608991, 2.2754169515714127, 0.9603696815074445]
eps3 = [0.1341345712917069, 4.14748191164041, 0.23964033889305708, 2.21574417681664, 1.0434047788597902]
eps2 = [0.16545365901803483, 4.132644635246499, 0.25930945401063815, 2.3517538568958503, 1.1296736698254388]

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
size2 = 4
x_label2 = ['Fmd', 'Tdv', 'Syn3', 'Ret']
x2 = np.arange(size2)

x2 = x2 - (total_width - width) / 2

eps4_multi = [5.900422183059485, 1.274864224640938, 0.13737782355213402, 11.105368492320414]
eps3_multi = [6.3048447746193865, 1.202567030574346, 0.1800245992061557, 15.862860768591549]
eps2_multi = [7.954213103242671, 1.2170208695468538, 0.26359102236625503, 22.165302467404224]

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

fig.savefig("./fig/spas_eps_ratio.pdf")