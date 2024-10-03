import numpy as np
import pyspedas as sp
import pytplot as tp
import matplotlib.pyplot as plt
import espec_pad as espec

# ========== TIME RANGE FOR THE ENERGY SPECTRUM (espec) ==============
# This period should be larger than 20s when EIS is used

str_tr_espec = ['2017-10-25/08:38:35','2015-10-25/08:38:55']
# Time range for loading data. Should be larger than str_tr_espec
trange = ['2015-10-25/08:38:35','2015-10-25/08:38:55']
# =====================================================================

# ------------
# DATA RATE
# ------------
rate = 'fast'  # data rate for FPI (either 'fast' or 'brst')
if rate == 'brst':
    brate = 'brst'
else:
    brate = 'srvy'

# ------------
# LOAD
# ------------
mms_fpi = sp.mms.fpi(trange=trange, data_rate=rate, datatype='dis-moms')
#mms_feeps = sp.mms.feeps(trange=trange, data_rate=brate, datatype='ion')
mms_extof = sp.mms.eis(trange=trange, data_rate=brate, datatype='extof', varformat='*proton*flux*_')
mms_phxtof = sp.mms.eis(trange=trange, data_rate=brate, datatype='phxtof', varformat='*proton*_flux*')

# ------------
# Cut
# ------------

tp_fpi = 'mms1_dis_energyspectr_omni_' + rate
#tp_feeps = 'mms1_epd_feeps_' + brate + '_l2_electron_intensity_omni'

#tp_extof = 'mms1_epd_eis_extof_proton_P3_flux'
#tp_phxtof = 'mms1_epd_eis_phxtof_proton_P3_flux'

tp_extof = 'mms1_epd_eis_' +brate+ '_l2_extof_proton_P3_flux'
tp_phxtof = 'mms1_epd_eis_' +brate+ '_l2_phxtof_proton_P3_flux'


pad_fpi = espec.pad(tp_fpi, str_tr_espec)
#pad_feeps = espec.pad(tp_feeps, str_tr_espec)
pad_extof = espec.pad(tp_extof, str_tr_espec)
pad_phxtof = espec.pad(tp_phxtof, str_tr_espec)

#bkgd_feeps = espec.bkgd('feeps')
bkgd_eis = espec.bkgd('eis')
bkgd_hpca = espec.bkgd('hpca')

# ------------
# Plot
# ------------
fig, ax = plt.subplots()
ax.plot(pad_fpi[0], pad_fpi[1], color='navy')
#ax.plot(pad_feeps[0], pad_feeps[1], color='orange')
ax.plot(pad_extof[0], pad_extof[1], color='red')
ax.plot(pad_phxtof[0], pad_phxtof[1], color='green')
#ax.plot(bkgd_feeps[0], bkgd_feeps[1], 'b--')
ax.plot(bkgd_eis[0], bkgd_eis[1], 'k--')
# ax.plot(bkgd_hpca[0],  bkgd_hpca[1],  'r--')

plt.legend(['FPI', 'EIS [ExTOF]', 'EIS [PHxTOF]', 'Typical lobe spectrum (EIS)'], loc ="lower left")

#plt.title('Ion Energy Spectrum \n \n 2015-11-04 / 04:58:05 - 04:58:25 \n Shock Angle: 83.9371 @ Mach number 10.9859')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim([1e+1, 1e+6])
ax.set_ylim([1e-5, 1e+9])
ax.set_xlabel('eV')
ax.set_ylabel('1/cm$^2$ s sr keV')
fig.set_size_inches(6,10)

plt.show()
#plt.savefig('espec_' + rate + '.png', dpi=300)
plt.close(fig)
