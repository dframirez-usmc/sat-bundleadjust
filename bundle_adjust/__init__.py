import sys

import numpy as np

from my_bundle_adjust import ba_timeseries, loader

__version__ = "my_0.1.0"


def main(config_path):

    # load scene and run BA
    scene = ba_timeseries.Scene(config_path)
    scene.run_bundle_adjustment_for_RPC_refinement()
