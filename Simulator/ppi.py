# ***** Imports ***** #

import matplotlib.pyplot as plt
import matplotlib.animation as anim

# *****   Data  ***** #

angles = [0.3,1.5,1.1, 2]
ranges = [20,15,7, 40]

class PPI:
    def __init__(self, range_max):
        super().__init__()
        self.range_max = range_max
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='polar',facecolor='#006d70')
        self.ax.set_ylim([0.0,range_max])
        self.detected_objects = [{"angle": angles[i], "range": ranges[i]} for i in range(0,len(angles))]
        self.animation = anim.FuncAnimation(self.fig, self.animate, interval=1, blit=False)
        plt.show()
        return

    def animate(self, t):
        self.ax.clear()
        self.ax.grid(color='w',alpha=0.5)
        delta = 0.0625
        radar_angle = (t*delta) % 361
        range_max = self.range_max
        
        plt_points_ang = [point["angle"] for point in self.detected_objects if point["angle"] < radar_angle]
        plt_points_rng = [point["range"] for point in self.detected_objects if point["angle"] < radar_angle]
        self.ax.plot(plt_points_ang,plt_points_rng, color='w',marker='o', linestyle='')
        
        self.ax.plot([radar_angle        ,radar_angle]        , [0,range_max]    ,color='w',linewidth=1.0, alpha=1)
        self.ax.plot([radar_angle - 1/100,radar_angle - 1/100], [0,range_max]    ,color='w',linewidth=2.0, alpha=0.6)
        self.ax.plot([radar_angle - 2/100,radar_angle - 2/100], [0,range_max]    ,color='w',linewidth=3.0, alpha=0.3)
        self.ax.plot([radar_angle - 4/100,radar_angle - 4/100], [0,range_max]    ,color='w',linewidth=5.0, alpha=0.2)
        self.ax.plot([radar_angle - 6/100,radar_angle - 6/100], [0,range_max]    ,color='w',linewidth=7.0, alpha=0.1)
        self.ax.plot([radar_angle - 8/100,radar_angle - 8/100], [0,range_max]    ,color='w',linewidth=9.0, alpha=0.05)
        self.ax.plot([radar_angle - 10/100,radar_angle- 10/100],[0,range_max]    ,color='w',linewidth=10.0, alpha=0.025)

        # self.detected_objects = [{"angle": angles[i], "range": ranges[i]} for i in range(0,len(angles)) if angles[i] > radar_angle+delta or ]
        

ppi = PPI(50)