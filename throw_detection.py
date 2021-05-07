import numpy as np
import math
from pdb import set_trace

FILENAME = 'Accelerometer'

print(f'Loading data from file "{FILENAME}"...')
def pull_data(dir_name, file_name):
    f = open(dir_name + '/' + file_name + '.csv')
    xs = []
    ys = []
    zs = []
    rs = []
    timestamps = []
    for line in f:
        value = line.split(',')
        if len(value) > 3:
            timestamps.append(float(value[1]))
            x = float(value[2])
            y = float(value[3])
            z = float(value[4])
            r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
            xs.append(x)
            ys.append(y)
            zs.append(z)
            rs.append(r)
    
    f.close()
    return np.array(xs), np.array(ys), np.array(zs), np.array(rs), np.array(timestamps)

x, y, z, signal, timestamps = pull_data('.', 'Accelerometer')

def throw_detection(window):
    '''
    detects if the data in window represents "in flight" values.
    @param  window   instantaneous matrix of the values at a given point in time (i.e. window represents ~0.1 seconds of data)
    @return True if data represents that the phone is in flight, False otherwise
    '''

    # observationally, we have observed that it is usually a safe bet to assume that
    # a magnitude of over ~8.0 m/s2 usually indicates free-fall or the phone
    # undergoing some accelerated throw event.

    MAG_ACCEL_CONSTANT = 8.0 # m/s^2
    win_len = len(window)

    # Now, we take the average of all values in the window.
    # (It is assumed that this data is somewhat smooth.)
    avg = np.average(window)
    
    # now, we return whether or not the average acceleration is greater than
    # or less than the constant
    return True if avg > MAG_ACCEL_CONSTANT else False


IN_MOTION_RANGES = ((9, 11), (22, 25), (28, 30)) # approx. ranges of when it's in flight of dummy data

FPOS = 0
FNEG = 0
TPOS = 0
TNEG = 0
WINDOW_LEN = 5

print('Analyzing data...')
for s, t in ((signal[i:i + WINDOW_LEN], timestamps[i]) for i in range(0,len(signal), WINDOW_LEN)):
    predicted_value = throw_detection(s)
    ground_truth = any(r[0] < t < r[1] for r in IN_MOTION_RANGES)
    if predicted_value and ground_truth:
        TPOS += 1
    if predicted_value and not ground_truth:
        FPOS += 1
    if not predicted_value and ground_truth:
        FNEG += 1
    if not predicted_value and not ground_truth:
        TNEG += 1

#set_trace()
print('Evaluating performance...')
TOTAL = TPOS + TNEG + FPOS + FNEG
PRECISION = 0 if TPOS + FPOS == 0 else float(TPOS / (TPOS + FPOS))
RECALL = 0 if TPOS + FNEG == 0 else float(TPOS / (TPOS + FNEG))
ACCURACY = float((TPOS + TNEG) / TOTAL)
# print out all statistics
print('Evaluation done! Statistics of detection performance:')
print(f'Accuracy is {ACCURACY}')
print(f'Precision is {PRECISION}')
print(f'Recall is {RECALL}')
print('Program terminating...')
