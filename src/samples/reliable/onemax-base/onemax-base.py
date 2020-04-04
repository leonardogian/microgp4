# -*- coding: utf-8
#############################################################################
#          __________                                                       #
#   __  __/ ____/ __ \__ __   This file is part of MicroGP4 v1.0 "Kiwi"     #
#  / / / / / __/ /_/ / // /   (!) by Giovanni Squillero and Alberto Tonda   #
# / /_/ / /_/ / ____/ // /_   https://github.com/squillero/microgp4         #
# \__  /\____/_/   /__  __/                                                 #
#   /_/ --MicroGP4-- /_/      "You don't need a big goal, be μ-ambitious!!" #
#                                                                           #
#############################################################################

# Copyright 2020 Giovanni Squillero and Alberto Tonda
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
import argparse
import sys

import microgp as ugp4
from microgp.utils import logging

if __name__ == "__main__":
    ugp4.show_banner()
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase log verbosity")
    parser.add_argument("-d",
                        "--debug",
                        action="store_const",
                        dest="verbose",
                        const=2,
                        help="log debug messages (same as -vv)")
    args = parser.parse_args()
    if args.verbose == 0:
        ugp4.logging.DefaultLogger.setLevel(level=ugp4.logging.INFO)
    elif args.verbose == 1:
        ugp4.logging.DefaultLogger.setLevel(level=ugp4.logging.VERBOSE)
    elif args.verbose > 1:
        ugp4.logging.DefaultLogger.setLevel(level=ugp4.logging.DEBUG)
        ugp4.logging.debug("Verbose level set to DEBUG")
    ugp4.logging.log_cpu(ugp4.logging.INFO, "Program started")

    # Define a parameter of type ugp4.parameter.Bitstring and length = 8
    word8 = ugp4.make_parameter(ugp4.parameter.Bitstring, len_=8)
    # Define a macro that contains a parameter of type ugp4.parameter.Bitstring
    word_macro = ugp4.Macro("{word8}", {'word8': word8})
    # Create a section containing a macro
    word_section = ugp4.make_section(word_macro, size=(1, 1), name='word_sec')

    # Create a constraints library
    library = ugp4.Constraints()
    # Define the sections in the library
    library['main'] = [word_macro]

    # Define the evaluator method and the fitness type
    def evaluator_function(data: str):
        count = data.count('1')
        return list(str(count))

    library.evaluator = ugp4.fitness.make_evaluator(evaluator=evaluator_function,
                                                    fitness_type=ugp4.fitness.Lexicographic)

    # Create a list of operators with their aritiy
    operators = ugp4.Operators()
    # Add initialization operators
    operators += ugp4.GenOperator(ugp4.create_random_individual, 0)
    # Add mutation operators
    operators += ugp4.GenOperator(ugp4.hierarchical_mutation, 1)
    operators += ugp4.GenOperator(ugp4.flat_mutation, 1)

    # Create the object that will manage the evolution
    mu = 10
    nu = 20
    sigma = 0.7
    lambda_ = 7
    max_age = 10

    darwin = ugp4.Darwin(
        constraints=library,
        operators=operators,
        mu=mu,
        nu=nu,
        lambda_=lambda_,
        sigma=sigma,
        max_age=max_age,
    )

    # Evolve and print individuals in population
    darwin.evolve()
    logging.bare("Final population:")
    for individual in darwin.population:
        msg = f"Solution {str(individual.id)} "
        ugp4.print_individual(individual, msg=msg, plot=False)
        ugp4.logging.bare(f"Fitness: {individual.fitness}")
        ugp4.logging.bare("")

    # Print best individuals
    ugp4.print_individual(darwin.archive.individuals, msg="Archive:", plot=True, score=True)

    ugp4.logging.log_cpu(ugp4.logging.INFO, "Program completed")
    sys.exit(0)
