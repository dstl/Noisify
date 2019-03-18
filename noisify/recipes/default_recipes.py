"""
.. Dstl (c) Crown Copyright 2019
Default recipes, these are extremely simple and are mainly to provide examples for developing your own code.
"""
from noisify.faults import TypographicalFault, ScrambleAttributes, GaussianNoise, InterruptionFault
from noisify.reporters import Noisifier, Reporter


def human_error(scale):
    """
    Simple example Noisifier recipe, applies typos and attribute scrambling to the input depending
    on the scale given, recommended scale range from 1-10
    """
    return Noisifier(
        reporter=Reporter(
            faults=[TypographicalFault(likelihood=min(1, 0.1*scale), severity=0.1*scale),
                    ScrambleAttributes(likelihood=0.1 * scale)]
        ),
        faults=None
    )


def machine_error(scale):
    """
    Simple example Noisifier recipe, applies gaussian noise and occasional interruptions to the input
    depending on the scale given, recommended scale range from 1-10
    """
    return Noisifier(
        reporter=Reporter(
            faults=[GaussianNoise(sigma=0.1*scale),
                    InterruptionFault(likelihood=min(1, 0.01*scale))]
        ),
        faults=None
    )
