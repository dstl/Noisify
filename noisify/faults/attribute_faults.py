from .fault import AttributeFault
from noisify.helpers.multi_dispatch import register_implementation
import random
from .utilities import typo


def get_mode_size(mode):
    return len([i for i in mode if i.isupper()])


class GaussianNoise(AttributeFault):
    """
    Applies a gaussian noise to a numeric object. Constitutively active.

    >>> noise = GaussianNoise(sigma=0.5)
    >>> noise.impact(27)
    28.08656007204934

    Numpy arrays like objects apply noise separately to each element.

    >>> import numpy as np
    >>> test = np.arange(5)
    >>> noise.impact(test)
    array([0.56983913, 0.92835482, 2.36240306, 2.87398093, 3.92371237])
    """
    def __init__(self, sigma=0):
        """
        Instantiate with sigma, mu is set to the value of the passed in object.
        :param sigma:
        """
        AttributeFault.__init__(self, sigma=sigma)
        self.sigma = sigma
        pass

    def condition(self, triggering_object):
        return True

    @register_implementation(priority=15)
    def pil_image(self, image_object):
        from PIL import Image
        import numpy as np

        input_size = (image_object.height, image_object.width, get_mode_size(image_object.mode))
        noise_mask = np.random.normal(scale=self.sigma, size=input_size)
        image_array = np.array(image_object)
        output = Image.fromarray(np.uint8(np.clip(image_array + noise_mask, 0, 255)))
        return output

    @register_implementation(priority=12)
    def pandas_df(self, data_frame):
        import numpy as np
        noise_mask = np.random.normal(scale=self.sigma, size=data_frame.shape)
        return data_frame.add(noise_mask)

    @register_implementation(priority=10)
    def numpy_array(self, array_like_object):
        import numpy as np
        noise_mask = np.random.normal(scale=self.sigma, size=array_like_object.size)
        return array_like_object + noise_mask

    @register_implementation(priority=1)
    def python_numeric(self, python_numeric_object):
        return random.gauss(python_numeric_object, self.sigma)


class UnitFault(AttributeFault):
    """
    Applies a user defined adjustment to the input numeric object. Useful for modelling unit errors.
    Constitutively active.

    >>> def celsius_to_kelvin(celsius_value):
    ...     return celsius_value + 273.15
    ...
    >>> kelvin_fault = UnitFault(unit_modifier=celsius_to_kelvin)
    >>> kelvin_fault.impact(21)
    294.15
    """
    def __init__(self, unit_modifier=None):
        """
        Instantiate with a function or lambda to apply the necessary unit conversion to a numeric
        :param unit_modifier:
        """
        if not unit_modifier:
            raise NotImplementedError('You need to provide a function to convert the units')
        AttributeFault.__init__(self, unit_modifier=unit_modifier)
        self.unit_modifier = unit_modifier
        pass

    def condition(self, triggering_object):
        return True

    @register_implementation(priority=15)
    def pil_image(self, image_object):
        from PIL import Image
        import numpy as np

        input_size = (image_object.height, image_object.width, get_mode_size(image_object.mode))
        image_array = np.array(image_object)
        output = Image.fromarray(np.uint8(np.clip(self.unit_modifier(image_array), 0, 255)))
        return output

    @register_implementation(priority=1)
    def numeric(self, numeric_object):
        return self.unit_modifier(numeric_object)


class CalibrationFault(UnitFault):
    """
    Subclass of UnitFault, adds a constant offset to the input numeric.
    Constitutively Active.

    >>> calibration_fault = CalibrationFault(10)
    >>> calibration_fault.impact(200)
    210
    """
    def __init__(self, offset=0):
        """
        Instantiate with a numeric offset value
        :param offset:
        """
        def offsetter(value):
            return value + offset
        UnitFault.__init__(self, unit_modifier=offsetter)
        pass


class InterruptionFault(AttributeFault):
    """
    Replaces input with None, activates according to set likelihood.

    >>> interrupt = InterruptionFault(1.0)
    >>> interrupt.impact('This can be anything')

    >>>
    """
    def __init__(self, likelihood=0):
        """
        Instantiate with likelihood of interruption as a 0-1 float.
        :param likelihood:
        """
        AttributeFault.__init__(self, likelihood=likelihood)
        self.likelihood = likelihood
        pass

    def condition(self, triggering_object):
        return random.random() < self.likelihood

    @register_implementation(priority=15)
    def pil_image(self, image_object):
        from PIL import Image
        import numpy as np

        input_size = (image_object.height, image_object.width, get_mode_size(image_object.mode))
        image_array = np.array(image_object)
        output = Image.fromarray(np.uint8(self.numpy_array(image_array)))
        return output

    @register_implementation(priority=12)
    def numpy_array(self, array_like_object):
        import numpy as np
        noise_mask = np.random.uniform(size=array_like_object.shape)
        output_array = array_like_object.copy()
        output_array[noise_mask < self.likelihood] = 0
        return output_array

    @register_implementation(priority=10)
    def impact_truth(self, truth):
        return None


class TypographicalFault(AttributeFault):
    """
    Applies a rough misspelling to the input using faults.utilities.typo()

    >>> from noisify.faults import TypographicalFault
    >>> typo_fault = TypographicalFault(1.0, 1)
    >>> typo_fault.impact('This is the original text')
    'Thhiisith heiginal etxt'
    """
    def __init__(self, likelihood=0, severity=0):
        """
        Instantiate with a likelihood of making a typo, and a severity metric, severities significantly larger than 1
        can lead to unstable behaviours
        :param likelihood:
        :param severity:
        """
        AttributeFault.__init__(self, likelihood=likelihood, severity=severity)
        self.likelihood = likelihood
        self.severity = severity

    def condition(self, triggering_object):
        return random.random() < self.likelihood

    @register_implementation(priority=1)
    def impact_string(self, string_object: str):
        return typo(string_object, self.severity)

    @register_implementation()
    def null_impact(self, truth_object):
        return truth_object
