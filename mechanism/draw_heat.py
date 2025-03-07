import matplotlib.pyplot as plt
import matplotlib
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
import pickle

def draw_heat_eps(error, datasetlist, epsilon_list):
    # print(error[0])
    eval = "eps"

    font={'family':'Times New Roman', 'weight':'bold'}
    fig, axes_l = plt.subplots(nrows=2, ncols=4, sharey="row", figsize=(14, 9))

    data_min = [[0 for i in range(len(epsilon_list))] for j in range(len(datasetlist))]
    for i in range(len(error)):
        for j in range(len(error[i])):
            data_min[i][j] = min(error[i][j])

    for i, axr in enumerate(axes_l):
        for j, ax in enumerate(axr):
            # print(axes_l)
            if i>=2:
                break
            data = []
            for m in range(len(datasetlist)):
                for n in range(len(epsilon_list)):
                    data.append(error[m][n][4 * i + j] / data_min[m][n])
            dataf = np.array([t for t in data])
            dataf.resize(len(datasetlist), 5)


            ax.tick_params(left=False, right=False)
            if j == 0:
                ax.set_ylabel('Datasets', fontsize =15, fontdict=font)
                
                datalist_shortname = ["Otp", "Dth", "Uem", "Syn1", "Syn2", "Flu", "Tdv", "Syn3", "Syn4", "Ret"]
                #datalist_shortname = ["Otp", "Dth", "Uem", "Syn1"]
                ax.set_yticks([i for i in range(len(datasetlist))])
                ax.tick_params(left=True, right=False)
                ax.set_yticklabels(datalist_shortname, fontsize = 10, fontdict=font)
            if i == 1:
                ax.set_xlabel(r'$\epsilon$', fontsize =15, fontdict=font)



            ax.set_xticks([0,1,2,3,4])
            for edge, spine in ax.spines.items():
                spine.set_visible(False)

            ax.set_xticklabels([0.1, 0.3, 0.5, 0.7, 0.9], fontsize = 10)
            ax.grid(which="minor", color ="w", linestyle="-", linewidth=3)
            
            norm1 = mcolors.LogNorm(vmin=1E0, vmax=1E2)
            im = ax.imshow(dataf, cmap='PuBu', norm=norm1, aspect=0.5) # YlGn

            for m in range(len(epsilon_list)):
                for n in range(len(datasetlist)):
                    text = ax.text(m, n, round(dataf[n, m], 1) if dataf[n, m] <= 100 else ">100",
                                    horizontalalignment="center", 
                                    verticalalignment="center", 
                                    color="black" if dataf[n, m] <= 10 else "w", fontsize=10)
            methods_name = ["SPAS", "Sample", "Uniform", "DSAT", "FAST", "BD", "AdaPub", "PeGaSuS"]
            ax.set_title(methods_name[4 * i + j], fontsize=14, fontdict=font)

    cax1 = fig.add_axes([0.82, 0.53, 0.01, 0.9 * ax.get_position().height])
    clb1 = fig.colorbar(im, ax = axes_l,location="right", fraction=0.05, pad=0.1, cax=cax1)
    for l in clb1.ax.yaxis.get_ticklabels():
        l.set_family('Times New Roman')
        l.set_fontweight('bold')
    clb1.ax.set_title(r"$\delta_{MRE}$", fontsize=10, fontdict=font)
    # clb.ax.set_aspect(8)

    cax2 = fig.add_axes([0.82, 0.22, 0.01, 0.9 * ax.get_position().height])
    # formatter = mpl.ticker.StrMethodFormatter('{x:.0f}')
    clb2 = fig.colorbar(im, ax = axes_l, location="right", fraction=0.05, pad=0.1, cax=cax2)
    for l in clb2.ax.yaxis.get_ticklabels():
        l.set_family('Times New Roman')
        l.set_fontweight('bold')
    clb2.ax.set_title(r"$\delta_{MRE}$", fontsize=10, fontdict=font)
    clb2.ax.tick_params(labelsize=10)
    #clb2.locator = ticker.MaxNLocator(nbins=5)  # colorbar上的刻度值个数
    clb2.update_ticks()

    fig.tight_layout()
    fig.subplots_adjust(left=0.076, bottom=0.2, right=0.813, top=0.77, wspace=0.15, hspace=0.26)

    plt.show()
    fig.savefig("./fig/sup_fig/heat_eps.pdf")
  
def draw_heat_w(error, datasetlist, window_size_list):
    # print(error[0])
    eval = "eps"

    font={'family':'Times New Roman', 'weight':'bold'}
    fig, axes_l = plt.subplots(nrows=2, ncols=4, sharey="row", figsize=(14, 9))

    data_min = [[0 for i in range(len(window_size_list))] for j in range(len(datasetlist))]
    for i in range(len(error)):
        for j in range(len(error[i])):
            data_min[i][j] = min(error[i][j])

    for i, axr in enumerate(axes_l):
        for j, ax in enumerate(axr):
            # print(axes_l)
            if i>=2:
                break
            data = []
            for m in range(len(datasetlist)):
                for n in range(len(window_size_list)):
                    data.append(error[m][n][4 * i + j] / data_min[m][n])
            dataf = np.array([t for t in data])
            dataf.resize(len(datasetlist), 5)


            ax.tick_params(left=False, right=False)
            if j == 0:
                ax.set_ylabel('Datasets', fontsize =15, fontdict=font)
                
                datalist_shortname = ["Otp", "Dth", "Uem", "Syn1", "Syn2", "Flu", "Tdv", "Syn3", "Syn4", "Ret"]
                #datalist_shortname = ["Otp", "Dth", "Uem", "Syn1", "Syn2"]
                ax.set_yticks([i for i in range(len(datasetlist))])
                ax.tick_params(left=True, right=False)
                ax.set_yticklabels(datalist_shortname, fontsize = 10, fontdict=font)
            if i == 1:
                ax.set_xlabel('w', fontsize =15, fontdict=font)



            ax.set_xticks([0,1,2,3,4])
            for edge, spine in ax.spines.items():
                spine.set_visible(False)

            ax.set_xticklabels([80, 120, 160, 200, 240], fontsize = 10)
            ax.grid(which="minor", color ="w", linestyle="-", linewidth=3)
            
            norm1 = mcolors.LogNorm(vmin=1E0, vmax=1E2)
            im = ax.imshow(dataf, cmap='PuBu', norm=norm1, aspect=0.5) # YlGn

            for m in range(len(window_size_list)):
                for n in range(len(datasetlist)):
                    text = ax.text(m, n, round(dataf[n, m], 1) if dataf[n, m] <= 100 else ">100",
                                    horizontalalignment="center", 
                                    verticalalignment="center", 
                                    color="black" if dataf[n, m] <= 10 else "w", fontsize=10)
            methods_name = ["SPAS", "Sample", "Uniform", "DSAT", "FAST", "BD", "AdaPub", "PeGaSuS"]
            ax.set_title(methods_name[4 * i + j], fontsize=14, fontdict=font)

    cax1 = fig.add_axes([0.82, 0.53, 0.01, 0.9 * ax.get_position().height])
    clb1 = fig.colorbar(im, ax = axes_l,location="right", fraction=0.05, pad=0.1, cax=cax1)
    for l in clb1.ax.yaxis.get_ticklabels():
        l.set_family('Times New Roman')
        l.set_fontweight('bold')
    clb1.ax.set_title(r"$\delta_{MRE}$", fontsize=10, fontdict=font)
    # clb.ax.set_aspect(8)

    cax2 = fig.add_axes([0.82, 0.22, 0.01, 0.9 * ax.get_position().height])

    clb2 = fig.colorbar(im, ax = axes_l, location="right", fraction=0.05, pad=0.1, cax=cax2)
    for l in clb2.ax.yaxis.get_ticklabels():
        l.set_family('Times New Roman')
        l.set_fontweight('bold')
    clb2.ax.set_title(r"$\delta_{MRE}$", fontsize=10, fontdict=font)
    clb2.ax.tick_params(labelsize=10)
    #clb2.locator = ticker.MaxNLocator(nbins=5)  # colorbar上的刻度值个数
    clb2.update_ticks()

    fig.tight_layout()
    fig.subplots_adjust(left=0.076, bottom=0.2, right=0.813, top=0.77, wspace=0.15, hspace=0.26)

    plt.show()
    fig.savefig("./fig/sup_fig/heat_w.pdf")


if __name__ == "__main__":
    methods = ["spas",
                "sample",
                "uniform",
                "dsat",
                "fast",
                "bd",
                "adapub",
                "pegasus",
                ]
    eval = "eps"

    # draw on real datasets
    #datasetlist = ["Uem", 'Out', 'syn_mix']
    #datasetlist = ['nation']
    datasets_list = ["F1d", "Dth", "Uem", "syn_mix", "Arbit1", "Fmd", "Tdv", "Tpt", "Arbitm", "Ret"]
    #datasets_list = ["F1d", "Dth", "Uem", "syn_uniform"]
    epsilon_list = [0.1, 0.3, 0.5, 0.7, 0.9]
    window_size_list = [80, 120, 160, 200, 240]
    

    # draw eps
    with open("./output/24.10.11/errorw1.pickle", "rb") as f:
        error = pickle.load(f)

    # # reorder error matrix, remove original syn1, change syn2 as syn1, new results are syn2 and syn4
    # for i in range(len(error)):
    #     for j in range(len(error[i])):
    #         data_min[i][j] = min(error[i][j])
    

    #draw_heat_eps(error, datasets_list, epsilon_list)
    draw_heat_w(error, datasets_list, window_size_list)