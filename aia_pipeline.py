import numpy as np
import matplotlib.pyplot as plt
from sunpy.map import Map
from sunpy.net import jsoc, attrs as a
from astropy import units as u
from aiapy.calibrate import register, update_pointing
import warnings

warnings.filterwarnings('ignore')

print("Modules loaded successfully.")

# Search Data
time_range = a.Time('2016-06-16T07:21:00', '2016-06-16T07:21:20')
wavelengths = (
    a.Wavelength(171 * u.angstrom) |
    a.Wavelength(94 * u.angstrom) |
    a.Wavelength(193 * u.angstrom) |
    a.Wavelength(211 * u.angstrom) |
    a.Wavelength(335 * u.angstrom) |
    a.Wavelength(131 * u.angstrom)
)

client = jsoc.JSOCClient()
response = client.search(
    time_range,
    jsoc.Series("aia.lev1_euv_12s"),
    wavelengths,
    jsoc.Notify("omprakash23@iiserbpr.ac.in")  # Put your real email here
)

print(response)

downloaded_files = client.fetch(response)
print(f"Downloaded files:\n{downloaded_files}")

for file in downloaded_files:
    aia_map = Map(file)
    aia_map_updated = update_pointing(aia_map)
    aia_map_registered = register(aia_map_updated)

    aia_map_registered.plot()
    plt.title(f"AIA Calibrated Map: {aia_map.wavelength}")
    plt.show()
