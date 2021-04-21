import matplotlib.pyplot as plt
import seaborn as sns
from skimage.color import rgb2gray
import numpy as np
from merging_utilities.img_utils import avg_image, split_layers_to_3

def plot_image(img, title):
    # Plot image
    fig, ax1 = plt.subplots(ncols=1, figsize=(18, 6), sharex=True,
                                   sharey=True)
    ax1.imshow(img, cmap='gray')
    ax1.set_title(title)
    ax1.axis('off')
    
def plot_images(rgb, rgb_name, ir, ir_name):

    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(14, 6), sharex=True,
                                   sharey=True)
    ax1.imshow(rgb, cmap='gray')
    ax1.set_title(rgb_name)
    ax1.axis('off')
    
    # plot altered
    ax2.imshow(ir, cmap='gray')
    ax2.set_title(ir_name)
    ax2.axis('off')
    
    
def plot_histogram(x, title):
    fig, ax = plt.subplots()

    sigma_ = np.std(x)
    mu_ = np.mean(x)

    x_ = np.ravel(x)
    min = x_.min()
    max = x_.max()
    range = max - min

    count, bins, ignored = ax.hist(x_, 300, density=True)

    bins = int(range / 3.5)

    ax.set_xlabel('{} bins with fit line, plotted against precise values'.format(bins))
    ax.set_ylabel('Probability Density')
    ax.set_title(r'{0}: $\mu=${1:.3f}, $\sigma=${2:.3f}'.format(title, mu_, sigma_))

    sns.set_style('darkgrid')
    sns.distplot(x_, color="b", bins=75)

#     out_name = 'output/histograms/' + title + '.jpg'
#     out_name = process_title(out_name)
#     plt.savefig(out_name, dpi=600)
    plt.show()

    
def plot_histograms(im, title, images=False):
    gray = rgb2gray(im)

    gray = 255 * gray # Now scale by 255
    gray = gray.astype(np.uint8)
    
    avgd_image = avg_image(im)
    
    R,G,B = split_layers_to_3(im)
    
    
    if images==True:
        plot_image(gray, 'grayscale/luminance (weighted channels)')
    plot_histogram(gray, '{}: Luminosity Histogram'.format(title[0:-1]))
    
    if images==True:
        plot_image(avgd_image, '3 channels averaged to one channel')
    plot_histogram(avgd_image, '{}: Averaged Histogram'.format(title[0:-1]))
        
    if images==True:
        plot_image(R, 'Red channel')
    plot_histogram(R, '{}: Reds Histogram'.format(title[0:-1]))

    if images==True:
        plot_image(B, 'Blues channel')
    plot_histogram(B, '{}: Blues Histogram'.format(title[0:-1]))

    if images==True:
        plot_image(G, 'Greens channel')
    plot_histogram(G, '{}: Greens Histogram'.format(title[0:-1]))
    
def compare_histograms(img1, img1_title, img2, img2_title):
    plot_images(img1, img1_title, img2, img2_title)