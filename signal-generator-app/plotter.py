import matplotlib.pyplot as plt

def plot_signal(t, y, title="Signal"):
    plt.plot(t, y)
    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.show()

#does not clear the plot
#def clear_plot():