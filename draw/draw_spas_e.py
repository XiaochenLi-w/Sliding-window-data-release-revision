#!/usr/bin/env python
# -*- coding:utf-8 -*-
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

#plt.rcParams['pdf.use14corefonts'] = True
font = {'family': 'Helvetica'}
plt.rc('font', **font)

#plt.style.use("whitegrid")
sns.set_style("whitegrid")
# -------------------------------------------------------
color_list = sns.color_palette("deep", 8)
fig = plt.figure(figsize=(10, 3))

ax1 = plt.subplot(1, 2, 1)
size = 5
x_label = ['Otp', 'Dth', 'Uem', 'Syn1', 'Syn2']
x = np.arange(size)

windownum2 = [0.12027366155246104, 7.263642709548162, 0.29051772786339236, 1.1464672119894657, 1.7740705889604715]
windownum3 = [0.11732655032093253, 4.224630990801481, 0.26923438744957023, 1.1813466173784053, 1.8843206879101788]
windownum4 = [0.11584356618612938, 4.26575093539004, 0.24051277399916876, 1.1481979590783786, 1.8590503861789203]

total_width, n = 0.8, 3
width = total_width / n
x = x - (total_width - width) / 2

l1 = ax1.bar(x, windownum2,  width=width, color=color_list[0], label='w')
l2 = ax1.bar(x + width, windownum3, width=width, color=color_list[1], label='2w')
l3 = ax1.bar(x + 2 * width, windownum4, width=width, color=color_list[2], label='3w')
# l4 = ax1.bar(x + 3 * width, BufferLdp_ndcg, width=width, color=color_list[3], label='BufferLdpPD')
plt.xticks(x + 0.25, x_label, rotation=0)
ax1.set_ylabel("MRE", fontsize=14)
ax1.set_xlabel("One-dimensional datasets", fontsize=12)

ax2 = plt.subplot(1, 2, 2)
size2 = 5
x_label2 = ['Fmd', 'Tdv', 'Syn3', 'Syn4', 'Ret']
x2 = np.arange(size2)

x2 = x2 - (total_width - width) / 2

windownum2_multi = [5.130512771418071, 1.227024354781636, 0.1404563133535414, 0.23908825202517114, 11.055262106679859]
windownum3_multi = [5.466383183267233, 1.2160921052760938, 0.1392640170090202, 0.2002502632015119, 11.027491158413973]
windownum4_multi = [5.656299975822682, 1.2182285416895808, 0.1400407675700451, 0.21178313356139963, 11.068647070643609]

ax2.bar(x2, windownum2_multi,  width=width, color=color_list[0], label='w')
ax2.bar(x2 + width, windownum3_multi, width=width, color=color_list[1], label='2w' )
ax2.bar(x2 + 2 * width, windownum4_multi, width=width, color=color_list[2], label='3w')
#ax2.bar(x + 3 * width, BufferLdp_re, width=width, color=color_list[3], label='BufferLdpPD')
plt.xticks(x2 + 0.25, x_label2, rotation=0)
ax2.set_ylabel("MRE", fontsize=14)
ax2.set_xlabel("Multi-dimensional datasets", fontsize=12)

# fig.legend(loc='center', bbox_to_anchor=(0.25, 0.78), ncol=1, prop={'size': 10}, frameon=True, edgecolor='gray')
legend_list = ['w', '2w', '3w']
fig.legend([l1, l2, l3], labels=legend_list, loc='upper center', bbox_to_anchor=(0.5, 0.99),
           ncol=4, prop={'size': 12}, frameon=True, edgecolor='gray')
fig.tight_layout()
fig.subplots_adjust(left=0.076, bottom=0.147, right=0.96, top=0.844, wspace=0.236, hspace=0.2)

plt.show()
# ----------------------------------------------

fig.savefig("./fig/sup_fig/spas_windownum.pdf")