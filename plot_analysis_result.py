
import os, sys
import ROOT
import numpy as np
import pickle
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy.optimize import curve_fit
from common_functions import MyArray1D
from common_functions import MyArray3D

import common_functions

MSCL_cut = common_functions.MSCL_cut
MSCW_cut = common_functions.MSCW_cut
logE_threshold = common_functions.logE_threshold
logE_axis = common_functions.logE_axis
logE_nbins = common_functions.logE_nbins
logE_bins = common_functions.logE_bins
gcut_bins = common_functions.gcut_bins
xvar_bins = common_functions.xvar_bins
yvar_bins = common_functions.yvar_bins
xoff_bins = common_functions.xoff_bins
yoff_bins = common_functions.yoff_bins
xoff_start = common_functions.xoff_start
xoff_end = common_functions.xoff_end
yoff_start = common_functions.yoff_start
yoff_end = common_functions.yoff_end
gcut_start = common_functions.gcut_start
gcut_end = common_functions.gcut_end
SaveFITS = common_functions.SaveFITS
GetSlicedDataCubeMap = common_functions.GetSlicedDataCubeMap
GetSlicedDataCubeMapGALFA = common_functions.GetSlicedDataCubeMapGALFA
ReadRunListFromFile = common_functions.ReadRunListFromFile
build_skymap = common_functions.build_skymap
smooth_image = common_functions.smooth_image
PlotSkyMap = common_functions.PlotSkyMap
PlotCountProjection = common_functions.PlotCountProjection
GetRegionIntegral = common_functions.GetRegionIntegral
make_flux_map = common_functions.make_flux_map
make_significance_map = common_functions.make_significance_map
DefineRegionOfInterest = common_functions.DefineRegionOfInterest
DefineRegionOfExclusion = common_functions.DefineRegionOfExclusion
PrintAndPlotInformationRoI = common_functions.PrintAndPlotInformationRoI
GetRadialProfile = common_functions.GetRadialProfile
fit_2d_model = common_functions.fit_2d_model
matrix_rank = common_functions.matrix_rank
skymap_size = common_functions.skymap_size
fine_skymap_size = common_functions.fine_skymap_size
skymap_bins = common_functions.skymap_bins
fine_skymap_bins = common_functions.fine_skymap_bins
GetGammaSourceInfo = common_functions.GetGammaSourceInfo
build_radial_symmetric_model = common_functions.build_radial_symmetric_model
doFluxCalibration = common_functions.doFluxCalibration
diffusion_func = common_functions.diffusion_func
significance_li_and_ma = common_functions.significance_li_and_ma
coordinate_type = common_functions.coordinate_type
ConvertRaDecToGalactic = common_functions.ConvertRaDecToGalactic
plot_camera_frame_power_spectrum = common_functions.plot_camera_frame_power_spectrum
Normalized_MSCL_cut = common_functions.Normalized_MSCL_cut
Normalized_MSCW_cut = common_functions.Normalized_MSCW_cut


fig, ax = plt.subplots()
figsize_x = 8.6
figsize_y = 6.4
fig.set_figheight(figsize_y)
fig.set_figwidth(figsize_x)

fig_fontsize = 16

smi_dir = os.environ.get("SMI_DIR")
smi_input = os.environ.get("SMI_INPUT")
#smi_output = os.environ.get("SMI_OUTPUT")
smi_output = "/nevis/ged/data/rshang/smi_output/output_mtx_paper"
#smi_output = "/nevis/ged/data/rshang/smi_output/output_default"
#smi_output = "/nevis/ged/data/rshang/smi_output/output_20250417"
#smi_output = "/nevis/ged/data/rshang/smi_output/output_20250421"

sky_tag = os.environ.get("SKY_TAG")

smooth_size = 0.06 # flux measurement
#smooth_size = 0.08
#smooth_size = 0.10
#smooth_size = 0.15
#smooth_size = 0.24

norm_smooth_size = [3.*smooth_size for i in range(0,logE_nbins)]
for logE in range(0,logE_nbins):
    scale_size = max(3.,float(logE))
    norm_smooth_size[logE] = scale_size*smooth_size

zoomin = 1.0
#zoomin = 0.5

ana_tag = sky_tag

qual_cut = 0.
#qual_cut = 20.

min_elev_cut = 40.
#min_elev_cut = 50.
#max_elev_cut = 60.
#min_elev_cut = 60.
max_elev_cut = 90.
cr_qual_cut = 1e10

source_name = sys.argv[1]
src_ra = float(sys.argv[2])
src_dec = float(sys.argv[3])
onoff = sys.argv[4]

n_mimic = 0
if onoff=='ON':
    n_mimic = 0
    #n_mimic = 5

#input_epoch = ['V4']
#input_epoch = ['V5']
#input_epoch = ['V6']
input_epoch = ['V4','V5','V6']
#input_epoch = ['V5','V6']

logE_min = logE_axis.get_bin(np.log10(0.1))+1
logE_mid = logE_axis.get_bin(np.log10(1.0))+1
logE_max = logE_nbins
fit_radial_profile = False
radial_bin_scale = 0.1

include_syst_error = True
#include_syst_error = False
plot_tag = ana_tag
if include_syst_error:
    plot_tag += '_syst'
else:
    plot_tag += '_nosyst'

if 'Crab' in source_name:
    fit_radial_profile = False
if 'SNR_G189_p03' in source_name:
    fit_radial_profile = False
if 'PSR_J1856_p0245' in source_name:
    fit_radial_profile = False
if 'PSR_J1907_p0602' in source_name:
    fit_radial_profile = False
if 'SS433' in source_name:
    fit_radial_profile = False
if 'PSR_J2021_p4026' in source_name:
    fit_radial_profile = False
if 'PSR_J2229_p6114' in source_name:
    fit_radial_profile = False
if 'Geminga' in source_name:
    fit_radial_profile = True
    radial_bin_scale = 0.5
if 'SNR_G150_p4' in source_name:
    fit_radial_profile = False
    radial_bin_scale = 0.5

if 'Cas_A' in source_name:
    logE_min = logE_axis.get_bin(np.log10(0.3))+1
    logE_mid = logE_axis.get_bin(np.log10(1.0))+1
if 'PSR_J1856_p0245' in source_name:
    logE_min = logE_axis.get_bin(np.log10(0.3))+1
    logE_mid = logE_axis.get_bin(np.log10(1.0))+1
if 'PSR_J1907_p0602' in source_name:
    #logE_min = logE_axis.get_bin(np.log10(0.3))+1
    #logE_mid = logE_axis.get_bin(np.log10(3.0))+1
    logE_min = logE_axis.get_bin(np.log10(1.0))+1
    logE_mid = logE_axis.get_bin(np.log10(3.0))+1
if 'PSR_J2021_p3651' in source_name:
    logE_min = logE_axis.get_bin(np.log10(1.0))+1
    logE_mid = logE_axis.get_bin(np.log10(3.0))+1
if 'Geminga' in source_name:
    logE_min = logE_axis.get_bin(np.log10(0.2))+1
    logE_mid = logE_axis.get_bin(np.log10(3.0))+1
if 'PSR_J2229_p6114' in source_name:
    logE_min = logE_axis.get_bin(np.log10(0.5))+1
    logE_mid = logE_axis.get_bin(np.log10(1.7))+1

xsky_start = src_ra+fine_skymap_size
xsky_end = src_ra-fine_skymap_size
ysky_start = src_dec-fine_skymap_size
ysky_end = src_dec+fine_skymap_size

if coordinate_type == 'galactic':
    src_gal_l, src_gal_b = ConvertRaDecToGalactic(src_ra, src_dec)
    xsky_start = src_gal_l+fine_skymap_size
    xsky_end = src_gal_l-fine_skymap_size
    ysky_start = src_gal_b-fine_skymap_size
    ysky_end = src_gal_b+fine_skymap_size

if onoff=='OFF':
    coordinate_type = 'relative'
    skymap_size = 2.
    skymap_bins = 80
    xsky_start = skymap_size
    xsky_end = -skymap_size
    ysky_start = skymap_size
    ysky_end = -skymap_size

print (f"xsky_start = {xsky_start}, xsky_end = {xsky_end}, ysky_start = {ysky_start}, ysky_end = {ysky_end}")

if onoff=='ON':
    skymap_bins = fine_skymap_bins
    print (f'original skymap_bins = {skymap_bins}')
    skymap_bin_size = 2.*fine_skymap_size/float(skymap_bins)

region_name = source_name
if onoff=='OFF':
    region_name = 'Validation'
all_roi_name, all_roi_x, all_roi_y, all_roi_r = DefineRegionOfInterest(region_name,src_ra,src_dec,coordinate_type=coordinate_type)
all_excl_name, all_excl_x, all_excl_y, all_excl_r = DefineRegionOfExclusion(region_name,src_ra,src_dec,coordinate_type=coordinate_type)
print (f"all_roi_name = {all_roi_name}")
print (f"all_roi_x = {all_roi_x}")
print (f"all_roi_y = {all_roi_y}")
print (f"all_roi_r = {all_roi_r}")

max_exposure = 1000.
#max_exposure = 10.
#max_exposure = 50.
#max_exposure = 100.

plot_tag += f'_{max_exposure}hr'

total_exposure = 0.
good_exposure = 0.
mimic_exposure = [0.] * n_mimic 
list_run_nsb = []
list_run_elev = []
list_run_azim = []
sum_incl_sky_map = []
sum_data_sky_map = []
sum_bkgd_sky_map = []
sum_syst_sky_map = []
sum_incl_sky_map_smooth = []
sum_data_sky_map_smooth = []
sum_bkgd_sky_map_smooth = []
sum_syst_sky_map_smooth = []
sum_excess_sky_map_smooth = []
sum_significance_sky_map = []
sum_flux_sky_map = []
sum_flux_err_sky_map = []
sum_flux_syst_sky_map = []
sum_flux_sky_map_smooth = []
sum_flux_err_sky_map_smooth = []
sum_flux_syst_sky_map_smooth = []
for logE in range(0,logE_nbins):
    sum_incl_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_data_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_bkgd_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_syst_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_incl_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_data_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_bkgd_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_syst_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_excess_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_significance_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_flux_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_flux_err_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_flux_syst_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_flux_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_flux_err_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_flux_syst_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
sum_data_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_data_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_data_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_bkgd_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_syst_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_bkgd_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_syst_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_bkgd_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_syst_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_significance_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_significance_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_significance_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_excess_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_excess_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_excess_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_err_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_syst_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_sky_map_allE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_err_sky_map_allE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_syst_sky_map_allE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_err_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_syst_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_err_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_syst_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_sky_map_LE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_err_sky_map_LE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_syst_sky_map_LE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_sky_map_HE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_err_sky_map_HE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
sum_flux_syst_sky_map_HE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)

sum_mimic_incl_sky_map = []
sum_mimic_data_sky_map = []
sum_mimic_bkgd_sky_map = []
sum_mimic_incl_sky_map_smooth = []
sum_mimic_data_sky_map_smooth = []
sum_mimic_bkgd_sky_map_smooth = []
sum_mimic_excess_sky_map_smooth = []
sum_mimic_significance_sky_map = []
sum_mimic_flux_sky_map = []
sum_mimic_flux_err_sky_map = []
sum_mimic_flux_sky_map_smooth = []
sum_mimic_flux_err_sky_map_smooth = []
sum_mimic_data_sky_map_allE = []
sum_mimic_data_sky_map_LE = []
sum_mimic_data_sky_map_HE = []
sum_mimic_bkgd_sky_map_allE = []
sum_mimic_bkgd_sky_map_LE = []
sum_mimic_bkgd_sky_map_HE = []
sum_mimic_significance_sky_map_allE = []
sum_mimic_significance_sky_map_LE = []
sum_mimic_significance_sky_map_HE = []
sum_mimic_excess_sky_map_allE = []
sum_mimic_excess_sky_map_LE = []
sum_mimic_excess_sky_map_HE = []
sum_mimic_flux_sky_map_allE = []
sum_mimic_flux_err_sky_map_allE = []
sum_mimic_flux_sky_map_allE_smooth = []
sum_mimic_flux_err_sky_map_allE_smooth = []
sum_mimic_flux_sky_map_LE = []
sum_mimic_flux_err_sky_map_LE = []
sum_mimic_flux_sky_map_HE = []
sum_mimic_flux_err_sky_map_HE = []
sum_mimic_flux_sky_map_LE_smooth = []
sum_mimic_flux_err_sky_map_LE_smooth = []
sum_mimic_flux_sky_map_HE_smooth = []
sum_mimic_flux_err_sky_map_HE_smooth = []
for mimic in range(1,n_mimic+1):
    mimic_incl_sky_map = []
    mimic_data_sky_map = []
    mimic_bkgd_sky_map = []
    mimic_incl_sky_map_smooth = []
    mimic_data_sky_map_smooth = []
    mimic_bkgd_sky_map_smooth = []
    mimic_excess_sky_map_smooth = []
    mimic_significance_sky_map = []
    mimic_flux_sky_map = []
    mimic_flux_err_sky_map = []
    mimic_flux_sky_map_smooth = []
    mimic_flux_err_sky_map_smooth = []
    for logE in range(0,logE_nbins):
        mimic_incl_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
        mimic_data_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
        mimic_bkgd_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
        mimic_incl_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
        mimic_data_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
        mimic_bkgd_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
        mimic_excess_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
        mimic_significance_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
        mimic_flux_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
        mimic_flux_err_sky_map += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
        mimic_flux_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
        mimic_flux_err_sky_map_smooth += [MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)]
    sum_mimic_incl_sky_map += [mimic_incl_sky_map]
    sum_mimic_data_sky_map += [mimic_data_sky_map]
    sum_mimic_bkgd_sky_map += [mimic_bkgd_sky_map]
    sum_mimic_incl_sky_map_smooth += [mimic_incl_sky_map_smooth]
    sum_mimic_data_sky_map_smooth += [mimic_data_sky_map_smooth]
    sum_mimic_bkgd_sky_map_smooth += [mimic_bkgd_sky_map_smooth]
    sum_mimic_excess_sky_map_smooth += [mimic_excess_sky_map_smooth]
    sum_mimic_significance_sky_map += [mimic_significance_sky_map]
    sum_mimic_flux_sky_map += [mimic_flux_sky_map]
    sum_mimic_flux_err_sky_map += [mimic_flux_err_sky_map]
    sum_mimic_flux_sky_map_smooth += [mimic_flux_sky_map_smooth]
    sum_mimic_flux_err_sky_map_smooth += [mimic_flux_err_sky_map_smooth]
for mimic in range(1,n_mimic+1):
    mimic_data_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_data_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_data_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_bkgd_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_bkgd_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_bkgd_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_significance_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_significance_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_significance_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_excess_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_excess_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_excess_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_err_sky_map_allE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_sky_map_allE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_err_sky_map_allE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_err_sky_map_LE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_err_sky_map_HE = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_sky_map_LE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_err_sky_map_LE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_sky_map_HE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    mimic_flux_err_sky_map_HE_smooth = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    sum_mimic_data_sky_map_allE += [mimic_data_sky_map_allE]
    sum_mimic_data_sky_map_LE += [mimic_data_sky_map_LE]
    sum_mimic_data_sky_map_HE += [mimic_data_sky_map_HE]
    sum_mimic_bkgd_sky_map_allE += [mimic_bkgd_sky_map_allE]
    sum_mimic_bkgd_sky_map_LE += [mimic_bkgd_sky_map_LE]
    sum_mimic_bkgd_sky_map_HE += [mimic_bkgd_sky_map_HE]
    sum_mimic_significance_sky_map_allE += [mimic_significance_sky_map_allE]
    sum_mimic_significance_sky_map_LE += [mimic_significance_sky_map_LE]
    sum_mimic_significance_sky_map_HE += [mimic_significance_sky_map_HE]
    sum_mimic_excess_sky_map_allE += [mimic_excess_sky_map_allE]
    sum_mimic_excess_sky_map_LE += [mimic_excess_sky_map_LE]
    sum_mimic_excess_sky_map_HE += [mimic_excess_sky_map_HE]
    sum_mimic_flux_sky_map_allE += [mimic_flux_sky_map_allE]
    sum_mimic_flux_err_sky_map_allE += [mimic_flux_err_sky_map_allE]
    sum_mimic_flux_sky_map_allE_smooth += [mimic_flux_sky_map_allE_smooth]
    sum_mimic_flux_err_sky_map_allE_smooth += [mimic_flux_err_sky_map_allE_smooth]
    sum_mimic_flux_sky_map_LE += [mimic_flux_sky_map_LE]
    sum_mimic_flux_err_sky_map_LE += [mimic_flux_err_sky_map_LE]
    sum_mimic_flux_sky_map_HE += [mimic_flux_sky_map_HE]
    sum_mimic_flux_err_sky_map_HE += [mimic_flux_err_sky_map_HE]
    sum_mimic_flux_sky_map_LE_smooth += [mimic_flux_sky_map_LE_smooth]
    sum_mimic_flux_err_sky_map_LE_smooth += [mimic_flux_err_sky_map_LE_smooth]
    sum_mimic_flux_sky_map_HE_smooth += [mimic_flux_sky_map_HE_smooth]
    sum_mimic_flux_err_sky_map_HE_smooth += [mimic_flux_err_sky_map_HE_smooth]


sum_data_xyoff_map = []
sum_fit_xyoff_map = []
sum_err_xyoff_map = []
sum_init_err_xyoff_map = []
for logE in range(0,logE_nbins):
    sum_data_xyoff_map += [MyArray3D(x_bins=xoff_bins[logE],start_x=xoff_start,end_x=xoff_end,y_bins=yoff_bins[logE],start_y=yoff_start,end_y=yoff_end,z_bins=gcut_bins,start_z=gcut_start,end_z=gcut_end)]
    sum_fit_xyoff_map += [MyArray3D(x_bins=xoff_bins[logE],start_x=xoff_start,end_x=xoff_end,y_bins=yoff_bins[logE],start_y=yoff_start,end_y=yoff_end,z_bins=gcut_bins,start_z=gcut_start,end_z=gcut_end)]
    sum_err_xyoff_map += [MyArray3D(x_bins=xoff_bins[logE],start_x=xoff_start,end_x=xoff_end,y_bins=yoff_bins[logE],start_y=yoff_start,end_y=yoff_end,z_bins=gcut_bins,start_z=gcut_start,end_z=gcut_end)]
    sum_init_err_xyoff_map += [MyArray3D(x_bins=xoff_bins[logE],start_x=xoff_start,end_x=xoff_end,y_bins=yoff_bins[logE],start_y=yoff_start,end_y=yoff_end,z_bins=gcut_bins,start_z=gcut_start,end_z=gcut_end)]

sum_data_xyvar_map = []
for logE in range(0,logE_nbins):
    end_x = Normalized_MSCL_cut[len(Normalized_MSCL_cut)-1]
    end_y = Normalized_MSCW_cut[len(Normalized_MSCW_cut)-1]
    sum_data_xyvar_map += [MyArray3D(x_bins=xvar_bins[logE],start_x=-1.,end_x=end_x,y_bins=yvar_bins[logE],start_y=-1.,end_y=end_y,z_bins=1,start_z=0.,end_z=1.)]

n_groups = 0.
for epoch in input_epoch:

    onoff_list = []
    onoff_list += [onoff]
    if onoff=='ON':
        for mimic in range(1,n_mimic+1):
            onoff_list += [f'MIMIC{mimic}']

    for mode in onoff_list:

        input_filename = f'{smi_output}/skymaps_{source_name}_{epoch}_{mode}_{ana_tag}.pkl'
        print (f'reading {input_filename}...')
        if not os.path.exists(input_filename):
            print (f'{input_filename} does not exist.')
            continue
        analysis_result = pickle.load(open(input_filename, "rb"))
        
        for run in range(0,len(analysis_result)):

            run_info = analysis_result[run][0] 
            exposure = run_info[0]
            run_elev = run_info[1]
            run_azim = run_info[2]
            run_nsb = run_info[3]
            print (f"run_nsb = {run_nsb}")

            if run_azim>270.:
                run_azim = run_azim-360.

            if run_elev<min_elev_cut:
                continue
            if run_elev>max_elev_cut:
                continue

            if total_exposure >= max_exposure:
                continue

            if not 'MIMIC' in mode:
                total_exposure += exposure
            else:
                mimic_index = int(mode.strip('MIMIC'))
                mimic_exposure[mimic_index-1] += exposure

            incl_sky_map = analysis_result[run][1] 
            data_sky_map = analysis_result[run][2] 
            bkgd_sky_map = analysis_result[run][3] 
            syst_sky_map = analysis_result[run][4] 
            data_xyoff_map = analysis_result[run][5]
            fit_xyoff_map = analysis_result[run][6]
            data_xyvar_map = analysis_result[run][7]

            for logE in range(0,logE_nbins):
                syst_sky_map[logE].scale(0.5)

            print ("=========================================================================")
            print (f"run = {run}")
            sum_bkgd = 0.
            sum_syst = 0.
            for logE in range(0,logE_nbins):
                data = np.sum(data_sky_map[logE].waxis[:,:,:])
                bkgd = np.sum(bkgd_sky_map[logE].waxis[:,:,:])
                syst = np.sum(syst_sky_map[logE].waxis[:,:,:])
                sum_bkgd += bkgd
                sum_syst += syst
                print (f"logE = {logE}, data = {data}, bkgd = {bkgd:0.1f}, diff = {data-bkgd:0.1f}, syst = {syst:0.1f}")

            if sum_bkgd==0.:
                print (f'bad fitting. reject the run.')
                continue

            if not 'MIMIC' in mode:
                good_exposure += exposure
                list_run_nsb += [run_nsb]
                list_run_elev += [run_elev]
                list_run_azim += [run_azim]
                n_groups += 1.

            logE_peak = 0
            bkgd_peak = 0.
            for logE in range(0,logE_nbins):
                bkgd = np.sum(fit_xyoff_map[logE].waxis[:,:,:])
                if bkgd>bkgd_peak:
                    bkgd_peak = bkgd
                    logE_peak = logE

            for logE in range(0,logE_nbins):
                if logE<logE_peak+logE_threshold: continue
                if logE<logE_min: continue
                if logE>logE_max: continue

                if 'MIMIC' in mode:
                    mimic_index = int(mode.strip('MIMIC'))-1
                    #sum_mimic_incl_sky_map[mimic_index][logE].add(incl_sky_map[logE])
                    sum_mimic_incl_sky_map[mimic_index][logE].add(bkgd_sky_map[logE])
                    sum_mimic_data_sky_map[mimic_index][logE].add(data_sky_map[logE])
                    sum_mimic_bkgd_sky_map[mimic_index][logE].add(bkgd_sky_map[logE])
                else:
                    #sum_incl_sky_map[logE].add(incl_sky_map[logE])
                    sum_incl_sky_map[logE].add(bkgd_sky_map[logE])
                    sum_data_sky_map[logE].add(data_sky_map[logE])
                    sum_bkgd_sky_map[logE].add(bkgd_sky_map[logE])
                    if include_syst_error:
                        #sum_syst_sky_map[logE].addSquare(syst_sky_map[logE])
                        sum_syst_sky_map[logE].add(syst_sky_map[logE],factor=2.)
                    sum_data_xyvar_map[logE].add(data_xyvar_map[logE])
                    sum_data_xyoff_map[logE].add(data_xyoff_map[logE])
                    sum_fit_xyoff_map[logE].add(fit_xyoff_map[logE])

    
for logE in range(0,logE_nbins):
    data_integral = 0.
    model_integral = 0.
    for idx_x in range(0,xoff_bins[logE]):
        for idx_y in range(0,yoff_bins[logE]):
            data_integral += sum_data_xyoff_map[logE].waxis[idx_x,idx_y,0] 
            model_integral += sum_data_xyoff_map[logE].waxis[idx_x,idx_y,1] 
    if model_integral==0.: continue
    for idx_x in range(0,xoff_bins[logE]):
        for idx_y in range(0,yoff_bins[logE]):
            data = sum_data_xyoff_map[logE].waxis[idx_x,idx_y,0] 
            model = sum_data_xyoff_map[logE].waxis[idx_x,idx_y,1]*data_integral/model_integral 
            data_err = max(1.,pow(data,0.5))
            sum_init_err_xyoff_map[logE].waxis[idx_x,idx_y,0] = (data-model)/data_err

for logE in range(0,logE_nbins):
    for idx_x in range(0,xoff_bins[logE]):
        for idx_y in range(0,yoff_bins[logE]):
            for gcut in range(0,gcut_bins):
                data = sum_data_xyoff_map[logE].waxis[idx_x,idx_y,gcut] 
                model = sum_fit_xyoff_map[logE].waxis[idx_x,idx_y,gcut] 
                significance = significance_li_and_ma(data, model, 0.)
                sum_err_xyoff_map[logE].waxis[idx_x,idx_y,gcut] = significance


for logE in range(0,logE_nbins):
    sum_data_xyvar_map[logE].scale(1./good_exposure)
    sum_data_xyoff_map[logE].scale(1./good_exposure)
    sum_fit_xyoff_map[logE].scale(1./good_exposure)

for logE in range(0,logE_nbins):
    sum_incl_sky_map_smooth[logE].reset()
    sum_data_sky_map_smooth[logE].reset()
    sum_bkgd_sky_map_smooth[logE].reset()
    sum_excess_sky_map_smooth[logE].reset()
    sum_incl_sky_map_smooth[logE].add(sum_incl_sky_map[logE])
    sum_data_sky_map_smooth[logE].add(sum_data_sky_map[logE])
    sum_bkgd_sky_map_smooth[logE].add(sum_bkgd_sky_map[logE])
    sum_syst_sky_map_smooth[logE].add(sum_syst_sky_map[logE])
    smooth_image(sum_incl_sky_map_smooth[logE].waxis[:,:,0],sum_incl_sky_map_smooth[logE].xaxis,sum_incl_sky_map_smooth[logE].yaxis,kernel_radius=norm_smooth_size[logE])
    smooth_image(sum_bkgd_sky_map_smooth[logE].waxis[:,:,0],sum_bkgd_sky_map_smooth[logE].xaxis,sum_bkgd_sky_map_smooth[logE].yaxis,kernel_radius=smooth_size)
    smooth_image(sum_syst_sky_map_smooth[logE].waxis[:,:,0],sum_syst_sky_map_smooth[logE].xaxis,sum_syst_sky_map_smooth[logE].yaxis,kernel_radius=smooth_size)
    smooth_image(sum_data_sky_map_smooth[logE].waxis[:,:,0],sum_data_sky_map_smooth[logE].xaxis,sum_data_sky_map_smooth[logE].yaxis,kernel_radius=smooth_size)
    sum_data_sky_map_allE.add(sum_data_sky_map_smooth[logE])
    sum_bkgd_sky_map_allE.add(sum_bkgd_sky_map_smooth[logE])
    sum_syst_sky_map_allE.add(sum_syst_sky_map_smooth[logE])
    if logE>=logE_min and logE<logE_mid:
        sum_data_sky_map_LE.add(sum_data_sky_map_smooth[logE])
        sum_bkgd_sky_map_LE.add(sum_bkgd_sky_map_smooth[logE])
        sum_syst_sky_map_LE.add(sum_syst_sky_map_smooth[logE])
    if logE>=logE_mid and logE<=logE_max:
        sum_data_sky_map_HE.add(sum_data_sky_map_smooth[logE])
        sum_bkgd_sky_map_HE.add(sum_bkgd_sky_map_smooth[logE])
        sum_syst_sky_map_HE.add(sum_syst_sky_map_smooth[logE])

for logE in range(0,logE_nbins):
    for mimic in range(0,n_mimic):
        sum_mimic_incl_sky_map_smooth[mimic][logE].reset()
        sum_mimic_data_sky_map_smooth[mimic][logE].reset()
        sum_mimic_bkgd_sky_map_smooth[mimic][logE].reset()
        sum_mimic_excess_sky_map_smooth[mimic][logE].reset()
        sum_mimic_incl_sky_map_smooth[mimic][logE].add(sum_mimic_incl_sky_map[mimic][logE])
        sum_mimic_data_sky_map_smooth[mimic][logE].add(sum_mimic_data_sky_map[mimic][logE])
        sum_mimic_bkgd_sky_map_smooth[mimic][logE].add(sum_mimic_bkgd_sky_map[mimic][logE])
        smooth_image(sum_mimic_incl_sky_map_smooth[mimic][logE].waxis[:,:,0],sum_incl_sky_map_smooth[logE].xaxis,sum_incl_sky_map_smooth[logE].yaxis,kernel_radius=smooth_size)
        smooth_image(sum_mimic_bkgd_sky_map_smooth[mimic][logE].waxis[:,:,0],sum_bkgd_sky_map_smooth[logE].xaxis,sum_bkgd_sky_map_smooth[logE].yaxis,kernel_radius=smooth_size)
        smooth_image(sum_mimic_data_sky_map_smooth[mimic][logE].waxis[:,:,0],sum_data_sky_map_smooth[logE].xaxis,sum_data_sky_map_smooth[logE].yaxis,kernel_radius=smooth_size)
        sum_mimic_data_sky_map_allE[mimic].add(sum_mimic_data_sky_map_smooth[mimic][logE])
        sum_mimic_bkgd_sky_map_allE[mimic].add(sum_mimic_bkgd_sky_map_smooth[mimic][logE])
        if logE>=logE_min and logE<logE_mid:
            sum_mimic_data_sky_map_LE[mimic].add(sum_mimic_data_sky_map_smooth[mimic][logE])
            sum_mimic_bkgd_sky_map_LE[mimic].add(sum_mimic_bkgd_sky_map_smooth[mimic][logE])
        if logE>=logE_mid and logE<=logE_max:
            sum_mimic_data_sky_map_HE[mimic].add(sum_mimic_data_sky_map_smooth[mimic][logE])
            sum_mimic_bkgd_sky_map_HE[mimic].add(sum_mimic_bkgd_sky_map_smooth[mimic][logE])


plot_logE_min = logE_min
plot_logE_mid = logE_mid
plot_logE_max = logE_max
for logE in range(logE_min,logE_max):
    sum_data = np.sum(sum_data_xyoff_map[logE].waxis[:,:,:])
    if sum_data>0.:
        plot_logE_min = logE
        break
if plot_logE_mid<=plot_logE_min:
    plot_logE_mid = plot_logE_min + 2


print ('=================================================================================')
for logE in range(0,logE_nbins):

    data_sum = np.sum(sum_data_sky_map[logE].waxis[:,:,0])
    bkgd_sum = np.sum(sum_bkgd_sky_map[logE].waxis[:,:,0])

    error = 0.
    stat_error = 0.
    if data_sum>0.:
        error = 100.*(data_sum-bkgd_sum)/data_sum
        stat_error = 100.*pow(data_sum,0.5)/data_sum
    print (f'E = {pow(10.,logE_bins[logE]):0.3f} TeV, data_sum = {data_sum}, bkgd_sum = {bkgd_sum:0.1f}, error = {error:0.1f} +/- {stat_error:0.1f} %')

for logE in range(0,logE_nbins):
    make_significance_map(sum_data_sky_map_smooth[logE],sum_bkgd_sky_map_smooth[logE],sum_significance_sky_map[logE],sum_excess_sky_map_smooth[logE],syst_sky_map=sum_syst_sky_map_smooth[logE])
make_significance_map(sum_data_sky_map_allE,sum_bkgd_sky_map_allE,sum_significance_sky_map_allE,sum_excess_sky_map_allE,syst_sky_map=sum_syst_sky_map_allE)
make_significance_map(sum_data_sky_map_LE,sum_bkgd_sky_map_LE,sum_significance_sky_map_LE,sum_excess_sky_map_LE,syst_sky_map=sum_syst_sky_map_LE)
make_significance_map(sum_data_sky_map_HE,sum_bkgd_sky_map_HE,sum_significance_sky_map_HE,sum_excess_sky_map_HE,syst_sky_map=sum_syst_sky_map_HE)

for mimic in range(0,n_mimic):
    make_significance_map(sum_mimic_data_sky_map_allE[mimic],sum_mimic_bkgd_sky_map_allE[mimic],sum_mimic_significance_sky_map_allE[mimic],sum_mimic_excess_sky_map_allE[mimic])

for logE in range(0,logE_nbins):
    avg_energy = 0.5*(pow(10.,logE_axis.xaxis[logE])+pow(10.,logE_axis.xaxis[logE+1]))
    delta_energy = 0.5*(pow(10.,logE_axis.xaxis[logE+1])-pow(10.,logE_axis.xaxis[logE]))
    make_flux_map(sum_incl_sky_map_smooth[logE],sum_data_sky_map_smooth[logE],sum_bkgd_sky_map_smooth[logE],sum_flux_sky_map_smooth[logE],sum_flux_err_sky_map_smooth[logE],sum_flux_syst_sky_map_smooth[logE],avg_energy,delta_energy,syst_sky_map=sum_syst_sky_map_smooth[logE])
    make_flux_map(sum_incl_sky_map_smooth[logE],sum_data_sky_map[logE],sum_bkgd_sky_map[logE],sum_flux_sky_map[logE],sum_flux_err_sky_map[logE],sum_flux_syst_sky_map[logE],avg_energy,delta_energy,syst_sky_map=sum_syst_sky_map[logE])

for mimic in range(0,n_mimic):
    for logE in range(0,logE_nbins):
        make_flux_map(sum_mimic_incl_sky_map_smooth[mimic][logE],sum_mimic_data_sky_map[mimic][logE],sum_mimic_bkgd_sky_map[mimic][logE],sum_mimic_flux_sky_map[mimic][logE],sum_mimic_flux_err_sky_map[mimic][logE],avg_energy,delta_energy)

for logE in range(plot_logE_min,plot_logE_max):
    PlotSkyMap(fig,'$E^{2}$ dN/dE [$\\mathrm{TeV}\\cdot\\mathrm{cm}^{-2}\\mathrm{s}^{-1}$]',logE,logE+1,sum_flux_sky_map_smooth[logE],f'flux_sky_map_{source_name}_logE{logE}_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='magma',zoomin=zoomin)
    PlotSkyMap(fig,'Background count',logE,logE+1,sum_bkgd_sky_map_smooth[logE],f'bkgd_sky_map_{source_name}_logE{logE}_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='magma',layer=0,zoomin=zoomin)
    PlotSkyMap(fig,'Excess count',logE,logE+1,sum_excess_sky_map_smooth[logE],f'excess_sky_map_{source_name}_logE{logE}_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='magma',layer=0,zoomin=zoomin)
    sum_flux_sky_map_allE.add(sum_flux_sky_map[logE])
    sum_flux_err_sky_map_allE.addSquare(sum_flux_err_sky_map[logE])
    sum_flux_syst_sky_map_allE.add(sum_flux_syst_sky_map[logE])
    sum_flux_sky_map_allE_smooth.add(sum_flux_sky_map_smooth[logE])
    sum_flux_err_sky_map_allE_smooth.addSquare(sum_flux_err_sky_map_smooth[logE])
    sum_flux_syst_sky_map_allE_smooth.add(sum_flux_syst_sky_map_smooth[logE])
    for mimic in range(0,n_mimic):
        sum_mimic_flux_sky_map_allE[mimic].add(sum_mimic_flux_sky_map[mimic][logE])
        sum_mimic_flux_err_sky_map_allE[mimic].addSquare(sum_mimic_flux_err_sky_map[mimic][logE])
    if logE<plot_logE_min: continue
    if logE>plot_logE_max: continue
    if logE>=plot_logE_min and logE<plot_logE_mid:
        sum_flux_sky_map_LE.add(sum_flux_sky_map[logE])
        sum_flux_err_sky_map_LE.addSquare(sum_flux_err_sky_map[logE])
        sum_flux_syst_sky_map_LE.add(sum_flux_syst_sky_map[logE])
        sum_flux_sky_map_LE_smooth.add(sum_flux_sky_map_smooth[logE])
        sum_flux_err_sky_map_LE_smooth.addSquare(sum_flux_err_sky_map_smooth[logE])
        sum_flux_syst_sky_map_LE_smooth.add(sum_flux_syst_sky_map_smooth[logE])
        for mimic in range(0,n_mimic):
            sum_mimic_flux_sky_map_LE[mimic].add(sum_mimic_flux_sky_map[mimic][logE])
            sum_mimic_flux_err_sky_map_LE[mimic].addSquare(sum_mimic_flux_err_sky_map[mimic][logE])
    if logE>=plot_logE_mid and logE<=plot_logE_max:
        sum_flux_sky_map_HE.add(sum_flux_sky_map[logE])
        sum_flux_err_sky_map_HE.addSquare(sum_flux_err_sky_map[logE])
        sum_flux_syst_sky_map_HE.add(sum_flux_syst_sky_map[logE])
        sum_flux_sky_map_HE_smooth.add(sum_flux_sky_map_smooth[logE])
        sum_flux_err_sky_map_HE_smooth.addSquare(sum_flux_err_sky_map_smooth[logE])
        sum_flux_syst_sky_map_HE_smooth.add(sum_flux_syst_sky_map_smooth[logE])
        for mimic in range(0,n_mimic):
            sum_mimic_flux_sky_map_HE[mimic].add(sum_mimic_flux_sky_map[mimic][logE])
            sum_mimic_flux_err_sky_map_HE[mimic].addSquare(sum_mimic_flux_err_sky_map[mimic][logE])
PlotSkyMap(fig,'$E^{2}$ dN/dE [$\\mathrm{TeV}\\cdot\\mathrm{cm}^{-2}\\mathrm{s}^{-1}$]',plot_logE_min,plot_logE_max,sum_flux_sky_map_allE_smooth,f'flux_sky_map_{source_name}_allE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='magma',zoomin=zoomin)
PlotSkyMap(fig,'$E^{2}$ dN/dE [$\\mathrm{TeV}\\cdot\\mathrm{cm}^{-2}\\mathrm{s}^{-1}$]',plot_logE_min,plot_logE_mid,sum_flux_sky_map_LE_smooth,f'flux_sky_map_{source_name}_LE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='magma',zoomin=zoomin)
PlotSkyMap(fig,'$E^{2}$ dN/dE [$\\mathrm{TeV}\\cdot\\mathrm{cm}^{-2}\\mathrm{s}^{-1}$]',plot_logE_mid,plot_logE_max,sum_flux_sky_map_HE_smooth,f'flux_sky_map_{source_name}_HE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='magma',zoomin=zoomin)

if onoff=='ON':
    print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print ('Fit 2d Gaussian (LE)')
    fit_2d_model(sum_data_sky_map_LE, sum_bkgd_sky_map_LE, all_roi_x[0], all_roi_y[0])
    print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print ('Fit 2d Gaussian (HE)')
    fit_2d_model(sum_data_sky_map_HE, sum_bkgd_sky_map_HE, all_roi_x[0], all_roi_y[0])
    print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print ('Fit 2d Gaussian (sum)')
    fit_2d_model(sum_data_sky_map_allE, sum_bkgd_sky_map_allE, all_roi_x[0], all_roi_y[0])
    print ('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

low_energy = int(1000.*pow(10.,logE_bins[plot_logE_min]))
high_energy = int(1000.*pow(10.,logE_bins[plot_logE_mid]))
SaveFITS(sum_flux_sky_map_LE_smooth,f'sum_flux_sky_map_{low_energy}GeV_{high_energy}GeV')
SaveFITS(sum_flux_err_sky_map_LE_smooth,f'sum_flux_err_sky_map_{low_energy}GeV_{high_energy}GeV')
low_energy = int(1000.*pow(10.,logE_bins[plot_logE_mid]))
high_energy = int(1000.*pow(10.,logE_bins[plot_logE_max]))
SaveFITS(sum_flux_sky_map_HE_smooth,f'sum_flux_sky_map_{low_energy}GeV_{high_energy}GeV')
SaveFITS(sum_flux_err_sky_map_HE_smooth,f'sum_flux_err_sky_map_{low_energy}GeV_{high_energy}GeV')
for logE in range(plot_logE_min,plot_logE_max):
    low_energy = int(1000.*pow(10.,logE_bins[logE]))
    high_energy = int(1000.*pow(10.,logE_bins[logE+1]))
    SaveFITS(sum_flux_sky_map_smooth[logE],f'sum_flux_sky_map_{low_energy}GeV_{high_energy}GeV')
    SaveFITS(sum_flux_err_sky_map_smooth[logE],f'sum_flux_err_sky_map_{low_energy}GeV_{high_energy}GeV')

PrintAndPlotInformationRoI(fig,plot_logE_min,plot_logE_mid,plot_logE_max,source_name,sum_data_sky_map,sum_bkgd_sky_map,sum_syst_sky_map,sum_flux_sky_map,sum_flux_err_sky_map,sum_flux_syst_sky_map,sum_mimic_data_sky_map,sum_mimic_bkgd_sky_map,all_roi_name,all_roi_x,all_roi_y,all_roi_r,all_excl_x,all_excl_y,all_excl_r)

    
for logE in range(plot_logE_min,plot_logE_max):
    on_radial_axis, on_profile_axis, on_profile_err_axis, on_profile_syst_axis = GetRadialProfile(sum_flux_sky_map[logE],sum_flux_err_sky_map[logE],sum_flux_syst_sky_map[logE],all_roi_x,all_roi_y,2.5,all_excl_x,all_excl_y,all_excl_r,radial_bin_scale=radial_bin_scale)
    baseline_yaxis = [0. for i in range(0,len(on_radial_axis))]
    fig.clf()
    figsize_x = 7
    figsize_y = 5
    fig.set_figheight(figsize_y)
    fig.set_figwidth(figsize_x)
    axbig = fig.add_subplot()
    axbig.tick_params(axis='both', which='major', labelsize=fig_fontsize*0.8)
    label_x = 'Angular distance [deg]'
    label_y = 'Surface brightness [$\\mathrm{TeV}\\ \\mathrm{cm}^{-2}\\mathrm{s}^{-1}\\mathrm{sr}^{-1}$]'
    axbig.set_xlabel(label_x, fontsize=fig_fontsize)
    axbig.set_ylabel(label_y, fontsize=fig_fontsize)
    axbig.fill_between(on_radial_axis,np.array(baseline_yaxis)-np.array(on_profile_syst_axis),np.array(baseline_yaxis)+np.array(on_profile_syst_axis),alpha=0.2,color='b')
    axbig.plot(on_radial_axis, baseline_yaxis, color='b', ls='dashed')
    axbig.errorbar(on_radial_axis,on_profile_axis,on_profile_err_axis,color='k',marker='+',ls='none')
    axbig.set_title(f'{pow(10.,logE_bins[logE]):0.2f}-{pow(10.,logE_bins[logE+1]):0.2f} TeV')
    fig.savefig(f'output_plots/surface_brightness_{source_name}_logE{logE}_{all_roi_name[0]}_{plot_tag}.png',bbox_inches='tight')
    axbig.remove()

on_radial_axis, on_profile_axis, on_profile_err_axis, on_profile_syst_axis = GetRadialProfile(sum_flux_sky_map_allE,sum_flux_err_sky_map_allE,sum_flux_syst_sky_map_allE,all_roi_x,all_roi_y,2.5,all_excl_x,all_excl_y,all_excl_r,radial_bin_scale=radial_bin_scale)
baseline_yaxis = [0. for i in range(0,len(on_radial_axis))]
fig.clf()
figsize_x = 7
figsize_y = 5
fig.set_figheight(figsize_y)
fig.set_figwidth(figsize_x)
axbig = fig.add_subplot()
axbig.tick_params(axis='both', which='major', labelsize=fig_fontsize*0.8)
label_x = 'Angular distance [deg]'
label_y = 'Surface brightness [$\\mathrm{TeV}\\ \\mathrm{cm}^{-2}\\mathrm{s}^{-1}\\mathrm{sr}^{-1}$]'
axbig.set_xlabel(label_x, fontsize=fig_fontsize)
axbig.set_ylabel(label_y, fontsize=fig_fontsize)
axbig.set_title(f'{pow(10.,logE_bins[plot_logE_min]):0.2f}-{pow(10.,logE_bins[plot_logE_max]):0.2f} TeV')
axbig.fill_between(on_radial_axis,np.array(baseline_yaxis)-np.array(on_profile_syst_axis),np.array(baseline_yaxis)+np.array(on_profile_syst_axis),alpha=0.2,color='b')
axbig.plot(on_radial_axis, baseline_yaxis, color='b', ls='dashed')
axbig.errorbar(on_radial_axis,on_profile_axis,on_profile_err_axis,color='k',marker='+',ls='none')
fig.savefig(f'output_plots/surface_brightness_{source_name}_allE_{all_roi_name[0]}_{plot_tag}.png',bbox_inches='tight')
axbig.remove()
txtfile = open(f'output_plots/txt_surface_brightness_{source_name}_allE_{all_roi_name[0]}_{plot_tag}.txt', 'w')
output_string = f"{pow(10.,logE_bins[plot_logE_min]):0.2f}-{pow(10.,logE_bins[plot_logE_max]):0.2f} TeV \n"
txtfile.write(output_string)
output_string = "angular distance [deg] \t surface brightness [TeV/cm2/s/sr] \t surface brightness error [TeV/cm2/s/sr] \n"
txtfile.write(output_string)
for entry in range(0,len(on_radial_axis)):
    radial_dist = on_radial_axis[entry]
    profile = on_profile_axis[entry]
    profile_err = on_profile_err_axis[entry]
    output_string = f"{radial_dist:0.2f} \t {profile:0.2e} \t {profile_err:0.2e} \n"
    txtfile.write(output_string)
txtfile.close()

on_radial_axis, on_profile_axis, on_profile_err_axis, on_profile_syst_axis = GetRadialProfile(sum_flux_sky_map_LE,sum_flux_err_sky_map_LE,sum_flux_syst_sky_map_LE,all_roi_x,all_roi_y,2.5,all_excl_x,all_excl_y,all_excl_r,radial_bin_scale=radial_bin_scale)
baseline_yaxis = [0. for i in range(0,len(on_radial_axis))]
fig.clf()
figsize_x = 7
figsize_y = 5
fig.set_figheight(figsize_y)
fig.set_figwidth(figsize_x)
axbig = fig.add_subplot()
axbig.tick_params(axis='both', which='major', labelsize=fig_fontsize*0.8)
label_x = 'Angular distance [deg]'
label_y = 'Surface brightness [$\\mathrm{TeV}\\ \\mathrm{cm}^{-2}\\mathrm{s}^{-1}\\mathrm{sr}^{-1}$]'
axbig.set_xlabel(label_x, fontsize=fig_fontsize)
axbig.set_ylabel(label_y, fontsize=fig_fontsize)
axbig.set_title(f'{pow(10.,logE_bins[plot_logE_min]):0.2f}-{pow(10.,logE_bins[plot_logE_mid]):0.2f} TeV')
axbig.fill_between(on_radial_axis,np.array(baseline_yaxis)-np.array(on_profile_syst_axis),np.array(baseline_yaxis)+np.array(on_profile_syst_axis),alpha=0.2,color='b')
axbig.plot(on_radial_axis, baseline_yaxis, color='b', ls='dashed')
axbig.errorbar(on_radial_axis,on_profile_axis,on_profile_err_axis,color='k',marker='+',ls='none')
fig.savefig(f'output_plots/surface_brightness_{source_name}_LE_{all_roi_name[0]}_{plot_tag}.png',bbox_inches='tight')
axbig.remove()
txtfile = open(f'output_plots/txt_surface_brightness_{source_name}_LE_{all_roi_name[0]}_{plot_tag}.txt', 'w')
output_string = f"{pow(10.,logE_bins[plot_logE_min]):0.2f}-{pow(10.,logE_bins[plot_logE_mid]):0.2f} TeV \n"
txtfile.write(output_string)
output_string = "angular distance [deg] \t surface brightness [TeV/cm2/s/sr] \t surface brightness error [TeV/cm2/s/sr] \n"
txtfile.write(output_string)
for entry in range(0,len(on_radial_axis)):
    radial_dist = on_radial_axis[entry]
    profile = on_profile_axis[entry]
    profile_err = on_profile_err_axis[entry]
    output_string = f"{radial_dist:0.2f} \t {profile:0.2e} \t {profile_err:0.2e} \n"
    txtfile.write(output_string)
txtfile.close()

on_radial_axis, on_profile_axis, on_profile_err_axis, on_profile_syst_axis = GetRadialProfile(sum_flux_sky_map_HE,sum_flux_err_sky_map_HE,sum_flux_syst_sky_map_HE,all_roi_x,all_roi_y,2.5,all_excl_x,all_excl_y,all_excl_r,radial_bin_scale=radial_bin_scale)
baseline_yaxis = [0. for i in range(0,len(on_radial_axis))]
fig.clf()
figsize_x = 7
figsize_y = 5
fig.set_figheight(figsize_y)
fig.set_figwidth(figsize_x)
axbig = fig.add_subplot()
axbig.tick_params(axis='both', which='major', labelsize=fig_fontsize*0.8)
label_x = 'Angular distance [deg]'
label_y = 'Surface brightness [$\\mathrm{TeV}\\ \\mathrm{cm}^{-2}\\mathrm{s}^{-1}\\mathrm{sr}^{-1}$]'
axbig.set_xlabel(label_x, fontsize=fig_fontsize)
axbig.set_ylabel(label_y, fontsize=fig_fontsize)
axbig.set_title(f'{pow(10.,logE_bins[plot_logE_mid]):0.2f}-{pow(10.,logE_bins[plot_logE_max]):0.2f} TeV')
axbig.fill_between(on_radial_axis,np.array(baseline_yaxis)-np.array(on_profile_syst_axis),np.array(baseline_yaxis)+np.array(on_profile_syst_axis),alpha=0.2,color='b')
axbig.plot(on_radial_axis, baseline_yaxis, color='b', ls='dashed')
axbig.errorbar(on_radial_axis,on_profile_axis,on_profile_err_axis,color='k',marker='+',ls='none')
fig.savefig(f'output_plots/surface_brightness_{source_name}_HE_{all_roi_name[0]}_{plot_tag}.png',bbox_inches='tight')
axbig.remove()
txtfile = open(f'output_plots/txt_surface_brightness_{source_name}_HE_{all_roi_name[0]}_{plot_tag}.txt', 'w')
output_string = f"{pow(10.,logE_bins[plot_logE_mid]):0.2f}-{pow(10.,logE_bins[plot_logE_max]):0.2f} TeV \n"
txtfile.write(output_string)
output_string = "angular distance [deg] \t surface brightness [TeV/cm2/s/sr] \t surface brightness error [TeV/cm2/s/sr] \n"
txtfile.write(output_string)
for entry in range(0,len(on_radial_axis)):
    radial_dist = on_radial_axis[entry]
    profile = on_profile_axis[entry]
    profile_err = on_profile_err_axis[entry]
    output_string = f"{radial_dist:0.2f} \t {profile:0.2e} \t {profile_err:0.2e} \n"
    txtfile.write(output_string)
txtfile.close()


if 'PSR_J1856_p0245' in source_name:

    on_radial_axis = [0.1, 0.3, 0.5, 0.7, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.1]
    on_profile_axis = [1.42630770e-09, 8.45610102e-10, 3.97927911e-10, 1.77387588e-10, 2.17602561e-10, 1.69687255e-10, 2.00294064e-11, -7.74294257e-11, 2.45221243e-11, -1.22693293e-11, -1.28535773e-11] #TeV/cm2/s/deg2
    on_profile_err_axis =[3.49403638e-10, 1.84587749e-10, 1.16395624e-10, 1.74538576e-10, 1.34151761e-10, 7.07628523e-11, 9.00952643e-11, 5.02971675e-11, 2.47404062e-11, 1.01558004e-11, 1.85267251e-13] #TeV/cm2/s/deg2
    profile_sum = np.sum(on_profile_axis)
    start = (profile_sum, 0.5)
    popt, pcov = curve_fit(diffusion_func,on_radial_axis,on_profile_axis,p0=start,sigma=on_profile_err_axis,absolute_sigma=True,bounds=((0, 0.01), (np.inf, np.inf)))
    profile_fit = diffusion_func(np.array(on_radial_axis), *popt)
    residual = np.array(on_profile_axis) - profile_fit
    chisq = np.sum((residual/np.array(on_profile_err_axis))**2)
    dof = len(on_radial_axis)-2
    print ('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print (f'Fermi data')
    print ('diffusion flux = %0.2E +/- %0.2E'%(popt[0],pow(pcov[0][0],0.5)))
    print ('diffusion radius = %0.2f +/- %0.2f deg (chi2/dof = %0.2f)'%(popt[1],pow(pcov[1][1],0.5),chisq/dof))

    baseline_yaxis = [0. for i in range(0,len(on_radial_axis))]
    fig.clf()
    figsize_x = 7
    figsize_y = 5
    fig.set_figheight(figsize_y)
    fig.set_figwidth(figsize_x)
    axbig = fig.add_subplot()
    label_x = 'angular distance [deg]'
    label_y = 'surface brightness [$\\mathrm{TeV}\\ \\mathrm{cm}^{-2}\\mathrm{s}^{-1}\\mathrm{sr}^{-1}$]'
    axbig.set_xlabel(label_x)
    axbig.set_ylabel(label_y)
    axbig.plot(on_radial_axis, baseline_yaxis, color='b', ls='dashed')
    axbig.errorbar(on_radial_axis,on_profile_axis,on_profile_err_axis,color='k',marker='+',ls='none',zorder=2)
    if fit_radial_profile:
        axbig.plot(on_radial_axis,diffusion_func(np.array(on_radial_axis),*popt),color='r')
    fig.savefig(f'output_plots/surface_brightness_{source_name}_Fermi_{plot_tag}.png',bbox_inches='tight')
    axbig.remove()

max_z = 3.

for logE in range(plot_logE_min,plot_logE_max):

    PlotSkyMap(fig,'Significance',logE,logE+1,sum_significance_sky_map[logE],f'significance_sky_map_{source_name}_logE{logE}_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,max_z=max_z,colormap='coolwarm',zoomin=zoomin)


font = {'family': 'serif', 'color':  'white', 'weight': 'normal', 'size': 10, 'rotation': 0.,}
for logE in range(plot_logE_min,plot_logE_max):
    fig.clf()
    figsize_y = 5
    figsize_x = 5
    fig.set_figheight(figsize_y)
    fig.set_figwidth(figsize_x)
    axbig = fig.add_subplot()
    axbig.set_xlabel('MSCL')
    axbig.set_ylabel('MSCW')
    xmin = sum_data_xyvar_map[logE].xaxis.min()*MSCL_cut[logE]
    xmax = sum_data_xyvar_map[logE].xaxis.max()*MSCL_cut[logE]
    ymin = sum_data_xyvar_map[logE].yaxis.min()*MSCW_cut[logE]
    ymax = sum_data_xyvar_map[logE].yaxis.max()*MSCW_cut[logE]
    im = axbig.imshow(sum_data_xyvar_map[logE].waxis[:,:,0].T,origin='lower',extent=(xmin,xmax,ymin,ymax),aspect='auto')
    lable_region = f'$\\gamma$-like SR'
    txt = axbig.text(-0.5, 0.4, lable_region, fontdict=font)
    lable_region = f'CR-1'
    txt = axbig.text(-0.5, 0.4+2.*MSCW_cut[logE], lable_region, fontdict=font)
    lable_region = f'CR-2'
    txt = axbig.text(-0.5, 0.4+4.*MSCW_cut[logE], lable_region, fontdict=font)
    lable_region = f'CR-3'
    txt = axbig.text(-0.5, 0.4+6.*MSCW_cut[logE], lable_region, fontdict=font)
    lable_region = f'CR-4'
    txt = axbig.text(-0.5+2.*MSCL_cut[logE], 0.4, lable_region, fontdict=font)
    lable_region = f'CR-5'
    txt = axbig.text(-0.5+2.*MSCL_cut[logE], 0.4+2.*MSCW_cut[logE], lable_region, fontdict=font)
    lable_region = f'CR-6'
    txt = axbig.text(-0.5+2.*MSCL_cut[logE], 0.4+4.*MSCW_cut[logE], lable_region, fontdict=font)
    lable_region = f'CR-7'
    txt = axbig.text(-0.5+2.*MSCL_cut[logE], 0.4+6.*MSCW_cut[logE], lable_region, fontdict=font)
    x_coord = np.array([1.,1.])*MSCL_cut[logE]
    y_coord = np.array([-1.,7.])*MSCW_cut[logE]
    axbig.plot(x_coord,y_coord,color='r',linestyle='solid',linewidth=1)
    x_coord = np.array([-1.,3.])*MSCL_cut[logE]
    y_coord = np.array([1.,1.])*MSCW_cut[logE]
    axbig.plot(x_coord,y_coord,color='r',linestyle='solid',linewidth=1)
    x_coord = np.array([-1.,3.])*MSCL_cut[logE]
    y_coord = np.array([3.,3.])*MSCW_cut[logE]
    axbig.plot(x_coord,y_coord,color='r',linestyle='solid',linewidth=1)
    x_coord = np.array([-1.,3.])*MSCL_cut[logE]
    y_coord = np.array([5.,5.])*MSCW_cut[logE]
    axbig.plot(x_coord,y_coord,color='r',linestyle='solid',linewidth=1)
    fig.savefig(f'output_plots/xyvar_map_inclusive_data_{source_name}_transpose_{plot_tag}_logE{logE}.png',bbox_inches='tight')
    axbig.remove()


fig.clf()
figsize_y = 2.*gcut_bins
figsize_x = 2.*(plot_logE_max-plot_logE_min)
fig.set_figheight(figsize_y)
fig.set_figwidth(figsize_x)
ax_idx = 0
gs = GridSpec(gcut_bins, (plot_logE_max-plot_logE_min), hspace=0.1, wspace=0.1)
for logE in range(plot_logE_min,plot_logE_max):
    for gcut in range(0,gcut_bins):
        ax_idx = logE-plot_logE_min + (plot_logE_max-plot_logE_min)*gcut + 1
        axbig = fig.add_subplot(gs[ax_idx-1])
        axbig.tick_params(axis='both', which='major', labelsize=fig_fontsize*0.8)
        if logE==plot_logE_min:
            if gcut==0:
                axbig.set_ylabel('SR', fontsize=fig_fontsize)
            else:
                axbig.set_ylabel(f'CR{gcut}', fontsize=fig_fontsize)
        if gcut==0:
            axbig.set_title(f'{pow(10.,logE_bins[logE]):0.2f}-{pow(10.,logE_bins[logE+1]):0.2f}\n TeV', fontsize=fig_fontsize)
        if not logE==plot_logE_min:
            axbig.axes.get_yaxis().set_visible(False)
        if not gcut==gcut_bins-1:
            axbig.axes.get_xaxis().set_visible(False)
        xmin = sum_data_xyoff_map[logE].xaxis.min()
        xmax = sum_data_xyoff_map[logE].xaxis.max()
        ymin = sum_data_xyoff_map[logE].yaxis.min()
        ymax = sum_data_xyoff_map[logE].yaxis.max()
        im = axbig.imshow(sum_data_xyoff_map[logE].waxis[:,:,gcut].T,origin='lower',extent=(xmin,xmax,ymin,ymax),aspect='auto')
fig.savefig(f'output_plots/xyoff_map_inclusive_data_{source_name}_transpose_{plot_tag}.png',bbox_inches='tight')
axbig.remove()


fig.clf()
figsize_y = 2.*gcut_bins
figsize_x = 2.*(plot_logE_max-plot_logE_min)
fig.set_figheight(figsize_y)
fig.set_figwidth(figsize_x)
ax_idx = 0
gs = GridSpec(gcut_bins, (plot_logE_max-plot_logE_min), hspace=0.1, wspace=0.1)
for logE in range(plot_logE_min,plot_logE_max):
    for gcut in range(0,gcut_bins):
        ax_idx = logE-plot_logE_min + (plot_logE_max-plot_logE_min)*gcut + 1
        axbig = fig.add_subplot(gs[ax_idx-1])
        axbig.tick_params(axis='both', which='major', labelsize=fig_fontsize*0.8)
        if logE==plot_logE_min:
            if gcut==0:
                axbig.set_ylabel('SR', fontsize=fig_fontsize)
            else:
                axbig.set_ylabel(f'CR{gcut}', fontsize=fig_fontsize)
        if gcut==0:
            axbig.set_title(f'{pow(10.,logE_bins[logE]):0.2f}-{pow(10.,logE_bins[logE+1]):0.2f}\n TeV', fontsize=fig_fontsize)
        if not logE==plot_logE_min:
            axbig.axes.get_yaxis().set_visible(False)
        if not gcut==gcut_bins-1:
            axbig.axes.get_xaxis().set_visible(False)
        xmin = sum_data_xyoff_map[logE].xaxis.min()
        xmax = sum_data_xyoff_map[logE].xaxis.max()
        ymin = sum_data_xyoff_map[logE].yaxis.min()
        ymax = sum_data_xyoff_map[logE].yaxis.max()
        im = axbig.imshow(sum_err_xyoff_map[logE].waxis[:,:,gcut].T,origin='lower',extent=(xmin,xmax,ymin,ymax),aspect='auto',vmin=-5.,vmax=5.,cmap='coolwarm')
ins_ax = fig.add_axes([0.905, 0.125, .010, 0.75])  # [lower left x, lower left y, width, height] w.r.t. fig
cb = fig.colorbar(im,cax=ins_ax)
fig.savefig(f'output_plots/xyoff_map_inclusive_err_{source_name}_transpose_{plot_tag}.png',bbox_inches='tight')
axbig.remove()


plot_camera_frame_power_spectrum(fig,f"{source_name}_LE_{plot_tag}",sum_significance_sky_map_LE,idx_z=0)
plot_camera_frame_power_spectrum(fig,f"{source_name}_HE_{plot_tag}",sum_significance_sky_map_HE,idx_z=0)

PlotSkyMap(fig,'Significance',plot_logE_min,plot_logE_max,sum_significance_sky_map_allE,f'significance_sky_map_{source_name}_allE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,max_z=max_z,colormap='custom',zoomin=zoomin)
PlotSkyMap(fig,'Excess count',plot_logE_min,plot_logE_max,sum_excess_sky_map_allE,f'excess_sky_map_{source_name}_allE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='coolwarm',zoomin=zoomin)
PlotSkyMap(fig,'Significance',plot_logE_min,plot_logE_mid,sum_significance_sky_map_LE,f'significance_sky_map_{source_name}_LE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,max_z=max_z,colormap='custom',zoomin=zoomin)
PlotSkyMap(fig,'Excess count',plot_logE_min,plot_logE_mid,sum_excess_sky_map_LE,f'excess_sky_map_{source_name}_LE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='coolwarm',zoomin=zoomin)
PlotSkyMap(fig,'Significance',plot_logE_mid,plot_logE_max,sum_significance_sky_map_HE,f'significance_sky_map_{source_name}_HE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,max_z=max_z,colormap='custom',zoomin=zoomin)
PlotSkyMap(fig,'Excess count',plot_logE_mid,plot_logE_max,sum_excess_sky_map_HE,f'excess_sky_map_{source_name}_HE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='coolwarm')
PlotSkyMap(fig,'Error count',plot_logE_min,plot_logE_max,sum_syst_sky_map_allE,f'excess_err_sky_map_{source_name}_allE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='coolwarm',zoomin=zoomin)
PlotSkyMap(fig,'Error count',plot_logE_min,plot_logE_mid,sum_syst_sky_map_LE,f'excess_err_sky_map_{source_name}_LE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='coolwarm',zoomin=zoomin)
PlotSkyMap(fig,'Error count',plot_logE_mid,plot_logE_max,sum_syst_sky_map_HE,f'excess_err_sky_map_{source_name}_HE_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,colormap='coolwarm',zoomin=zoomin)

for mimic in range(0,n_mimic):
    PlotSkyMap(fig,'Significance',plot_logE_min,plot_logE_max,sum_mimic_significance_sky_map_allE[mimic],f'significance_sky_map_{source_name}_allE_mimic{mimic}_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,excl_x=all_excl_x,excl_y=all_excl_y,excl_r=all_excl_r,max_z=max_z,colormap='custom',zoomin=zoomin)

print (f'total_exposure = {total_exposure}')
print (f'good_exposure = {good_exposure}')
print (f'mimic_exposure = {mimic_exposure}')

label_x = 'X [deg]'
label_y = 'Y [deg]'
if onoff=='ON':
    label_x = 'RA [deg]'
    label_y = 'Dec [deg]'
    if coordinate_type == 'galactic':
        label_x = 'Gal. l [deg]'
        label_y = 'Gal. b [deg]'
PlotCountProjection(fig,'Count',plot_logE_min,plot_logE_max,sum_data_sky_map_allE,sum_bkgd_sky_map_allE,label_x,label_y,f'projection_sky_map_{source_name}_allE_{plot_tag}',hist_map_syst=sum_syst_sky_map_allE,roi_x=all_excl_x,roi_y=all_excl_y,roi_r=all_excl_r,colormap='magma')
PlotCountProjection(fig,'Count',plot_logE_min,plot_logE_mid,sum_data_sky_map_LE,sum_bkgd_sky_map_LE,label_x,label_y,f'projection_sky_map_{source_name}_LE_{plot_tag}',hist_map_syst=sum_syst_sky_map_LE,roi_x=all_excl_x,roi_y=all_excl_y,roi_r=all_excl_r,colormap='magma')
PlotCountProjection(fig,'Count',plot_logE_mid,plot_logE_max,sum_data_sky_map_HE,sum_bkgd_sky_map_HE,label_x,label_y,f'projection_sky_map_{source_name}_HE_{plot_tag}',hist_map_syst=sum_syst_sky_map_HE,roi_x=all_excl_x,roi_y=all_excl_y,roi_r=all_excl_r,colormap='magma')

for mimic in range(0,n_mimic):
    PlotCountProjection(fig,'Count',plot_logE_min,plot_logE_max,sum_mimic_data_sky_map_allE[mimic],sum_mimic_bkgd_sky_map_allE[mimic],label_x,label_y,f'projection_sky_map_{source_name}_allE_mimic{mimic}_{plot_tag}',roi_x=all_excl_x,roi_y=all_excl_y,roi_r=all_excl_r,colormap='magma')
    PlotCountProjection(fig,'Count',plot_logE_min,plot_logE_mid,sum_mimic_data_sky_map_LE[mimic],sum_mimic_bkgd_sky_map_LE[mimic],label_x,label_y,f'projection_sky_map_{source_name}_LE_mimic{mimic}_{plot_tag}',roi_x=all_excl_x,roi_y=all_excl_y,roi_r=all_excl_r,colormap='magma')
    PlotCountProjection(fig,'Count',plot_logE_mid,plot_logE_max,sum_mimic_data_sky_map_HE[mimic],sum_mimic_bkgd_sky_map_HE[mimic],label_x,label_y,f'projection_sky_map_{source_name}_HE_mimic{mimic}_{plot_tag}',roi_x=all_excl_x,roi_y=all_excl_y,roi_r=all_excl_r,colormap='magma')


#if 'PSR_J2021_p4026' in source_name:
#    HI_sky_map = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
#    MWL_map_file = '/nevis/ged/data/rshang/MWL_maps/CGPS/CGPS_MO2_HI_line_image.fits' 
#    GetSlicedDataCubeMapCGPS(MWL_map_file, HI_sky_map, -3., 5.)
#    PlotSkyMap(fig,'Intensity',plot_logE_min,plot_logE_max,HI_sky_map,f'HI_sky_map_{source_name}_m03_p05_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,colormap='magma',zoomin=zoomin)
#    GetSlicedDataCubeMapCGPS(MWL_map_file, HI_sky_map, -27., -19.)
#    PlotSkyMap(fig,'Intensity',plot_logE_min,plot_logE_max,HI_sky_map,f'HI_sky_map_{source_name}_m27_m19_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,colormap='magma',zoomin=zoomin)
#    GetSlicedDataCubeMapCGPS(MWL_map_file, HI_sky_map, -19., -3.)
#    PlotSkyMap(fig,'Intensity',plot_logE_min,plot_logE_max,HI_sky_map,f'HI_sky_map_{source_name}_m19_m03_{plot_tag}',roi_x=all_roi_x,roi_y=all_roi_y,roi_r=all_roi_r,colormap='magma',zoomin=zoomin)

if 'PSR_J1856_p0245' in source_name:

    j1856_roi_x=[284.30, 284.37]
    j1856_roi_y=[2.72,   2.72]
    j1856_roi_r=[0.38,   0.24]
    
    HI_intensity_to_H_column_density = 1.8*1e18 / 1000.
    HI_sky_map = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    MWL_map_file = '/nevis/ged/data/rshang/MW_FITS/GALFA_HI_RA+DEC_284.00+02.35_N.fits' 
    GetSlicedDataCubeMapGALFA(MWL_map_file, HI_sky_map, 81.*1e3, 102.*1e3)
    HI_sky_map.scale(HI_intensity_to_H_column_density)
    PlotSkyMap(fig,'Column density [$1/\mathrm{cm}^{2}$]',plot_logE_min,plot_logE_max,HI_sky_map,f'Gas_HI_sky_map_{source_name}_p81_p102_{plot_tag}',roi_x=j1856_roi_x,roi_y=j1856_roi_y,roi_r=j1856_roi_r,colormap='magma',zoomin=zoomin)

    CO_intensity_to_H_column_density = 2.*1e20
    CO_sky_map = MyArray3D(x_bins=skymap_bins,start_x=xsky_start,end_x=xsky_end,y_bins=skymap_bins,start_y=ysky_start,end_y=ysky_end,z_bins=1,start_z=gcut_start,end_z=gcut_end)
    MWL_map_file = '/nevis/ged/data/rshang/MWL_maps/DHT08_Quad1_interp.fits' 
    GetSlicedDataCubeMap(MWL_map_file, CO_sky_map, 81., 102.)
    CO_sky_map.scale(CO_intensity_to_H_column_density)
    PlotSkyMap(fig,'Column density [$1/\mathrm{cm}^{2}$]',plot_logE_min,plot_logE_max,CO_sky_map,f'Gas_CO_sky_map_{source_name}_p81_p102_{plot_tag}',roi_x=j1856_roi_x,roi_y=j1856_roi_y,roi_r=j1856_roi_r,colormap='magma',zoomin=zoomin)



fig.clf()
figsize_x = 7
figsize_y = 7
fig.set_figheight(figsize_y)
fig.set_figwidth(figsize_x)
axbig = fig.add_subplot()
label_x = 'elevation'
label_y = 'azimuth'
axbig.set_xlabel(label_x)
axbig.set_ylabel(label_y)
for entry in range(0,len(list_run_elev)):
    axbig.scatter(list_run_elev[entry],list_run_azim[entry],color='b',alpha=0.5)
fig.savefig(f'output_plots/elevazim_{source_name}_{plot_tag}.png',bbox_inches='tight')
axbig.remove()

fig.clf()
figsize_x = 6.4
figsize_y = 4.8
fig.set_figheight(figsize_y)
fig.set_figwidth(figsize_x)
axbig = fig.add_subplot()
label_x = 'elevation [deg]'
label_y = 'number of runs'
axbig.set_xlabel(label_x)
axbig.set_ylabel(label_y)
axbig.hist(list_run_elev, bins=20, label=f"mean = {np.mean(list_run_elev):0.1f}, std dev = {np.std(list_run_elev):0.1f}")
axbig.legend(loc='best')
fig.savefig(f'output_plots/elev_{source_name}_{plot_tag}.png',bbox_inches='tight')
axbig.remove()

fig.clf()
figsize_x = 6.4
figsize_y = 4.8
fig.set_figheight(figsize_y)
fig.set_figwidth(figsize_x)
axbig = fig.add_subplot()
label_x = 'NSB'
label_y = 'number of runs'
axbig.set_xlabel(label_x)
axbig.set_ylabel(label_y)
axbig.hist(list_run_nsb, bins=20, label=f"mean = {np.mean(list_run_nsb):0.1f}, std dev = {np.std(list_run_nsb):0.1f}")
axbig.legend(loc='best')
fig.savefig(f'output_plots/nsb_{source_name}_{plot_tag}.png',bbox_inches='tight')
axbig.remove()


other_stars, other_star_type, other_star_coord = GetGammaSourceInfo() 
for star in range(0,len(other_stars)):
    if abs(src_ra-other_star_coord[star][0])>skymap_size: continue
    if abs(src_dec-other_star_coord[star][1])>skymap_size: continue
    print (f'Star {other_stars[star]} RA = {other_star_coord[star][0]:0.2f}, Dec = {other_star_coord[star][1]:0.2f}')

