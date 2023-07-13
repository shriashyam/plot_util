import numpy as np
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy.ma as ma

def plot_util(control_file, expr_file, var_name = "", lat = None, lon = None, X = None, Y = None):
	
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
	elif var_name not in common_vars:
		# check if variable (var_name) is in both datasets, else return with error message
		print(var_name + " not in both control and experimental datasets.")
		return
	elif "lat" not in common_vars and "lon" not in common_vars:
		# check if latitude and longitude in both datasets, else return with error message
		print("Latitude and longitude not found in control and experimental datasets.")
		return
	elif len(np.squeeze(control_ds[var_name]).shape) == 2 or len(np.squeeze(expr_ds[var_name]).shape) == 2:
		# plot_util control_file expr_file var_name: make three plots with a variable (var_name)
		# make experimental, control, and difference plots
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
		if not lat == None:
			Y = np.abs(ma.getdata(control_ds["lat"][:,0])-lat).argmin()
		if not lon == None:
			X = np.abs(ma.getdata(control_ds["lon"][0,:])-lon).argmin()
		if X == None or Y == None:
			print("Provide X/Y or latitude/longitude values.")
			return
		data = np.array([xr.DataArray.to_numpy(control_ds[var_name])[:,Y,X],xr.DataArray.to_numpy(expr_ds[var_name])[:,Y,X],xr.DataArray.to_numpy(expr_ds[var_name])[:,Y,X]-xr.DataArray.to_numpy(control_ds[var_name][:,Y,X])])
		titles = np.array(["Control", "Experimental", "Difference"])
		for i in range(3):
			plt.figure()
			plt.plot(xr.DataArray.to_numpy(control_ds["time"]),data[i,:])
			plt.xlabel("Time")
			plt.ylabel(var_name)
			plt.title("Change Over Time in " + titles[i] + " " + var_name + " at Latitude " + str(round(xr.DataArray.to_numpy(control_ds["lat"])[Y,0])) + " and Longitude " + str(round(xr.DataArray.to_numpy(control_ds["lon"])[0,X])))
			plt.savefig(var_name + titles[i] + "timeseries.png")
		return
plot_util("sfccat.nc", "sfccat.nc", var_name = "tmp2m", lon = 23, lat = -36)

