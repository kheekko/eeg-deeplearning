import numpy as np
import time
import os
import sys
import bz2
import pickle

def get_all_files(dir):
    filelist = []

    for root, dirs, files in os.walk(dir):
        for file in files:
            if "reject_trials" not in file:
                filelist.append(os.path.join(root,file))

    return filelist


prelim_ME_db = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}
# prelim_MI_db = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

reject_ME_db = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[], 7:[]}

pwd = os.getcwd()
processed_data_dir = pwd + "/" + "processed_data"
filelist = get_all_files(processed_data_dir)

print("Processing %d files" % (len(filelist)))

t1 = time.time()
data = None
while len(filelist) > 0:
    seq_v_class_fname = filelist.pop()
    tmp = seq_v_class_fname.split('.')
    reject_trials_fname = tmp[0] + "_reject_trials." + tmp[1]
    with open(seq_v_class_fname, 'rb') as seq_v_class_file, open(reject_trials_fname, 'rb') as reject_trials_file:
        seq_v_class_data = pickle.load(seq_v_class_file)
        reject_trials_data = pickle.load(reject_trials_file)
        # f_name = os.path.basename(f.name)
        # db = None
        # if "ME" in f_name:
        #     db = prelim_ME_db
        # else:
        #     db = prelim_MI_db
        for key in seq_v_class_data.keys():
            prelim_ME_db[key].extend(seq_v_class_data[key])
            reject_ME_db[key].extend(reject_trials_data[key])
            
print("Complete loading and merging maps in %f s" % (time.time()-t1))

t1 = time.time()
with open("prelim_ME_db.pickle", "wb") as db, open("reject_ME_db.pickle", 'wb') as rt:
    i_str = pickle.dumps(prelim_ME_db)
    f_size = sys.getsizeof(i_str)/1048576
    print("Finished writing %.2f MB of data to prelim_ME_db.pickle in %f s" % (f_size, time.time()-t1))
    db.write(i_str)

    i_str = pickle.dumps(reject_ME_db)
    f_size = sys.getsizeof(i_str)/1048576
    print("Finished writing %.2f MB of data to reject_ME_db.pickle in %f s" % (f_size, time.time()-t1))
    rt.write(i_str)

# t1 = time.time()
# f = open("prelim_MI_db.pickle", "wb")
# i_str = pickle.dumps(prelim_MI_db)
# f_size = sys.getsizeof(i_str)/1048576
# f.write(i_str)
# f.close()
    
# print("Finished writing %.2f MB of data to prelim_MI_db.pickle in %f s" % (f_size, time.time()-t1))