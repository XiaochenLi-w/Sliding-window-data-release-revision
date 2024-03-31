import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import pickle

def draw_radar_eps(error, datasetlist, epsilon_list):

    font={'family':'Times New Roman', 'weight':'bold'}
    
    plt.rc('font', **font)
    
    fig, axes_list = plt.subplots(nrows=1, ncols=2, sharey="row", figsize=(9, 5), subplot_kw=dict(polar=True))
    # fig = plt.figure(figsize=(12, 8))
    # gs = gridspec.GridSpec(2, 6)
    
    # axes_list = []
    # for i in range(3):
    #     axes_list.append(fig.add_subplot(gs[0, i * 2:i * 2 + 2], polar=True))

    # axes_list.append(fig.add_subplot(gs[1, 1:3], polar=True))
    # axes_list.append(fig.add_subplot(gs[1, 3:5], polar=True))
    
    error_min = [[0 for i in range(len(epsilon_list))] for j in range(len(datasetlist))]
    for i in range(len(error)):
        for j in range(len(error[i])):
            error_min[i][j] = min(error[i][j])
    
    methods_name = ["SPAS", "Sample", "Uniform", "DSAT", "FAST", "BD", "AdaPub", "PeGaSuS"]
    datalist_shortname = ["Otp", "Dth", "Uem", "Syn1", "Syn2"]
    # colors = ['#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd']
    # colors = ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0', '#f0027f', '#bf5b17', '#666666']
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf']
    
    for i, ax in enumerate(axes_list):
        
        ax.set_ylim(10.5, 0.5)
        # ax.set_ylim(1, 100)
        
        if i>=2:
            break
        
        for method_index, method_name in enumerate(methods_name):
            
            # obtain and normalize data
            stats = []
            for j in range(len(datasetlist)):
                stats.append(min(10, error[j][2*i+2][method_index] / error_min[j][2*i+2]))
            
            stats = np.concatenate((stats, [stats[0]]))
            
            angles = np.linspace(0, 2 * np.pi, len(datalist_shortname), endpoint=False).tolist()
            angles += angles[:1]

            if method_index == 0:
                ax.plot(angles, stats, colors[method_index], linewidth=1.5, marker = 'o', ms=2)
            else:
                ax.plot(angles, stats, colors[method_index], linewidth=0.5, marker = 'o', ms=1)
                
            ax.fill(angles, stats, colors[method_index], alpha=0.05)
            
            desired_radii = [1, 3, 5, 7, 9]
            labels = [str(r) for r in desired_radii]
            ax.set_rgrids(desired_radii, labels=labels, color="grey")
        
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(datalist_shortname, size=10)
        
        if i == 0:
            ax.set_title('(a) ' + r'$\epsilon$=' + str(epsilon_list[2*i+2]), fontsize=15, fontdict=font)
        else:
            ax.set_title('(b) ' + r'$\epsilon$=' + str(epsilon_list[2*i+2]), fontsize=15, fontdict=font)
      
    plt.tight_layout()
    plt.subplots_adjust(top=0.85, left=0.03, right=0.95, wspace=0.29, hspace=0.15)

    legend_ax = fig.add_axes([0.3, 0.9, 0.4, 0.1])
    # legend_ax = fig.add_axes([0.3, 0.45, 0.4, 0.1])
    legend_ax.axis('off')

    legend_handles = [plt.Line2D([0], [0], color=color, linewidth=1, linestyle='-') for color in colors]
    legend_ax.legend(legend_handles, methods_name, loc='center', ncol=len(methods_name)//2, fontsize=8)

    fig.savefig("./fig/radar_count_query_eps.pdf")
    plt.show()
    
    
def draw_radar_w(error, datasetlist, window_size_list):

    font={'family':'Times New Roman', 'weight':'bold'}
    
    plt.rc('font', **font)
    
    fig, axes_list = plt.subplots(nrows=1, ncols=2, sharey="row", figsize=(9, 5), subplot_kw=dict(polar=True))
    # fig = plt.figure(figsize=(12, 8))
    # gs = gridspec.GridSpec(2, 6)
    
    # axes_list = []
    # for i in range(3):
    #     axes_list.append(fig.add_subplot(gs[0, i * 2:i * 2 + 2], polar=True))

    # axes_list.append(fig.add_subplot(gs[1, 1:3], polar=True))
    # axes_list.append(fig.add_subplot(gs[1, 3:5], polar=True))
    
    error_min = [[0 for i in range(len(window_size_list))] for j in range(len(datasetlist))]
    for i in range(len(error)):
        for j in range(len(error[i])):
            error_min[i][j] = min(error[i][j])
    
    methods_name = ["SPAS", "Sample", "Uniform", "DSAT", "FAST", "BD", "AdaPub", "PeGaSuS"]
    datalist_shortname = ["Otp", "Dth", "Uem", "Syn1", "Syn2"]
    # colors = ['#d53e4f', '#f46d43', '#fdae61', '#fee08b', '#e6f598', '#abdda4', '#66c2a5', '#3288bd']
    # colors = ['#7fc97f', '#beaed4', '#fdc086', '#ffff99', '#386cb0', '#f0027f', '#bf5b17', '#666666']
    colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf']
    
    for i, ax in enumerate(axes_list):
        
        ax.set_ylim(10.5, 0.5)
        # ax.set_ylim(1, 100)
        
        if i>=2:
            break
        
        for method_index, method_name in enumerate(methods_name):
            
            # obtain and normalize data
            stats = []
            for j in range(len(datasetlist)):
                stats.append(min(10, error[j][2*i+1][method_index] / error_min[j][2*i+1]))
            
            stats = np.concatenate((stats, [stats[0]]))
            
            angles = np.linspace(0, 2 * np.pi, len(datalist_shortname), endpoint=False).tolist()
            angles += angles[:1]
        
            if method_index == 0:
                ax.plot(angles, stats, colors[method_index], linewidth=1.5, marker = 'o', ms=2)
            else:
                ax.plot(angles, stats, colors[method_index], linewidth=0.5, marker = 'o', ms=1)
                
            ax.fill(angles, stats, colors[method_index], alpha=0.05)
            
            desired_radii = [1, 3, 5, 7, 9]
            labels = [str(r) for r in desired_radii]
            ax.set_rgrids(desired_radii, labels=labels, color="grey")
        
        ax.set_yticklabels([])
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(datalist_shortname, size=10)
        if i == 0:
            ax.set_title('(a) w=' + str(window_size_list[2*i+1]), fontsize=15, fontdict=font)
        else:
            ax.set_title('(b) w=' + str(window_size_list[2*i+1]), fontsize=15, fontdict=font)
      
    plt.tight_layout()
    plt.subplots_adjust(top=0.85, left=0.03, right=0.95, wspace=0.29, hspace=0.15)
    
    legend_ax = fig.add_axes([0.3, 0.9, 0.4, 0.1])
    # legend_ax = fig.add_axes([0.3, 0.45, 0.4, 0.1])
    legend_ax.axis('off')

    legend_handles = [plt.Line2D([0], [0], color=color, linewidth=1, linestyle='-') for color in colors]
    legend_ax.legend(legend_handles, methods_name, loc='center', ncol=len(methods_name)//2, fontsize=8)

    fig.savefig("./fig/radar_count_query_w.pdf")
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
    

    ########## draw eps ########
    with open("./output/error_eps_count_query.pickle", "rb") as f:
        error = pickle.load(f)
        
    draw_radar_eps(error, datasets_list, epsilon_list)    
        
    ########## draw w #########
    # with open("./output/error_w_count_query.pickle", "rb") as f:
    #     error = pickle.load(f)
    
    # draw_radar_w(error, datasets_list, window_size_list) 