import pandas as pd
from  cosmocalc import cosmocalc
import matplotlib.pyplot as plt
import numpy as np



all_blazars = pd.read_csv("blazars.txt") # from 4LAC blazars catalog
selected_blazars = pd.DataFrame(all_blazars)
flux_error_column = pd.read_csv("flux_eror.txt")
flux_error =pd.DataFrame(flux_error_column)
flux_error.columns=["Energy_error"]

selected_blazars.columns = ["Catalog_name", "RA", "DEC", "Sign","Flux","Energy_Flux","Spectrum type","PL index","LP_alpha","LP_beta","Type","Assoc_name","Redshift","Synchrotron_peak"]

selected_blazars.insert(7,"Energy_error",flux_error.Energy_error,True)

# for selecting blazars which redshift is between 2 < z < 2.5
#selected_blazars=selected_blazars.loc[(selected_blazars.Redshift > 2.0)&(selected_blazars.Redshift < 2.5)]
selected_blazars.sort_values(by=["Redshift"],inplace=True)
distance = []
for i in selected_blazars["Redshift"]:
    distances = cosmocalc(i,H0=71,WM = 0.3,WV = 0.7) # convert z to distance unit(cm)
    distance.append(distances["DL_cm"])

# make a column for distance values in main DF
selected_blazars.insert(13,"Distance",distance,True)

# Calculate Luminosity and add it as a column ( L = 4*pi*R^2*F*(1+z) )
selected_blazars["Luminosity"] = (4*np.pi)*(selected_blazars["Distance"]**2)*selected_blazars["Energy_Flux"]*(1+selected_blazars["Redshift"])
selected_blazars["Luminosity_error"] = (4*np.pi)*(selected_blazars["Distance"]**2)*selected_blazars["Energy_error"]*(1+selected_blazars["Redshift"])
selected_blazars = selected_blazars[selected_blazars["Redshift"].notnull()]
#plt.scatter(selected_blazars.Redshift,selected_blazars.Luminosity,s=15,c = "red",alpha = 0.5) # z - L plot z->x, L->y
plt.xlabel("z")
plt.ylabel(r'L ($\mathregular {erg \ \ s^{-1}}$)')
plt.yscale("log")
plt.errorbar(selected_blazars.Redshift,selected_blazars.Luminosity,yerr = selected_blazars.Luminosity_error,fmt=".",c="red",elinewidth =1.5)
plt.ylim(1e+45,5e+49)

# z axis scale will be  0.0, 0.5 ..,4

ticks = []
x= 0
while x <= 4: 
    ticks.append(x)
    x=x+0.5
"""ticks = [range(1,5,0.5)]
print(ticks)

"""
plt.xticks(ticks)

# add two vertical lines on z = 2 and z = 2.5
xpoints = [2,2.5]
for p in xpoints:
    plt.axvline(p)


plt.show()