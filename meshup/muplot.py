import Tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class App:
    def __init__(self, master, range_, data):
        # Create a container
        frame = Tkinter.Frame(master)

        fig = Figure(figsize=(4, 1.8))
        ax = fig.add_subplot(111)
        self.line, = ax.plot(range_, data)

        self.canvas = FigureCanvasTkAgg(fig,master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side='top', fill='both', expand=1)
        frame.pack()
#        print data
#        self.line.set_ydata(data)
        self.canvas.draw()

def showPlot(frame, range_, data):
	app = App(frame, range_, data)
	return app
