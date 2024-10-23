from matplotlib import pyplot as plt
from matplotlib import font_manager
import seaborn as sns
import matplotlib.colors as mcolors
import numpy as np
# import pandas as pd


def draw_heat_w():
    # print(error[0])
    eval = "w"

    font = {'family': 'Times New Roman', 'weight': 'bold'}

    fig, axes_l = plt.subplots(nrows=1, ncols=2, sharey="row")  # figsize=(10,4)
    fig.set_size_inches(7, 4)

    a = [[0.07306696, 0.65760266, 1.82667405, 3.58028113, 5.91842391], [0.22325144628099175 ,0.10960044270833334 ,0.07306696180555555 ,0.05480022135416667 ,0.043840177083333334]]
    b = [[0.00114448, 0.01030028, 0.0286119, 0.05607932, 0.09270256], [0.0034544863861386142 ,0.0017062656249999999 ,0.00114447601010101 ,0.0008531328124999999 ,0.00068250625]]
    c = [[0.00185205, 0.01666844, 0.04630122, 0.09075038, 0.15001594], [0.005538791322314049 ,0.0027780729166666665 ,0.001852048611111111 ,0.0013890364583333333 ,0.0011112291666666668]]
    d = [[0.00715682, 0.06441137, 0.17892047, 0.35068413, 0.57970233], [0.021470456827309237 ,0.010775787550403225 ,0.0071568189424364125 ,0.0053878937752016125 ,0.004359558673469388]]
    e = [[0.014076568775100403 ,0.12668911897590363 ,0.35191421937751005 ,0.6897518699799197 ,1.1402020707831324], [0.0422297063253012 ,0.021114944556451614 ,0.014076568775100403 ,0.010557472278225807 ,0.00844883418367347]]
    f = [[0.00283714, 0.02553424, 0.07092845, 0.13901976, 0.22980817], [0.008601259066731143 ,0.00430062953336557 ,0.002837137911371782 ,0.0021331287055335975 ,0.0016907794191919191]]
    g = [[8.89655921e-05, 8.00690329e-04, 2.22413980e-03, 4.35931401e-03, 7.20621296e-03], [0.0002674954501065341 ,0.00013374772505326705 ,8.896559207375478e-05 ,6.687386252663353e-05 ,5.383363970588235e-05]]
    h = [[0.0700749656961178 ,0.6306746912650603 ,1.751874142402945 ,3.4336733191097717 ,5.676072221385541], [0.2102248970883535 ,0.1055333587449597 ,0.0700749656961178 ,0.05276667937247985 ,0.04272675102040817]]
    ii = [[0.13907095046854084 ,1.2516385542168675 ,3.476773761713521 ,6.814476572958499 ,11.264746987951805], [0.4172128514056225 ,0.20850176411290322 ,0.13907095046854084 ,0.10425088205645161 ,0.083472125]]
    gg = [[0.11730010335648147 ,1.055700930208333 ,2.9325025839120364 ,5.747705064467591 ,9.501308371874996], [0.3519003100694444 ,0.17595015503472225 ,0.11730010335648147 ,0.08764616956676134 ,0.0703800620138889]]

    for j, ax in enumerate(axes_l):

        dataf = np.array([a[j], b[j], c[j], d[j], e[j], f[j], g[j], h[j], ii[j], gg[j]])

        ax.tick_params(left=False, right=False)
        if j == 0:
            ax.set_ylabel('Datasets', fontsize=12)
            datalist_shortname = ["Otp", "Dth", "Uem", "Syn1", "Syn2", "Fmd", "Tdv", "Syn3", "Syn4", "Ret"]
            ax.set_yticks([i for i in range(len(datalist_shortname))])
            ax.tick_params(left=True, right=False)
            ax.set_yticklabels(datalist_shortname, fontsize=10, fontdict=font)
        
        if j == 0:
            ax.set_xlabel('$\epsilon$', fontsize=15, fontdict=font)
        else:
            ax.set_xlabel('w', fontsize=15, fontdict=font)

        ax.set_xticks([0, 1, 2, 3, 4])
        for edge, spine in ax.spines.items():
            spine.set_visible(False)
        
        if j == 0:
            ax.set_xticklabels([0.1, 0.3, 0.5, 0.7, 0.9], fontsize=10, fontdict=font)
        else:
            ax.set_xticklabels([40, 80, 120, 160, 200], fontsize=10, fontdict=font)
        ax.grid(which="minor", color="w", linestyle="-", linewidth=3)

        norm1 = mcolors.LogNorm(vmin=1e-3, vmax=10)
        # im = ax.imshow(dataf, cmap='YlGn', norm=norm1, aspect=0.5) # YlGn
        im = ax.imshow(dataf, cmap='BuGn', norm=norm1, aspect=0.5)  # YlGn

        for m in range(dataf.shape[1]):
            for n in range(dataf.shape[0]):
                text = ax.text(m, n, round(dataf[n, m], 2) if dataf[n, m] <= 1 else ">1",
                                horizontalalignment="center",
                                verticalalignment="center",
                                color="black" if dataf[n, m] <= 1e-1 else "w", fontsize=10, fontdict=font)
    
    cax1 = fig.add_axes([0.82, 0.23, 0.01, 1 * ax.get_position().height])
    clb1 = fig.colorbar(im, ax=axes_l, fraction=0.03, pad=0.1, cax=cax1)
    for l in clb1.ax.yaxis.get_ticklabels():
        l.set_family('Times New Roman')
        l.set_fontweight('bold')
 
    fig.subplots_adjust(left=0.076, bottom=0.258, right=0.813, top=0.775, wspace=0.1, hspace=0.1)

    plt.show()
    fig.savefig("./fig/sup_fig/dataset.pdf")

    # fig.savefig("D:/W-dp-Streaming-Data-Publish-main/new_fig/" + "heat_color_w" + "_" + eval + ".pdf",
    #             bbox_inches='tight')

draw_heat_w()

