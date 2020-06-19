import matplotlib
import matplotlib.pyplot as plt
import numpy as np
#from pylab import *
import matplotlib.colors as colors
import re
from astropy import constants as const


def KepMass(axprofile,rrs,cosi,bmaj,v_Phi_prof,sv_Phi_prof,distance,a_min,a_max,linecolor='grey'):

    # ----------------------------------------------------------------------
    # optimal mass
    # ----------------------------------------------------------------------
    
    ##print( "bmaj = ",bmaj,"\n";)
    #Nind=2.*np.pi*rrs * cosi  /(bmaj) #cosi
    ##print( "Nind=",Nind)
    ##print( "sqrt(Nind)=",np.sqrt(Nind))
    #
    #dispv_Phi_prof=sv_Phi_prof.copy()
    #sv_Phi_prof_mean=dispv_Phi_prof/np.sqrt(Nind)
    ##sv_Phi_prof=dispv_Phi_prof#/np.sqrt(Nind)
    #
    yr = 31558149.8
    RRs=rrs*distance*const.au.value

    nmesh=10
    rbins=np.arange(nmesh)*(a_max-a_min)/float(nmesh)+a_min
    Ms=np.zeros(nmesh)
    dr=rbins[1]-rbins[0]

    
    for irrs in np.arange(nmesh):
        #mask= ((rrs > 0.4) & (rrs < 0.6))
        mask= ((rrs > rbins[irrs]) & (rrs < rbins[irrs]+dr))
        
        # mask= ((rrs > 0.4) & (rrs < 0.8))
        v0=v_Phi_prof[np.where(mask)]
        #sv0=sv_Phi_prof_mean[np.where(mask)]
        sv0=sv_Phi_prof[np.where(mask)]

        print ("v0 ",v0)
        print ("sv0 ",sv0)
        
        subRRs=RRs[np.where(mask)]
        
        Mstar_num =  (np.sum( v0 / (sv0**2 * np.sqrt(subRRs))))**2
        Mstar_denom = (np.sum(np.sqrt(1.-cosi**2)*1E-3*np.sqrt( const.G.value  * const.M_sun.value) / subRRs / sv0**2))**2
        Mstar = Mstar_num / Mstar_denom
        Ms[irrs] = Mstar
        print( "rrs ",rbins[irrs]," iMstar = ",Mstar, "Mstar_num ", Mstar_num,"Mstar_denom", Mstar_denom )
        
        #Mstar = float("%.2f" % Mstar)
        

    #mask= ((rrs > 0.4) & (rrs < 0.6))
    mask= ((rrs > a_min) & (rrs < a_max))
    #mask= ((rrs > rbins[irrs]) & (rrs < rbins[irrs]+dr))
    
    # mask= ((rrs > 0.4) & (rrs < 0.8))
    v0=v_Phi_prof[np.where(mask)]
    sv0=sv_Phi_prof[np.where(mask)]
    subRRs=RRs[np.where(mask)]
    
    Mstar_num =  (np.sum( v0 / (sv0**2 * np.sqrt(subRRs))))**2
    Mstar_denom = (np.sum(np.sqrt(1.-cosi**2)*1E-3*np.sqrt( const.G.value  * const.M_sun.value) / subRRs / sv0**2))**2
    Mstar = Mstar_num / Mstar_denom
    sMstar = (1./Mstar_denom) * np.sqrt( np.sum( 1./(sv0**2 * subRRs)))
    print( "Mstar = ",Mstar,"+-",sMstar,"Msun")
    
    print( "radial Mstar scatter: ",np.std(Ms),"Msun")

        
    vstar = np.sqrt(1.-cosi**2)*1E-3*np.sqrt( const.G.value  * Mstar * const.M_sun.value / RRs )
    vstar[0]=0.

    plotmask = np.where( (rrs >= a_min) & (rrs <= a_max) )

    axprofile.plot(rrs[plotmask],vstar[plotmask]*np.sqrt(rrs[plotmask])/np.sqrt(a_max),color=linecolor,linewidth=2.0,alpha=1.0,linestyle='dashed',label=str("%.2f" % Mstar)+r'$\,M_\odot$')

    return
