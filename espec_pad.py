import pyspedas as sp
import pytplot as tp
import numpy as np
import csv


def fpi(str_tr_espec):
    print(str_tr_espec)
    breakpoint()
    return 0


def bkgd(instr):
    with open('bkgd_' + instr + '.csv', "r", encoding='utf-8') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        egy = []
        flx = []
        for row in data:
            egy.append(float(row[0]))
            flx.append(float(row[1]))

    return (egy, flx)


def pad(tpv, str_tr_espec):
    # ------------------
    # Instrument type
    # ------------------
    instr = "fpi"
    if "_epd_" in tpv:
        instr = "epd"

    # ------------
    # Get Data
    # ------------
    if "_eis_" in tpv:
        a0 = tp.get_data(tpv + '_t0')
        a1 = tp.get_data(tpv + '_t1')
        a2 = tp.get_data(tpv + '_t2')
        a3 = tp.get_data(tpv + '_t3')
        a4 = tp.get_data(tpv + '_t4')
        a5 = tp.get_data(tpv + '_t5')
        wtime = a0[0]
        wegy = a0[2]
        wf_all = (a0[1] + a1[1] + a2[1] + a3[1] + a4[1] + a5[1]) / 6.0
    else:
        alldata = tp.get_data(tpv)
        attr = tp.get_data(tpv, metadata=True)
        wtime = alldata[0]  # time data [seconds from 1970]
        wegy = alldata[2]  # eV if FPI, keV if FEEPS/EIS
        wf_all = alldata[1]  # particle flux [1/cm2 s sr keV]

    nmax = wf_all.shape[0]  # Number of time steps
    imax = wf_all.shape[1]  # Number of energy steps

    # ---------------------------------------
    # Average over the specified time range
    # ---------------------------------------

    # prep output
    wf = np.empty(imax)
    we = np.empty(imax)

    # find the indices that fall within the specified time range
    tr_espec = sp.time_double(str_tr_espec)
    idx = np.where((tr_espec[0] <= wtime) & (wtime <= tr_espec[1]))
    ns = np.nanmin(idx)
    ne = np.nanmax(idx)
    ct = ne - ns + 1  # Number of time steps in the specified time range

    # loop through the data array
    if instr == 'fpi':  # __________________ FPI
        for n in range(ns, ne):  # For each time step
            for i in range(0, imax):  # For each energy step
                E = wegy[n, i] * 0.001  # eV --> keV
                wf[i] += wf_all[n, i] / E  # energy flux --> particle flux
        wf /= ct  # To make it an average.
        we = wegy[0, 0:imax]  # keep the unit eV

    else:  # ______________________________ FEEPS and EIS
        for n in range(ns, ne):
            for i in range(0, imax):
                wf[i] += wf_all[n, i]  # no need for conversion
        wf /= ct
        we = wegy * 1000  # keV --> eV

    return (we, wf)
