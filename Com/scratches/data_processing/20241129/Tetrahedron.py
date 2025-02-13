import os
import matplotlib.pyplot as plt
import numpy as np
from src.general.read_file import read_file
from src.general import set_figure
from src.ui.general_methods import GeneralMethods
from src.general.save_figure import save_subfig

'''
curve colors
'''
# 获取默认颜色循环
default_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

# 获取前 20 条曲线的颜色
num_colors = 20
colors = default_colors * (num_colors // len(default_colors) + 1)  # 复制颜色列表以确保足够多的颜色
colors = colors[:num_colors]  # 截取前 num_colors 条颜色

folder_path = r'C:\Users\a1033\Desktop\Contemporary\2024年11月\20241129DFS\20241129RenishawDFS\20241129\data\20241129\4'
extensions = ['.txt']

file_paths, files, file_names = GeneralMethods.list_files_in_directory(folder_path, extensions)
i = 0

sps = []
legend_labels = []
for file_path, file_name in zip(file_paths, file_names):
    if 'sub(sio2)-1_DFS_30s' in file_name:
        RF = read_file(file_path, strip='all', show_data_flag=False)
        sub = RF.data['intensity']
        wav = RF.data['wavelength']
    elif '30s' in file_name and 'sub' not in file_name:
        RF = read_file(file_path, strip='all', show_data_flag=False)
        sps.append(RF.data['intensity'])
        legend_labels.append(file_name)


def gaussian(x, A, mu, sigma):
    return A * np.exp(- (x - mu) ** 2 / (2 * sigma ** 2))


def double_gaussian(x, A1, mu1, sigma1, A2, mu2, sigma2):
    return A1 * np.exp(- (x - mu1) ** 2 / (2 * sigma1 ** 2)) + A2 * np.exp(- (x - mu2) ** 2 / (2 * sigma2 ** 2))


from scipy.optimize import curve_fit


fig = plt.figure(figsize=(8, 6), dpi=100)
ax = fig.add_subplot(111)
for idx, sp in enumerate(sps):
    sp = (sp - sub)/sub
    ax.plot(wav, sp/np.max(sp))  # Normalized
    # ax.plot(wav, sp)

title = f'Tetrahedron-Contrast DFS-Normalized'  # Normalized
set_figure.set_label_and_title(ax, title=title, ylabel='Intensity(Contrast, Normalized)',
                               label_fontsize=25, title_fontsize=25,
                               label_font_family='Times New Roman', title_font_family='Times New Roman',
                               label_fontweight='bold', title_fontweight='bold',
                               label_pad=8, title_pad=15)
set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
                    linewidth=3, tick_pad=5, direction='in',
                    ticks_xlabel=np.linspace(500, 1000, 11),
                    ticks_ylabel=np.linspace(0, 1, 11))  # Normalized
set_figure.set_legend(ax, legend_labels=legend_labels, font_size=20)

# title = f'Tetrahedron-Contrast DFS'
# set_figure.set_label_and_title(ax, title=title, ylabel='Intensity(Contrast)',
#                                label_fontsize=25, title_fontsize=25,
#                                label_font_family='Times New Roman', title_font_family='Times New Roman',
#                                label_fontweight='bold', title_fontweight='bold',
#                                label_pad=8, title_pad=15)
# set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
# set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
#                     linewidth=3, tick_pad=5, direction='in',
#                     ticks_xlabel=np.linspace(500, 1000, 11))
# set_figure.set_legend(ax, legend_labels=legend_labels, font_size=20)

# for idx, sp in enumerate(sps):
#     sp = (sp - sub)
#     fig = plt.figure(figsize=(8, 6), dpi=100)
#     ax = fig.add_subplot(111)
#     ax.plot(wav, sp)
#     print(f'name = {legend_labels[idx]}')
#     if 'tetrahedron-1' in legend_labels[idx] or 'tetrahedron-4' in legend_labels[idx]:
#         popt, pcov = curve_fit(gaussian, wav, sp, p0=[4800, 700, 50])
#         # 拟合参数
#         A_fit, mu_fit, sigma_fit = popt
#         print(f'拟合结果: A1 = {A_fit:.2f}, mu1 = {mu_fit:.2f}, sigma1 = {sigma_fit:.2f}')
#         y_fit = gaussian(wav, *popt)
#     elif 'tetrahedron-3' in legend_labels[idx] or 'tetrahedron-5' in legend_labels[idx]:
#         popt, pcov = curve_fit(double_gaussian, wav, sp, p0=[300, 625, 100, 50, 800, 200])
#         # 拟合参数
#         A1_fit, mu1_fit, sigma1_fit, A2_fit, mu2_fit, sigma2_fit = popt
#         print(f'拟合结果: A1 = {A1_fit:.2f}, mu1 = {mu1_fit:.2f}, sigma1 = {sigma1_fit:.2f}')
#         print(f'拟合结果: A2 = {A2_fit:.2f}, mu2 = {mu2_fit:.2f}, sigma2 = {sigma2_fit:.2f}')
#         y_fit = double_gaussian(wav, *popt)
#     else:
#         popt, pcov = curve_fit(double_gaussian, wav, sp, p0=[5000, 600, 100, 4200, 700, 200])
#         # 拟合参数
#         A1_fit, mu1_fit, sigma1_fit, A2_fit, mu2_fit, sigma2_fit = popt
#         print(f'拟合结果: A1 = {A1_fit:.2f}, mu1 = {mu1_fit:.2f}, sigma1 = {sigma1_fit:.2f}')
#         print(f'拟合结果: A2 = {A2_fit:.2f}, mu2 = {mu2_fit:.2f}, sigma2 = {sigma2_fit:.2f}')
#         y_fit = double_gaussian(wav, *popt)
#     ax.plot(wav, y_fit, 'r-', label='Fitted Gaussian')  # 拟合曲线
#     title = f'{legend_labels[idx]}-Normalized'
#
#     set_figure.set_label_and_title(ax, title=title, ylabel='Intensity(cts/s)',
#                                    label_fontsize=25, title_fontsize=25,
#                                    label_font_family='Times New Roman', title_font_family='Times New Roman',
#                                    label_fontweight='bold', title_fontweight='bold',
#                                    label_pad=8, title_pad=15)
#     set_figure.set_spines(ax, bottom_linewidth=3, left_linewidth=3, top_linewidth=3, right_linewidth=3)
#     set_figure.set_tick(ax, xbins=6, ybins=10, fontsize=15, fontweight='bold',
#                         linewidth=3, tick_pad=5, direction='in',
#                         ticks_xlabel=np.linspace(500, 1000, 11))

    # save_filename = os.path.join(folder_path, legend_labels[idx])
    # save_filename += '.png'
    # print(save_filename)
    # save_subfig(fig, save_filename)
plt.show()
