.. _quickstart:

Quickstart
==========

If Noisify is :ref:`installed <install>` we can get to work with some examples!


Augmenting with recipes
-----------------------

Basic augmentation can be done very simply using basic recipes.

    >>> from noisify.recipes import *

The built in recipes are designed to work with a wide variety of different object types. Let's give it a go with
a simple python dict.

    >>> test_data = {'this': 1.0, 'is': 2, 'a': 'test!'}
    >>> human_noise = human_error(5)
    >>> print(human_noise(test_data))
    <generator object Noisifier.generate_reports at 0x7f2d67e0f570>

Recipes create Noisifier objects, these objects then generate observations based on what they are given. To get a simple
list, cast to list.

    >>> print(list(human_noise(test_data)))
    [Observed value: {'a': 'tset!', 'this': 2, 'is': 1.0}]

You can also use a noisifier on a list of data.

    >>> test_data = [{'test%d' % (index): "This is test run number %d" % index} for index in range(5)]
    >>> test_data
    [{'test0': 'This is test run number 0'},
     {'test1': 'This is test run number 1'},
     {'test2': 'This is test run number 2'},
     {'test3': 'This is test run number 3'},
     {'test4': 'This is test run number 4'}]
    >>> print(list(human_noise(test_data)))
    [Observed value: {'test0': 'This is test run number 0'},
     Observed value: {'test1': 'This is test run number 1'},
     Observed value: {'test2': 'hT iis testt unn umber2'},
     Observed value: {'test3': 'This is test run number 3'},
     Observed value: {'test4': 'This is test run number 4'}]

Let's have a closer look at what human_noise does.

    >>> print(human_noise)
    {'Noisifier': {'Reporter': {'Attributes': [],
                   'Faults': [Fault: TypographicalFault {'likelihood': 0.5, 'severity': 0.5},
                              Fault: ScrambleAttributes {'likelihood': 0.5, 'attribute_identifiers': None}]}}}

That's a lot of information!
The main thing to focus on is the 'Reporter' entry. This contains attributes (which we'll get to later) and Faults.
Faults are the methods used to modify the incoming data steam, here you can see the two being used, typographical faults
which scramble text and numbers, and attribute scrambling, this swaps values between keys in incoming dictionaries.

Let's have a look at another recipe.

    >>> print(machine_error(5))
    {'Noisifier': {'Reporter': {'Attributes': [],
                   'Faults': [Fault: GaussianNoise {'sigma': 0.5},
                              Fault: InterruptionFault {'likelihood': 0.05}]}}}

Can you tell what this does?

Applying Gaussian noise to a string doesn't make much sense. That's no issue here though, if noisify doesn't know how to
apply a given fault to a value, it won't try.

    >>> print(list(machine_error(5)(test_data)))
    [Observed value: {'test0': 'This is test run number 0'},
     Observed value: {'test1': 'This is test run number 1'},
     Observed value: {'test2': None},
     Observed value: {'test3': 'This is test run number 3'},
     Observed value: {'test4': 'This is test run number 4'}]


Custom Noisifiers
-----------------

Imagine we have a series of medical records, people's height and weight are generally measured in metres and kilograms.
Occasionally however somebody has their weight entered in pounds and their height in inches.
Let's say we've built a mechanism to find these wrongly entered values and we want to test it, how do we create this
data?
And more importantly, how do we tell when the noisifier has actually changed these values?

We need to create a custom noisifier.

First let's create some data.

    >>> import random
    >>> def build_patient_record():
    ...     return {'height': random.gauss(1.7, 0.1), 'weight': random.gauss(85, 10)}
    >>> build_patient_record()
    {'weight': 79.0702693462696, 'height': 1.690377702784025}

Now let's create some conversion functions for metric to imperial.

    >>> def kilo_to_pounds(weight):
    ...     return weight * 2.205
    ...
    >>> def metres_to_inches(height):
    ...     return height * 39.37
    ...
    >>>

Now let's create our *attributes*, this enables us to associate specific faults with specific values of the record.

    >>> from noisify.attributes import Attribute
    >>> from noisify.faults import UnitFault
    >>> height = Attribute('height', faults=UnitFault(likelihood=0.25, unit_modifier=metres_to_inches))
    >>> weight = Attribute('weight', faults=UnitFault(likelihood=0.25, unit_modifier=kilo_to_pounds))

Attributes take an identifier, this can be a key to a dictionary, or an attribute name of an object.

Now we build the reporter.

    >>> from noisify.reporters import Reporter
    >>> patient_reporter = Reporter(attributes=[height, weight])

That was easy, the reporter can be called on individual records, but won't accept data series.

    >>> patient_reporter(build_patient_record())
    Observed value: {'height': 1.8157596382670191, 'weight': 199.97545102729777}

To apply more generally, create a noisifier.

    >>> from noisify.recipes import Noisifier
    >>> patient_noise = Noisifier(reporter=patient_reporter)

Let's build some data and noisify it.

    >>> true_patients = [build_patient_record() for i in range(5)]
    >>> true_patients
    [{'height': 1.7831797462380368, 'weight': 84.70459461136014},
     {'height': 1.7661108421633465, 'weight': 87.20572747494349},
     {'height': 1.5047252739096044, 'weight': 102.7315276194823},
     {'height': 1.9371269447064758, 'weight': 78.54807087351945},
     {'height': 1.7624795973113694, 'weight': 76.47383227872784}]
    >>> processed_patients = list(patient_noise(true_patients))
    >>> processed_patients
    [Observed value: {'height': 1.7831797462380368, 'weight': 84.70459461136014},
     Observed value: {'height': 1.7661108421633465, 'weight': 192.2886290822504},
     Observed value: {'height': 59.24103403382112, 'weight': 102.7315276194823},
     Observed value: {'height': 76.26468781309394, 'weight': 78.54807087351945},
     Observed value: {'height': 1.7624795973113694, 'weight': 76.47383227872784}]

Report objects
--------------

Noisify reporters return report objects. These contain the observation made, but they also contain other information.
These are stored as additional attributes on the object.

The faults triggered on an object can be retrieved through the triggered_faults attribute. Continuing from our example
above:

    >>> for patient in processed_patients:
    ...     print(patient.triggered_faults)
    {'reporter': [], 'height': [], 'weight': []}
    {'reporter': [], 'height': [], 'weight': [Fault: UnitFault {'unit_modifier': <function kilo_to_pounds at 0x7f0b1fd17400>}]}
    {'reporter': [], 'height': [Fault: UnitFault {'unit_modifier': <function metres_to_inches at 0x7f0b1fd17488>}], 'weight': []}
    {'reporter': [], 'height': [Fault: UnitFault {'unit_modifier': <function metres_to_inches at 0x7f0b1fd17488>}], 'weight': []}
    {'reporter': [], 'height': [], 'weight': []}

The ground truth is also stored.

    >>> for patient in processed_patients:
    ...     print(patient.truth)
    {'height': 1.7831797462380368, 'weight': 84.70459461136014}
    {'height': 1.7661108421633465, 'weight': 87.20572747494349}
    {'height': 1.5047252739096044, 'weight': 102.7315276194823}
    {'height': 1.9371269447064758, 'weight': 78.54807087351945}
    {'height': 1.7624795973113694, 'weight': 76.47383227872784}

Recipes
-------

Recipes are simply factory functions for noisifiers. Consider the built in 'human_error' recipe.


    >>> def human_error(scale):
    ...     return Noisifier(
    ...         reporter=Reporter(
    ...             faults=[TypographicalFault(likelihood=min(1, 0.1*scale), severity=0.1*scale),
    ...                     ScrambleAttributes(scrambledness=0.1*scale)]
    ...         ),
    ...         faults=None
    ...     )
    >>>


Combining reporters and noisifiers
----------------------------------

The addition operator will combine reporters/ noisifiers into composites which will apply all faults from both original
reporters.

    >>> from noisify.recipes import machine_error, human_error
    >>> print(machine_error(5))
    {'Noisifier': {'Reporter': {'Attributes': [],
                  'Faults': [Fault: GaussianNoise {'sigma': 0.5},
                             Fault: InterruptionFault {'likelihood': 0.05}]}}}
    >>> print(human_error(5))
    {'Noisifier': {'Reporter': {'Attributes': [],
                  'Faults': [Fault: TypographicalFault {'likelihood': 0.5, 'severity': 0.5},
                             Fault: ScrambleAttributes {'likelihood': 0.5, 'attribute_identifiers': None}]}}}
    >>> print(machine_error(5) + human_error(5))
    {'Noisifier': {'Reporter': {'Attributes': [],
                  'Faults': [Fault: GaussianNoise {'sigma': 0.5},
                             Fault: InterruptionFault {'likelihood': 0.05},
                             Fault: TypographicalFault {'likelihood': 0.5, 'severity': 0.5},
                             Fault: ScrambleAttributes {'likelihood': 0.5, 'attribute_identifiers': None}]}}}



For custom faults and adding new datatype handlers to faults, see the :ref:`advanced <advanced>` section.
