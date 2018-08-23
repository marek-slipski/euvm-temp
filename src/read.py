import os
import yaml
import pandas as pd
import scipy.io as spi

def configinfo(configpath):
    # Open config file to get path to data
    with open(configpath,'r') as cf:
        return yaml.load(cf)
    
def euvT_vrdir(euvdir,vers,rev):
    # convert to full path based on version and revision numbers
    data_path = os.path.expanduser(euvdir)
    vrdif = 'euvm_temperatures_v'+str(vers).zfill(2)+'r'+str(rev).zfill(2)+'/'
    return os.path.join(data_path,vrdif)
    

def orbIO(fullfilepath):
    # take orb number from file
    filename = os.path.basename(fullfilepath)
    orbio = filename.split('_')[1]
    if 'in' in orbio:
        inout = 'i'
        orbno = int(orbio.split('i')[0])
    elif 'out' in orbio:
        inout = 'o'
        orbno = int(orbio.split('o')[0])
    else:
        inout = np.nan
        orbno = np.nan
    return orbno, inout
    
def sav2df(sav,orbno,inout):
    # Make DataFrame
    tdf_init = pd.DataFrame(sav['temp'],columns=['alt_temp','temp']) #init
    tdf_init['pressure'] = sav['pressure'] # Add columns
    tdf_init['lat'] = sav['location_info'][0][1]
    tdf_init['lon'] = sav['location_info'][0][2]
    tdf_init['lst'] = sav['location_info'][0][3]
    den_df = pd.DataFrame(sav['density'],columns=['alt_den','density'])
    df = pd.concat([tdf_init,den_df],axis=1) # Full DataFrame
    df['orbit'] = [orbno]*len(df)
    df['inout'] = [inout]*len(df)
    return df

if __name__=='__main__':
    config = configinfo('config_local.yaml')
    data_path_vr = euvT_vrdir(config['data_path'],1,0)
    filename = 'temp_888out_v01r00.sav'

    # Orbit number and Inbound or outbound
    orb,io = orbIO(data_path_vr+filename)

    # read in savfile
    savobj = spi.readsav(data_path_vr+filename)


    newdf = sav2df(savobj,orb,io)

    print newdf.head()
