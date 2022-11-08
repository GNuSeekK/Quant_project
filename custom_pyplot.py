import matplotlib.pyplot as plt
from matplotlib import cm, gridspec
import numpy as np

class custom_pyplot_colorbar:
    def __init__(self, min_color: int, max_color: int, figsize: tuple=(5,5), data_num: int=1, cmap = 'rainbow'):
        """_summary_

        Args:
            min_color (int): 첫번째 컬러의 값
            max_color (int): 마지막 컬러의 값
            figsize (tuple, optional): pyplot 크기. Defaults to (5,5).
            data_num (int, optional): 데이터의 갯수. Defaults to 1.
            cmap (str, optional): _description_. Defaults to 'rainbow'.
        """        
        
        self.data_num = data_num
        self.min_color = min_color
        self.max_color = max_color
        self.fig = plt.figure(figsize = figsize)
        self.gs = gridspec.GridSpec(nrows=1, # row 몇 개 
                            ncols=self.data_num + 1, # col 몇 개 
                            height_ratios = [20], 
                            width_ratios = [20] * self.data_num + [0.5]
                            )

        color_x = [0] * 256
        color_y = np.linspace(self.min_color, self.max_color, 256)

        ax1 = plt.subplot(self.gs[-1])
        ax1.scatter(color_x, color_y, c=color_y, cmap=cmap, s=520)
        plt.ylim(self.min_color, self.max_color)
        plt.xticks([])
    
    def axes_call(self, index: int):
        """_summary_

        Args:
            index (int): N번째 grid 불러오기

        Returns:
            _type_: plt.subplot
        """        
        if index < self.data_num:
            return plt.subplot(self.gs[index])
        else:
            raise ValueError('index over data num')

    def color_find(self, x: int):
        """_summary_

        Args:
            x (int): 값에 알맞은 color 찾기

        Returns:
            _type_: cmap
        """        
        x = int(((x - self.min_color) / (self.max_color - self.min_color)) * 256)
        cmap = 'rainbow'
        rgb = cm.get_cmap(cmap)(x)

        return rgb
    
# 실험

# custom_graph = custom_pyplot_colorbar(-3,3, figsize = (10,5), data_num = 2)
# ax = custom_graph.axes_call(0)
# ax.scatter(1,1, color = custom_graph.color_find(0))
# ax1 = custom_graph.axes_call(1)
# ax1.plot( [0,3], [0,3], c = custom_graph.color_find(3))
# plt.show()