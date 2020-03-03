# -*- coding: utf-8 -*-
#############################################################################
#          __________                                                       #
#   __  __/ ____/ __ \__ __   This file is part of MicroGP4 v1.0a1 "Kiwi"   #
#  / / / / / __/ /_/ / // /   (!) by Giovanni Squillero and Alberto Tonda   #
# / /_/ / /_/ / ____/ // /_   https://github.com/squillero/microgp4         #
# \__  /\____/_/   /__  __/                                                 #
#   /_/ --MicroGP4-- /_/      "You don't need a big goal, be μ-ambitious!!" #
#                                                                           #
#############################################################################

# Copyright 2019 Giovanni Squillero and Alberto Tonda
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.

"""Logging facility for MicroGPv4, as colorful as possible

Usage example:

    `logging.DefaultLogger.setLevel(level=logging.INFO)`

    `logging.debug("This is a 'debug' message")`

    `logging.bare("This is a 'verbose' message (somewhat between info and debug)")`

    `logging.info("This is a 'info' message")`

    `logging.bare("This is a 'bare' message (like info, but without level name)")`

    `logging.warning ("This is a 'warning' message")`

    `logging.error("This is a 'error' message")`

    `logging.critical("This is a 'critical' message")`
"""

import logging
import os
import warnings

microgp4_process = None
try:
    import psutil
    microgp4_process = psutil.Process(os.getpid())
except:
    pass

DefaultLogger = logging.getLogger('microgp4')

# Propagate Log levels, and add a few ones
SPAM = logging.DEBUG - 1
DEBUG = logging.DEBUG
VERBOSE = logging.INFO - 1
INFO = logging.INFO
BARE = logging.INFO + 1
CRITICAL = logging.CRITICAL
WARNING = logging.WARNING
ERROR = logging.ERROR

# Setup DefaultLogger's handler
DefaultLogger.handler = []
DefaultLogger.setLevel(logging.INFO)
DefaultLogger.__doc__ = "Default MicroGP4 logger"


def cpu_info(msg: str, log_level: int = DEBUG) -> None:
    if msg:
        DefaultLogger.log(log_level, "%s: %s", msg, microgp4_process.cpu_times())
    else:
        DefaultLogger.log(log_level, "%s", msg, microgp4_process.cpu_times())


def log_split(level: int, msg: str) -> None:
    for line in msg.split("\n"):
        DefaultLogger.log(level, line)


DefaultLogger.cpu_info = cpu_info
DefaultLogger.log_split = log_split

# Log SPAM, VERBOSE & BARE
DefaultLogger.spam = lambda *args, **kwargs: DefaultLogger.log(SPAM, *args, **kwargs)
DefaultLogger.verbose = lambda *args, **kwargs: DefaultLogger.log(VERBOSE, *args, **kwargs)
DefaultLogger.bare = lambda *args, **kwargs: DefaultLogger.log(BARE, *args, **kwargs)

# shortcuts
spam = DefaultLogger.spam
debug = DefaultLogger.debug
verbose = DefaultLogger.verbose
info = DefaultLogger.info
warning = DefaultLogger.warning
error = DefaultLogger.error
critical = DefaultLogger.critical
bare = DefaultLogger.bare

try:
    import coloredlogs

    logging.addLevelName(SPAM, ' SPAM')
    logging.addLevelName(DEBUG, ' DEBUG')
    logging.addLevelName(VERBOSE, ' VERBOSE')
    logging.addLevelName(INFO, ' INFO')
    logging.addLevelName(BARE, '')
    logging.addLevelName(WARNING, ' WARNING')
    logging.addLevelName(ERROR, ' ERROR')
    logging.addLevelName(CRITICAL, ' CRITICAL')
    coloredlogs.install(level='DEBUG',
                        logger=DefaultLogger,
                        fmt="%(asctime)s%(levelname)s %(message)s",
                        datefmt="%H:%M:%S",
                        field_styles={
                            'asctime':   {
                                'color': 'cyan'
                            },
                            'levelname': {
                                'color':  'blue',
                                'bold':   False,
                                'bright': True
                            }
                        },
                        level_styles={
                            logging.getLevelName(ERROR):    {
                                'color': 'red',
                                'bold':  True
                            },
                            logging.getLevelName(CRITICAL): {
                                'color': 'red',
                                'bold':  True
                            },
                            logging.getLevelName(WARNING):  {
                                'color': 'yellow',
                                'bold':  True
                            },
                            logging.getLevelName(DEBUG):    {
                                'color':  'black',
                                'bright': True
                            },
                            logging.getLevelName(SPAM):     {
                                'color':  'black',
                                'bright': True
                            }
                        })
except:
    WARN_NOCOLOR = "Colored log not available (install module 'coloredlogs')."
    warnings.warn(WARN_NOCOLOR, RuntimeWarning)
    logging.addLevelName(SPAM, ' [SPAM]')
    logging.addLevelName(DEBUG, ' [DEBUG]')
    logging.addLevelName(VERBOSE, ' [VERBOSE]')
    logging.addLevelName(INFO, ' [INFO]')
    logging.addLevelName(BARE, '')
    logging.addLevelName(WARNING, ' [WARNING]')
    logging.addLevelName(ERROR, ' [ERROR]')
    logging.addLevelName(CRITICAL, ' [CRITICAL]')
    logging.basicConfig(level='DEBUG', format="%(asctime)s%(levelname)s %(message)s", datefmt="%H:%M:%S")