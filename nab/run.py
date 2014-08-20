#!/usr/bin/env python
# ----------------------------------------------------------------------
# Copyright (C) 2014, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------

import os
import yaml
import argparse

from nab.lib.running import Runner
from nab.lib.util import recur, detectorNameToClass

from nab.detectors.numenta.numenta_detector import NumentaDetector
from nab.detectors.skyline.skyline_detector import SkylineDetector


depth = 2

root = recur(os.path.dirname, os.path.realpath(__file__), depth)

def main(args):
  constructors = getDetectorClassConstructors(args.config)
  runner = Runner(root, args, constructors)

  if args.detectOnly:
    runner.detect()

  elif args.scoreOnly:
    runner.score()

  else:
    runner.detect()
    runner.score()


def getDetectorClassConstructors(relativeConfigPath):
  f = open(os.path.join(root, relativeConfigPath))

  config = yaml.load(f)

  detectorClassNames = [detectorNameToClass(detector) for detector in config["AnomalyDetectors"]]

  detectorConstructors = [globals()[className] for className in detectorClassNames]

  return detectorConstructors

if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  parser.add_argument("--detectOnly",
                    help="Generate detector results but do not analyze results \
                    files.",
                    default=False,
                    action="store_true")

  parser.add_argument("--scoreOnly",
                    help="Analyze results in the results directory",
                    default=False,
                    action="store_true")


  parser.add_argument("--dataDir",
                    default="data",
                    help="This holds all the label windows for the corpus.")

  parser.add_argument("--labelDir",
                    default="labels",
                    help="This holds all the label windows for the corpus.")


  parser.add_argument("-c", "--config",
                    default="config/benchmark_config.yaml",
                    help="The configuration file to use while running the "
                    "benchmark.")

  parser.add_argument("-p", "--profiles",
                    default="config/user_profiles.yaml",
                    help="The configuration file to use while running the "
                    "benchmark.")

  parser.add_argument("-n", "--numCPUs",
                    default=None,
                    help="The number of CPUs to use to run the "
                    "benchmark. If not specified all CPUs will be used.")

  args = parser.parse_args()

  main(args)
