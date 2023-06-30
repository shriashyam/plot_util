import os
import netCDF4 as nc
import numpy.ma as ma
import numpy as np

def plot_util(control_file, expr_file, timeseries = None, var_name = "", lat = None, lon = None, X = None, Y = None):
	
	# if control_file exists and is netCDF, extract control dataset as masked array, else return with error message
	try:
		control_ds = nc.Dataset(control_file)
	except:
		print("Control file not found.")
		return

	# if expr_file exists and is netCDF, extract experimental dataset as masked array, else return with error message
	try:
		expr_ds = nc.Dataset(expr_file)
	except:
		print("Experimental file not found.")
		return

	# make numpy array with common variables in control and experimental datasets
	common_vars = np.intersect1d(np.array(list(control_ds.variables.keys())), np.array(list(expr_ds.variables.keys())))

	if var_name == "":
		# plot_util control_file expr_file: list all common variables in the two files
		print("The following variables are found in both control and experimental datasets: ")
		print(*common_vars,sep=', ')
	elif timeseries == None:
		# plot_util control_file expr_file var_name: make three plots with a variable (var_name)
		
		# check if variable (var_name) is in both datasets, else return with error message
		# if variable (var_name) is in both datasets, plot control, experimental, difference
		if var_name in common_vars:
			f = open("Plots.jnl", "w")
			# control graph
			f.write("set data " + control_file + " \n")
			f.write("shade/title = \"Control " + var_name + "\" " + var_name + "; go land \n")
			f.write("frame/file=CONTROL" + var_name + ".gif \n")
			# expr graph
			f.write("set data " + expr_file + " \n")
			f.write("shade/title = \"Experimental " + var_name + "\" " + var_name + "; go land \n")
			f.write("frame/file=EXPR" + var_name + ".gif \n")
			# difference graph
			os.system("cp " + control_file + " control_edited.nc")
			os.system("ncrename -v " + var_name + ",old" + var_name + " control_edited.nc")
			f.write("use control_edited.nc \n")
			f.write("save/file=concat.cdf old" + var_name + "\n")
			f.write("use " + expr_file + "\n")
			f.write("save/append/file=concat.cdf " + var_name + "\n")
			f.write("set data concat.cdf \n")
			f.write("shade/palette=cmocean_balance/title = \"Difference (exp - con) in " + var_name + "\" " + var_name + "-old" + var_name + "; go land \n")
			f.write("frame/file=DIFF" + var_name + ".gif \n")
			# plot and reset
			f.close()
			os.system("ferret -script Plots.jnl")
			os.system("rm Plots.jnl")	
			os.system("rm control_edited.nc")
			os.system("rm concat.cdf")
		else:
			print(var_name + " not in both control and experimental datasets.")

plot_util("/work2/noaa/nems/sshyam/comparisons/base/sfcf024.nc", "/work2/noaa/nems/sshyam/comparisons/noise3/sfcf024.nc", var_name = "ugrd10m")
