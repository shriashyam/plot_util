import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import sys

def plot_util(control_file, expr_file, timeseries = None, var_name = "", lat = None, lon = None, X = None, Y = None):
	
	# if control_file exists and is netCDF, extract control dataset as masked array, else return with error message
	try:
		control_ds = xr.open_dataset(control_file)
	except:
		print("Control file not found.")
		return

	# if expr_file exists and is netCDF, extract experimental dataset as masked array, else return with error message
	try:
		expr_ds = xr.open_dataset(expr_file)
	except:
		print("Experimental file not found.")
		return

	# make numpy array with common variables in control and experimental datasets
	common_vars = np.intersect1d(np.array(list(control_ds.variables.keys())), np.array(list(expr_ds.variables.keys())))

	if var_name == "":
		# plot_util control_file expr_file: list all common variables in the two files
		print("The following variables are found in both control and experimental datasets: ")
		print(*common_vars,sep=', ')
		return
	elif timeseries == None:
		# plot_util control_file expr_file var_name: make three plots with a variable (var_name)
		
		# check if variable (var_name) is in both datasets, else return with error message
		# if variable (var_name) is in both datasets, plot control, experimental, difference
		if var_name in common_vars:
			# check if latitude and longitude in both datasets, else return with error message
			if "lat" in common_vars and "lon" in common_vars:
				#setup
				data = np.array([np.squeeze(control_ds[var_name]), np.squeeze(expr_ds[var_name]), np.squeeze(expr_ds[var_name]-control_ds[var_name])])
				titles = np.array(["Control", "Experimental", "Difference"])
				for i in range(3):
					fig = plt.figure()
					ax = plt.axes(projection=ccrs.PlateCarree())
					plt.contourf(control_ds["lon"], control_ds["lat"], data[i, :, :], transform = ccrs.PlateCarree())
					ax.add_feature(cfeature.COASTLINE)
					cbar = plt.colorbar()
					cbar.set_label(var_name)
					plt.title(titles[i] + " " + var_name)
					plt.savefig(var_name + titles[i] + ".png")

				return
			else:
				print("Latitude and longitude not found in control and experimental datasets.")
				return
		else:
			print(var_name + " not in both control and experimental datasets.")
			return

plot_util("/work2/noaa/nems/sshyam/comparisons/base/sfcf024.nc", "/work2/noaa/nems/sshyam/comparisons/noise1/sfcf024.nc", var_name = "ugrd10m")
