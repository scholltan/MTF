import os
import sys
import cv2
import numpy as np
import math
import time
import pyMTF2
from utilities import drawRegion
from matplotlib import pyplot as plt

if __name__ == '__main__':
    # script parameters
    show_tracking_output = 1

    # MTF parameters
    config_dir = '../../Config'
    db_root_path = '../../../Datasets'
    pipeline = 'c'
    img_source = 'u'
    actor_id = 1
    seq_id = 16
    seq_fmt = 'jpg'
    init_frame_id = 1
    py_visualize = 1
    n_trackers = 1

    param_str = 'db_root_path {:s}'.format(db_root_path)
    param_str = '{:s} pipeline {:s}'.format(param_str, pipeline)
    param_str = '{:s} img_source {:s}'.format(param_str, img_source)
    param_str = '{:s} actor_id {:d}'.format(param_str, actor_id)
    param_str = '{:s} seq_id {:d}'.format(param_str, seq_id)
    param_str = '{:s} seq_fmt {:s}'.format(param_str, seq_fmt)
    param_str = '{:s} init_frame_id {:d}'.format(param_str, init_frame_id)
    param_str = '{:s} py_visualize {:d}'.format(param_str, py_visualize)
    param_str = '{:s} n_trackers {:d}'.format(param_str, n_trackers)

    nargin = len(sys.argv) - 1
    if nargin % 2 != 0:
        raise IOError('Optional arguments must be specified in pairs')
    # parse optional arguments
    arg_id = 1
    while arg_id <= nargin:
        arg_name = sys.argv[arg_id]
        arg_val = sys.argv[arg_id + 1]
        if arg_name == 'config_dir':
            config_dir = arg_val
        elif arg_name == 'show_tracking_output':
            show_tracking_output = int(arg_val)
        else:
            param_str = '{:s} {:s} {:s}'.format(param_str, arg_name, arg_val)
        if arg_name == 'n_trackers':
            n_trackers = int(arg_val)
        arg_id += 2
    param_str = 'config_dir {:s} {:s}'.format(config_dir, param_str)

    print('param_str: ', param_str)

    # thickness of the bounding box lines drawn on the image
    thickness = 2
    # tracker location drawn in red
    result_colors = ('red', 'green', 'blue',  'cyan', 'orange_red', 'yellow', 'magenta',
                     'purple', 'orange', 'white', 'black')

    n_cols = len(result_colors)

    # initialize input pipeline
    if not pyMTF2.init(param_str):
        raise SystemError('MTF input pipeline creation was unsuccessful')
    else:
        print('MTF input pipeline created successfully')

    if n_trackers > 1:
        tracker_ids = pyMTF2.createTrackers(param_str)
        if tracker_ids is None:
            raise SystemError('Tracker creation was unsuccessful')
        print('Created {} trackers with tracker_ids: {} '.format(n_trackers, tracker_ids))
    else:
        tracker_ids = []
        tracker_id = pyMTF2.createTracker(param_str)
        if not tracker_id:
            raise SystemError('Tracker creation was unsuccessful')
        print('Tracker created successfully')
        tracker_ids.append(tracker_id)

    if show_tracking_output:
        # plt.ion()
        # plt.show()

        # window for displaying the tracking result
        window_name = 'Tracking Result'
        cv2.namedWindow(window_name)

    tracker_ids = list(tracker_ids)

    while True:
        # print('getting frame')
        src_img = pyMTF2.getFrame()
        if src_img is None:
            print('Frame extraction was unsuccessful')
            break

        # src_img = np.asarray(src_img)
        # print('got frame {}/{}'.format(src_img.shape, src_img.dtype))
        stopped_ids = []
        for i in range(n_trackers):
            curr_corners = pyMTF2.getRegion(tracker_ids[i])
            if curr_corners is None:
                print('Tracker {} update was unsuccessful'.format(i + 1))
                pyMTF2.removeTracker(tracker_ids[i])
                stopped_ids.append(i)
                continue
            # print('curr_corners: ', curr_corners)
            if show_tracking_output:
                col = result_colors[i % n_cols]
                drawRegion(src_img, curr_corners, col, thickness, '{}'.format(tracker_ids[i]))

        for i in stopped_ids:
            del tracker_ids[i]
            n_trackers -= 1

        if not tracker_ids:
            break

        if show_tracking_output:
            # plt.imshow(src_img)
            # plt.draw()
            # plt.pause(0.00001)

            cv2.imshow(window_name, src_img)
            if cv2.waitKey(1) == 27:
                break

    pyMTF2.removeTrackers()
    pyMTF2.quit()
