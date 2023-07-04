#read a niftifile and plot heatmap of center slice
"""
input: niftifile
output: heatmap of center slice
"""
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import os

def crossing_hm(niftifile):
    img = nib.load(niftifile)
    data = img.get_fdata()
    #data will be probability values; plot heatmap of center slice
    plt.imshow(data[:,:,int(data.shape[2]/2)], cmap='hot', interpolation='nearest')
    plt.colorbar()
    #axis off
    plt.axis('off')
    plt.savefig("/home/shailja/ismrmMethodOutput/heatmap_1d.svg")
    plt.show()
    return
file = "/home/shailja/ismrmMethodOutput/pTDA_3directions.nii.gz"
file = "/home/shailja/ismrmMethodOutput/pTDA_2directions.nii.gz"
file = "/home/shailja/ismrmMethodOutput/pTDA_1direction.nii.gz"
crossing_hm(file)

