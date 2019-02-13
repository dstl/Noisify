from noisify.faults import TypographicalFault, ScrambleAttributes, GaussianNoise, InterruptionFault
from noisify.reporters import Noisifier, Reporter


def human_error(scale):
    return Noisifier(
        reporter=Reporter(
            faults=[TypographicalFault(likelihood=min(1, 0.1*scale), severity=0.1*scale),
                    ScrambleAttributes(scrambledness=0.1*scale)]
        ),
        faults=None
    )


def machine_error(scale):
    return Noisifier(
        reporter=Reporter(
            faults=[GaussianNoise(sigma=0.1*scale),
                    InterruptionFault(likelihood=min(1, 0.01*scale))]
        ),
        faults=None
    )
