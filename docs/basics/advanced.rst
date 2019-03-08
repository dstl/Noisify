.. _advanced:

Advanced Usage
==============
This guide covers more advanced topics in noisify.

Defining Faults
---------------
Faults are defined by subclassing the base Fault class:

    >>> from noisify.faults import Fault
    >>> import random
    >>> class AddOneFault(Fault):
    ...     def __init__(self, likelihood=1.0):
    ...         self.likelihood = min(1.0, likelihood)
    ...
    ...     def condition(self, triggering_object):
    ...         return random.random < self.likelihood
    ...
    ...     @register_implementation(priority=1)
    ...     def add_to_string(self, string_object):
    ...         return string_object + "1"
    ...

Let's unpack this definition.

We have the constructor, this behaves as expected. In this case adding a likelihood attribute to the object.

Next we have a 'condition' method, this must be defined! It accepts the triggering object (that is the attribute or
report) this enables conditional activation based upon the content of the trigger (for example if a flaw is more likely
to happen for numbers then for strings).

Finally we have an implementation. This describes how a fault will act on the data it is given.

Implementations And The Dispatch Queue
--------------------------------------

The power of noisify lies in its ability to take a large variety of different data types and intelligently apply noise.
This mechanism is managed through the Dispatch Queue.

When an implementation is written for a given fault, it is decorated using the @register_implementation(priority=x)
decorator. This gives the implementation its place within the queue. When a fault is called upon an unknown object it
will attempt to apply each implementation in the queue to it in sequence. If all fail it will return the original object
unaffected.

Let's look at some source code for an example


    >>> class GaussianNoise(AttributeFault):
    ...     def __init__(self, sigma=0):
    ...         AttributeFault.__init__(self, sigma=sigma)
    ...         self.sigma = sigma
    ...         pass
    ...
    ...     def condition(self, triggering_object):
    ...         return True
    ...
    ...     @register_implementation(priority=10)
    ...     def numpy_array(self, array_like_object):
    ...         import numpy as np
    ...         noise_mask = np.random.normal(scale=self.sigma, size=array_like_object.size)
    ...         return array_like_object + noise_mask
    ...
    ...     @register_implementation(priority=1)
    ...     def python_numeric(self, python_numeric_object):
    ...         return random.gauss(python_numeric_object, self.sigma)

This fault will apply a gaussian noise filter to the input data. If the python_numeric implementation is called on a
numpy array then a single random value will be added to the entire array, this is not desired behaviour. To fix this a
second implementation with higher priority kicks in for numpy array like objects, this adds a separate offset to each
value independently.

Dispatch Through Type Annotations
---------------------------------

Dispatch should be handled through ducktyping where possible. However we recognise that cases exist where explicit
dispatch on type is needed, this can be done through type annotations on the relevant implementations as follows.

>>> class TypographicalFault(AttributeFault):
...     @register_implementation(priority=1)
...     def impact_string(self, string_object: str):
...         return typo(string_object, self.severity)
...
...     @register_implementation(priority=1)
...     def impact_int(self, int_object: int):
...         return int(self.impact_string(str(int_object)) or 0)

Implementation Dispatch And Inheritance
---------------------------------------

Implementations are passed down through inheritance. The main example of this is the AttributeFault fault type,
which adds a single implementation which will attempt to map the fault onto all elements of the input object. This can
be given to a Reporter to cause it to apply the fault to all of its attributes.

