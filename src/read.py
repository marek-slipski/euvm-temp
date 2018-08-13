import os
import yaml
import pandas as pd
import scipy.io as spi

# Open config file to get path to data
with open('config_local.yaml','r') as cf:
    config = yaml.load(cf)
    
# convert to full path based on version and revision numbers
data_path = os.path.expanduser(config['data_path'])
vers = '01'
rev = '00'
vrdif = 'euvm_temperatures_v'+vers+'r'+rev+'/'
data_path_vr = os.path.join(data_path,vrdif)

# Open IDL savefile
sav = spi.readsav(data_path_vr+'temp_888out_v01r00.sav')

# Make DataFrame
tdf_init = pd.DataFrame(sav['temp'],columns=['alt_temp','temp']) #init
tdf_init['pressure'] = sav['pressure'] # Add columns
tdf_init['lat'] = sav['location_info'][0][1]
tdf_init['lon'] = sav['location_info'][0][2]
tdf_init['lst'] = sav['location_info'][0][3]
den_df = pd.DataFrame(sav['density'],columns=['alt_den','density'])
df = pd.concat([tdf_init,den_df],axis=1) # Full DataFrame

print df.head()
print df.tail()