import numpy as np
import json
from sklearn.preprocessing import RobustScaler

# --- your canonical features (copied from preprocessing code) ---
main_feature = [
    'destinationport', 'flowduration', 'totalfwdpackets',
    'totalbackwardpackets', 'totallengthoffwdpackets',
    'totallengthofbwdpackets', 'fwdpacketlengthmax',
    'fwdpacketlengthmin', 'fwdpacketlengthmean',
    'fwdpacketlengthstd', 'bwdpacketlengthmax',
    'bwdpacketlengthmin', 'bwdpacketlengthmean',
    'bwdpacketlengthstd', 'flowbytess', 'flowpacketss',
    'flowiatmean', 'flowiatstd', 'flowiatmax', 'flowiatmin',
    'fwdiattotal', 'fwdiatmean', 'fwdiatstd', 'fwdiatmax',
    'fwdiatmin', 'bwdiattotal', 'bwdiatmean', 'bwdiatstd',
    'bwdiatmax', 'bwdiatmin', 'fwdpshflags', 'bwdpshflags',
    'fwdurgflags', 'bwdurgflags', 'fwdheaderlength',
    'bwdheaderlength', 'fwdpacketss', 'bwdpacketss',
    'minpacketlength', 'maxpacketlength', 'packetlengthmean',
    'packetlengthstd', 'packetlengthvariance', 'finflagcount',
    'synflagcount', 'rstflagcount', 'pshflagcount',
    'ackflagcount', 'urgflagcount', 'cweflagcount',
    'eceflagcount', 'downupratio', 'averagepacketsize',
    'avgfwdsegmentsize', 'avgbwdsegmentsize', 'fwdavgbytesbulk',
    'fwdavgpacketsbulk', 'fwdavgbulkrate', 'bwdavgbytesbulk',
    'bwdavgpacketsbulk', 'bwdavgbulkrate', 'subflowfwdpackets',
    'subflowfwdbytes', 'subflowbwdpackets', 'subflowbwdbytes',
    'initwinbytesforward', 'initwinbytesbackward',
    'actdatapktfwd', 'minsegsizemin', 'activemean',
    'activestd', 'activemax', 'activemin', 'idlemean', 'idlestd',
    'idlemax', 'idlemin', 'l7protocol'
]



# --- Step 1: create dummy row (replace with CSV row if you want) ---
vector = np.arange(len(main_feature)).astype(float).reshape(1, -1)

# --- Step 2: scale with RobustScaler ---
scaler = RobustScaler()
scaled_vector = scaler.fit_transform(vector)

print("Scaled vector shape:", scaled_vector.shape)

# --- Step 3: save request.json for TF Serving ---
request_data = {"instances": scaled_vector.tolist()}
with open("./request.json", "w") as f:
    json.dump(request_data, f)

print("Saved request.json, ready to send to TF Serving")
