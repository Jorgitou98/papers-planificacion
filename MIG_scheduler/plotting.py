import matplotlib.pyplot as plt
import matplotlib.patches as patches
from algorithm import give_makespan


def plot_speedup_inputs(device, times):
    #plt.rcParams["figure.figsize"] = (6.5, 2.5)
    if device != "A100":
        return
    slices_A100=[1,2,3,4,7]
    for time_task in times:
        print(time_task)
        speedups = [time_task[0][2] / time for index, slices, time in time_task[1:]]
        print(speedups)
        plt.plot(slices_A100[1:], speedups, marker='o')
        #input("Continuar")

    plt.plot(slices_A100[1:], slices_A100[1:], linestyle='--', label = "Linear scaling", color="black")
    plt.xlabel("Number of slices")
    plt.ylabel("Speedup over 1 slice", labelpad=5)
    plt.grid(axis='y', linestyle='--')

    plt.tight_layout(pad=0)
    plt.legend()
    plt.savefig("C:/Users/jorvi/Downloads/syntehtic_input.pdf")
    plt.show()

def draw_rects(n_slices, scheduling_no_dynamic, scheduling_1s, scheduling_fifo_fixed, scheduling_7s, scheduling_algorithm, lb_makespane_opt, names=None):
    colors = plt.cm.tab20.colors
    fig, axs = plt.subplots(1, 5, sharex=True, sharey=True)
    axs[0].set_title("Speed-Indep", size=20)
    axs[1].set_title("Fix-Part(1,...,1)", size=20)
    axs[2].set_title("Fix-Part-Best", size=20)
    axs[3].set_title("Fix-Part(7)", size=20)
    axs[4].set_title("Our algorithm", size=20)
    fig.add_subplot(111, frameon=False)
    plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
            
    
        
    makespan_scheduling_no_dynamic = give_makespan(scheduling_no_dynamic)
    scheds = [scheduling_no_dynamic, scheduling_1s, scheduling_fifo_fixed, scheduling_7s, scheduling_algorithm]
    for scheduling, ax in zip(scheds, axs):
        ax.set_xlim(-0.2, n_slices+0.2)
        ax.set_ylim(0, makespan_scheduling_no_dynamic+1)
        ax.set_yticks([0,5,10,15,20,25,30])
        line = ax.axhline(y=lb_makespane_opt, color='red', label = "baseline", linewidth=2)
        ax.tick_params(labelsize=20)
        rects = []
        for task in scheduling:
            label = names[task.index] if names else None
            rect = patches.Rectangle((task.first_slice, task.start_time), task.slices, task.time, alpha = 0.55,\
                                        linewidth = 1, facecolor = colors[task.index % len(colors)], label = label, edgecolor = 'black')
            ax.add_patch(rect)
            rects.append(rect)
    axs[2].set_xlabel("Slices", fontsize=20)
    axs[0].set_ylabel("Time", labelpad=5, fontsize=20)
    plt.subplots_adjust(wspace=0, hspace=0)
    plt.setp(axs, xticks=range(n_slices+1), xticklabels=[f"$S_{n}$" for n in range(n_slices)]+ [""])
    plt.tight_layout(pad=0)
    axs[4].legend(fontsize=20, handles=[line])
    if names != None:
        rects_sorted = sorted(rects, key=lambda x: x.get_label())
        lgd = plt.legend(fontsize=13, ncols = 8, handles=rects_sorted, bbox_to_anchor=(4.2, -0.2))
    plt.show()