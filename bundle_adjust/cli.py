import argparse
import os
import sys
import shutil

import numpy as np

import my_bundle_adjust
from my_bundle_adjust import ba_timeseries, loader


def main():

    parser = argparse.ArgumentParser(description="Bundle Adjustment for S2P")

    parser.add_argument(
        "config",
        metavar="config.json",
        help="path to a json file containing the configuration parameters of the scene to be bundle adjusted.",
    )

    parser.add_argument(
        "--timeline",
        action="store_true",
        help="just print the timeline of the scene described by config.json, do not run anything else.",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print stdout on command line instead of redirecting it to a log file",
    )

    # parse command line arguments
    args = parser.parse_args()

    if args.timeline:
        scene = ba_timeseries.Scene(args.config)
        timeline_indices = np.arange(len(scene.timeline), dtype=np.int32).tolist()
        scene.get_timeline_attributes(timeline_indices, ["datetime", "n_images", "id"])
        sys.exit()

    # load options from config file and copy config file to output_dir
    opt = loader.load_dict_from_json(args.config)
    os.makedirs(opt["output_dir"], exist_ok=True)
    try:
        shutil.copyfile(args.config, os.path.join(opt["output_dir"], os.path.basename(args.config)))
    except shutil.SameFileError:
        pass

    # redirect all prints to a bundle adjustment logfile inside the output directory
    if not args.verbose:
        path_to_log_file = "{}/bundle_adjust.log".format(opt["output_dir"], loader.get_id(args.config))
        print("Running bundle adjustment for RPC model refinement ...")
        print("Path to log file: {}".format(path_to_log_file))
        log_file = open(path_to_log_file, "w+")
        sys.stdout = log_file
        sys.stderr = log_file

    # load scene and run BA
    my_bundle_adjust.main(args.config)

    if not args.verbose:
        # close logfile
        sys.stderr = sys.__stderr__
        sys.stdout = sys.__stdout__
        log_file.close()
        print("... done !")
        print("Path to output files: {}".format(opt["output_dir"]))
