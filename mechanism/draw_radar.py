import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
import pickle

def draw_radar_eps(error, datasetlist, epsilon_list):

    font={'family':'Times New Roman', 'weight':'bold'}
    plt.rc('font', **font)
    fig, axes_l = plt.subplots(nrows=1, ncols=5, sharey="row", figsize=(20, 4), subplot_kw=dict(polar=True))
    
    data_min = [[0 for i in range(len(epsilon_list))] for j in range(len(datasetlist))]
    for i in range(len(error)):
        for j in range(len(error[i])):
            data_min[i][j] = min(error[i][j])
    
    methods_name = ["SPAS", "Sample", "Uniform", "DSAT", "FAST", "BD", "AdaPub", "PeGaSuS"]
    colors = list(mcolors.XKCD_COLORS.values())
    
    dark_colors = [color for name, color in zip(mcolors.XKCD_COLORS.keys(), colors) if 'dark' in name][:len(methods_name)]
    
    for i, ax in enumerate(axes_l.flatten()):
        
        # ax.set_ylim(100, 1)
        ax.set_ylim(1, 100)
        
        if i>=5:
            break
        
        for method_index, method_name in enumerate(methods_name):
            datalist_shortname = ["Otp", "Dth", "Uem", "Syn1", "Syn2"]
            
            stats = np.array([10, 20, 25, 50, 21]) * method_index * 0.25
            
            stats = np.concatenate((stats, [stats[0]]))
            
            angles = np.linspace(0, 2 * np.pi, len(datalist_shortname), endpoint=False).tolist()
            angles += angles[:1]
        
            ax.plot(angles, stats, dark_colors[method_index], linewidth=0.5)
            ax.fill(angles, stats, dark_colors[method_index], alpha=0.1)
        
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(datasetlist, size=8)
      
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)

    legend_ax = fig.add_axes([0.25, 0.9, 0.5, 0.1])
    legend_ax.axis('off')

    legend_handles = [plt.Line2D([0], [0], color=color, linewidth=3, linestyle='-') for color in dark_colors]
    legend_ax.legend(legend_handles, methods_name, loc='center', ncol=len(methods_name)//2, fontsize=12)

    plt.show()
            
            
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

    datasets_list = ["F1d", "Dth", "Uem", "syn_uniform", "syn_mix"]
    epsilon_list = [0.1, 0.3, 0.5, 0.7, 0.9]
    window_size_list = [40, 80, 120, 160, 200]
    

    # draw eps
    with open("./output/error_w_sum_query.pickle", "rb") as f:
        error = pickle.load(f)
    draw_radar_eps(error, datasets_list, epsilon_list)