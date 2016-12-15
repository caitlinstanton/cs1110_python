# plot3d.py
# Walker M. White (wmw2), Steve Marschner (srm2), Lillian Lee (ljl2)
# November 1, 2013
"""Visualization App to verify that k-means works

The visualize can view any clustering on a set of 3D points.
Visualization is limited to 3d points and k-values < 15."""
import matplotlib
import numpy
import math
import traceback
matplotlib.use('TkAgg')

# Modules to embed matplotlib in a custom Tkinter window
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

# File support to load data files
import os
import sys
import Tkinter as Tk
import tkFileDialog
import tkMessageBox
import tkFont

# The k-means implementation
import a6

# Maximum allowable k-means
MAX_K_VAL = 14


def parse_data(data):
    """Return: 3-element list equivalent to file line

    Precondition: data is a line from csv file whole first three elements are numbers."""
    if data[0] == '#':
        return None
    
    return map(float,data[:-1].split(',')[-3:])


class Visualizer(object):
    """Instance is a visualization app.

    INSTANCE ATTRIBUTES:
        _root:   TCL/TK graphics backend [TK object]
        _canvas: MatPlotLib canvas [FigureCanvas object]
        _axes:   MatPlotLib axes   [Axes object]
        _ds:     Data set [Dataset object]
        _kmean:   Clustering of dataset [Clustering object]
        _count:  Number of steps executed [int >= 0]
        _finish: Whether the computation is done [bool]

    There are several other attributes for GUI widgets
    (buttons and labels).  We do not list all of them here."""

    def __init__(self, filename=None):
        """Initializer: Make a visualization app"""
        self._root = Tk.Tk()
        self._root.wm_title("Clustering Assignment Visualizer")
        self._ds = None
        self._kmean = None
        
        # Start the application
        self._config_canvas()
        self._config_control()
        self._canvas.show()
        
        # Load data if provided
        if filename is not None:
            self._load_file(filename)
        
        Tk.mainloop()
    
    def _config_canvas(self):
        """Load the MatPlotLib drawing code"""
        # Create the drawing canvas
        figure = Figure(figsize=(6,6), dpi=100)
        self._canvas = FigureCanvasTkAgg(figure, master=self._root)
        self._canvas._tkcanvas.pack(side=Tk.LEFT, expand=True, fill=Tk.BOTH)
        
        # Initialize the scatter plot
        self._axes = figure.gca(projection='3d')
        self._axes.set_xlim((0.0, 1.0))
        self._axes.set_ylim((0.0, 1.0))
        self._axes.set_zlim((0.0, 1.0))
        self._axes.set_xlabel('X')
        self._axes.set_ylabel('Y')
        self._axes.set_zlabel('Z')
        self._axes.set_xticks(numpy.arange(0.0,1.0,0.1))
        self._axes.set_yticks(numpy.arange(0.0,1.0,0.1))
        self._axes.set_zticks(numpy.arange(0.0,1.0,0.1))
        self._axes.tick_params(labelsize=9)
    
    def _config_control(self):
        """Create the control panel on the right hand side
        
        This method is WAY too long, but GUI layout code is typically
        like this. Plus, Tkinter makes this even worse than it should be."""
        panel = Tk.Frame(master=self._root)
        panel.columnconfigure(0,pad=3)
        panel.columnconfigure(1,pad=3)
        panel.rowconfigure(0,pad=3)
        panel.rowconfigure(1,pad=0)
        panel.rowconfigure(2,pad=23)
        panel.rowconfigure(3,pad=3)
        panel.rowconfigure(4,pad=3)
        panel.rowconfigure(5,pad=3)
        panel.rowconfigure(6,pad=13)
        
        title = Tk.Label(master=panel,text='K Means Control',height=3)
        wfont = tkFont.Font(font=title['font'])
        wfont.config(weight='bold',size=20)
        title.grid(row=0,columnspan=2, sticky='we')
        title.config(font=wfont)
        
        divider = Tk.Frame(master=panel,height=2, bd=1, relief=Tk.SUNKEN)
        divider.grid(row=1,columnspan=2, sticky='we')
        
        # Label and button for managing files.
        label = Tk.Label(master=panel,text='Data Set: ',height=2)
        wfont = tkFont.Font(font=label['font'])
        wfont.config(weight='bold')
        label.config(font=wfont)
        label.grid(row=2,column=0, sticky='e')
        
        self._filebutton = Tk.Button(master=panel, text='<select file>', width=10,command=self._load)
        self._filebutton.grid(row=2,column=1, sticky='w',padx=(0,10))
        
        # Label and option menu to select k-value
        label = Tk.Label(master=panel,text='K Value: ',height=2,font=wfont)
        label.grid(row=3,column=0,sticky='e')
        
        self._kval = Tk.IntVar(master=self._root)
        self._kval.set(3)
        options = Tk.OptionMenu(panel,self._kval,*range(1,MAX_K_VAL+1),command=self._reset)
        options.grid(row=3,column=1,sticky='w')
        
        # Label and step indicator
        label = Tk.Label(master=panel,text='At Step: ',height=2,font=wfont)
        label.grid(row=4,column=0,sticky='e')
        
        self._count = 0
        self._countlabel = Tk.Label(master=panel,text='0')
        self._countlabel.grid(row=4,column=1,sticky='w')
        
        # Label and convergence indicator
        label = Tk.Label(master=panel,text='Finished: ',height=2,font=wfont)
        label.grid(row=5,column=0,sticky='e')
        
        self._finished = False
        self._finishlabel = Tk.Label(master=panel,text='False')
        self._finishlabel.grid(row=5,column=1,sticky='w')
        
        # Control buttons
        button = Tk.Button(master=panel, text='Reset', width=8, command=self._reset)
        button.grid(row=6,column=0,padx=(10,0))
        button = Tk.Button(master=panel, text='Step', width=8, command=self._step)
        button.grid(row=6,column=1)
        
        panel.pack(side=Tk.RIGHT, fill=Tk.Y)
    
    def _plot_clusters(self):
        """Plot the clusters in a completed assignment"""
        COLORS = ('r','g','b','k','c','m','y')
        for k in range(self._kval.get()):
            c = COLORS[k % len(COLORS)]
            m = 'x' if k % 2 == 0 else '+'
            cluster = self._kmean.getClusters()[k]
            rows = numpy.array(cluster.getContents())
            cent = cluster.getCentroid()
            if (len(rows) > 0):
                self._axes.scatter(rows[:,0], rows[:,1], rows[:,2], c=c, marker=m)
            self._axes.scatter(cent[0],cent[1],cent[2],c=c,s=30,marker='o')
    
    def _plot_one_cluster(self):
        """Plot one cluster in an assignment that has finished Cluster but not Clustering."""
        # Try to show everything in one cluster.
        cluster = a6.Cluster(self._ds, self._ds.getPoint(0))
        for i in range(self._ds.getSize()):
            cluster.addIndex(i)
        cluster.updateCentroid()
        rows = numpy.array(self._ds.getContents())
        cent = cluster.getCentroid()
        if (len(rows) > 0):
            self._axes.scatter(rows[:,0], rows[:,1], rows[:,2], c='b', marker='+')
        self._axes.scatter(cent[0],cent[1],cent[2],c='b',s=30,marker='o')
    
    def _plot_points(self):
        """Plot the clusters in an assignment that has finished Dataset but not much else."""
        rows = numpy.array(self._ds.getContents())
        self._axes.scatter(rows[:,0], rows[:,1], rows[:,2], c='k', marker='+')
    
    def _plot(self):
        """General plot function
        
        This function replots the data any time that it changes."""
        assert not self._ds is None, 'Invariant Violation: Attempted to plot when data set is None'
        
        self._axes.clear()
        if self._kmean is not None:
            try:
                self._plot_clusters()
            except BaseException as e:
                print 'FAILED KMEANS VISUALIZATION: '
                traceback.print_exc()
                print ''
                print 'Attempting One Cluster Only'
                try:
                    self._plot_one_cluster()
                except BaseException as e:
                    print 'FAILED CLUSTER VISUALIZATION '
                    traceback.print_exc()
                    print ''
                    print 'Attempting Data Set Only'
                    self._plot_points()
        else:
            self._plot_points()
        
        # Reset axes information
        xb = self._axes.get_xbound()
        xb = (numpy.floor(xb[0]*10)/10.0,numpy.ceil(xb[1]*10)/10.0)
        self._axes.set_xlim(xb)
        self._axes.set_xticks(numpy.arange(xb[0],xb[1],0.1))
        
        yb = self._axes.get_ybound()
        yb = (numpy.floor(yb[0]*10)/10.0,numpy.ceil(yb[1]*10)/10.0)
        self._axes.set_ylim(yb)
        self._axes.set_yticks(numpy.arange(yb[0],yb[1],0.1))
        
        zb = self._axes.get_zbound()
        zb = (numpy.floor(zb[0]*10)/10.0,numpy.ceil(zb[1]*10)/10.0)
        self._axes.set_zlim(zb)
        self._axes.set_zticks(numpy.arange(zb[0],zb[1],0.1))
        self._axes.set_xlabel('X')
        self._axes.set_ylabel('Y')
        self._axes.set_zlabel('Z')
        
        self._canvas.show()
        
    def _load(self):
        """Let the user select a file, and load it."""
        filename = tkFileDialog.askopenfilename(initialdir='.',
                                                title='Select a Data File',
                                                filetypes=[('CSV Data Files', '.csv')])
        if filename is None:
            return
        self._load_file(filename)

    def _load_file(self, filename):
        """Load a data set file into a Dataset."""
        try:
            f = open(filename)
            contents = []
            first = f.readline()
            assert first[1:].strip()[:5] == 'kdata'
            
            for x in f:
                if x[0] != '#': # Ignore comments
                    point = parse_data(x)
                    contents.append(point)
        
            self._ds = a6.Dataset(3,contents)
            if not self._ds.getContents():
                raise RuntimeError()
            shortname = os.path.split(filename)[1]
            if (len(shortname) > 10):
                shortname = shortname[0:10]+'...'
            self._filebutton.configure(text=shortname)
            self._kmean = None
            self._plot()
        except RuntimeError:
            tkMessageBox.showwarning('Load','ERROR: You must complete Dataset first.')
        except AssertionError:
            tkMessageBox.showwarning('Load','ERROR: CSV file must be a kdata file.')
        except:
            traceback.print_exc()
            tkMessageBox.showwarning('Load','ERROR: kdata file is corrupted.')
    
    def _reset(self,k=None):
        """Reset the k-means calculation with the given k value.  If k is
        None, use the value of self._kval.
        
        Precondition: k > 0 is an int, and a dataset with at least k
        points is loaded.  If k is None, the current value of self._kval
        is used."""
        if k is None:
            k = self._kval.get()
        if self._ds is None:
            tkMessageBox.showwarning('Reset','ERROR: No data set loaded.')
        
        self._count = 0
        self._countlabel.configure(text='0')
        self._finished = False
        self._finishlabel.configure(text='False')
        
        # Student may not have implemented this yet.
        self._kmean = a6.ClusterGroup(self._ds, k)
        self._kmean._partition()
        self._plot()
    
    def _step(self):
        """Perform one step in k-means clustering"""
        if self._ds is None:
            tkMessageBox.showwarning('Step','ERROR: No data set loaded.')
        if self._kmean is None:
            self._reset()
        if self._finished:
            return
        
        self._count = self._count+1
        self._countlabel.configure(text=str(self._count))
        self._finished = self._kmean.step()
        self._finishlabel.configure(text=str(self._finished))
        
        self._plot()


# Script code
if __name__ == '__main__':
    if len(sys.argv) == 2:
        Visualizer(sys.argv[1])
    else:
        Visualizer()
