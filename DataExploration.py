import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import numpy as np

from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy.wcs import WCS
from astropy.coordinates import SkyCoord
from astropy.units import Quantity

def GetCutout(image, cutout, wcs, size=100):
    """
    Get the cropped image from a cutout entry.
    """
    # Taking the centre of the cutout and entering as a SkyCoord
    centre = SkyCoord(cutout[1], cutout[2], unit="deg")

    # Getting the size of the cutout as a Quantity
    size = Quantity([abs(cutout[4]-cutout[8]), abs(cutout[3]-cutout[5])], unit="deg")

    # Cropping the image
    croppedImg = Cutout2D(image, centre, size, wcs=wcs)

    return croppedImg

# Dictionary containing all data files
DataDict = {
      "NIRH": "EUC_MER_BGSUB-MOSAIC-NIR-H_TILE102159484-39CF67_20241024T214009.099906Z_00.00.fits", 
      "NIRJ": "EUC_MER_BGSUB-MOSAIC-NIR-J_TILE102159484-C026DB_20241024T213141.416722Z_00.00.fits", 
      "NIRY": "EUC_MER_BGSUB-MOSAIC-NIR-Y_TILE102159484-A9CCA7_20241024T221227.957725Z_00.00.fits", 
       "VIS": "EUC_MER_BGSUB-MOSAIC-VIS_TILE102159484-116033_20241025T015934.885975Z_00.00.fits", 
       "CAT": "EUC_MER_FINAL-CAT_TILE102159484-EF6D85_20241026T003047.133877Z_00.00.fits", 
    "CUTOUT": "EUC_MER_FINAL-CUTOUTS-CAT_TILE102159484-73BCF1_20241025T145359.184204Z_00.00.fits", 
     "MORPH": "EUC_MER_FINAL-MORPH-CAT_TILE102159484-AE979F_20241026T003045.182961Z_00.00.fits", 
      "GSED": "EUC_PHZ_GALAXYSED__20241120T003959.957136Z_00.00.fits",
    "PHZCAT": "EUC_PHZ_PHZCAT__20241120T003850.158262Z_00.00.fits", 
      "SSED": "EUC_PHZ_STARSED__20241120T003936.665995Z_00.00.fits", 
    "SPELIN":"EUC_SPE_WIDE-CAT-LIN-102159484_N_20241110T054343.637093Z_00.00.fits", 
    "SPEMOD": "EUC_SPE_WIDE-CAT-MOD-102159484_N_20241110T054509.870865Z_00.00.fits", 
      "SPEZ": "EUC_SPE_WIDE-CAT-Z-102159484_N_20241110T054253.801351Z_00.00.fits"
}

# Which image to use
filt = "NIRZ"

# Getting the cutouts and image
hdulCutouts = fits.open(f"/home/brad/Downloads/DIP_2026/{DataDict["CUTOUT"]}")
hdulImage  = fits.open(f"/home/brad/Downloads/DIP_2026/{DataDict[filt]}")

# Getting the world coordinate system
wcs = WCS(hdulImage[0].header)

# Looping through the cutouts
for cutout in hdulCutouts[1].data[0:2]:
    
    # Cropping the image to the cutout box
    croppedImg = GetCutout(hdulImage[0].data, cutout, wcs, 100)

    # Plotting the cropped image
    fig, ax = plt.subplots(subplot_kw=dict(projection=croppedImg.wcs))
    ax.imshow(croppedImg.data, cmap="plasma", norm=LogNorm())
    ax.set_xlabel("Right Ascension")
    ax.set_ylabel("Declination")
    plt.gca().invert_yaxis()
    # fig.savefig(f"{filter}.png")
    plt.show()