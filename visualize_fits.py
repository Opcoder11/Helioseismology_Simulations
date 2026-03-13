import os
import matplotlib.pyplot as plt
from sunpy.map import Map
from aiapy.calibrate import update_pointing, register
from aiapy.calibrate.util import get_pointing_table
from astropy.time import Time
from astropy import units as u
import warnings

warnings.filterwarnings("ignore")

# Create output folder
os.makedirs("plots", exist_ok=True)

# Get list of .fits files
fits_dir = "data"
fits_files = [f for f in os.listdir(fits_dir) if f.endswith(".fits")]

print(f"Found {len(fits_files)} FITS files.")

# Load all maps
maps = []
for file in fits_files:
    try:
        full_path = os.path.join(fits_dir, file)
        map_obj = Map(full_path)
        maps.append(map_obj)
    except Exception as e:
        print(f"❌ Error loading {file}: {e}")

# If no maps were loaded, exit
if not maps:
    print("No valid FITS files to process.")
    exit()

# Compute time range for pointing table
map_times = [m.date for m in maps]
start_time = min(map_times) - 3 * 3600 * u.s
end_time = max(map_times) + 3 * 3600 * u.s

print(f"Downloading pointing table from JSOC between {start_time} and {end_time}...")

# Get pointing table
pointing_table = get_pointing_table(time_range=(start_time, end_time), source="jsoc")

# Process each map
for aia_map in maps:
    try:
        aia_map_updated = update_pointing(aia_map, pointing_table=pointing_table)
        aia_map_registered = register(aia_map_updated)

        # Make timestamp filename-safe (Windows does not allow ':')
        safe_time = str(aia_map.date).replace(":", "-")
        filename = f"plots/aia_{aia_map.wavelength.value}_{safe_time}.png"

        aia_map_registered.plot()
        plt.title(f"AIA Calibrated Map: {aia_map.wavelength}")
        plt.savefig(filename)
        plt.close()
        print(f"✅ Saved plot to {filename}")

    except Exception as e:
        print(f"❌ Error processing {file}: {e}")
