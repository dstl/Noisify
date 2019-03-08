.. Noisify documentation master file, created by
   sphinx-quickstart on Wed Feb 13 09:46:40 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Noisify: All purpose data augmentation
======================================

Release v\ |version|. (:ref:`Installation <install>`)


**Noisify** is a simple light weight library for augmenting and modifying data by adding realistic noise.


-------------------

**Let's make some noise**::

Add some human noise (typos, things in the wrong boxes etc.)

    >>> from noisify.recipes import human_error
    >>> test_data = {'this': 1.0, 'is': 2, 'a': 'test!'}
    >>> human_noise = human_error(5)
    >>> print(list(human_noise(test_data)))
    [Observed value: {'a': 'tset!', 'this': 2, 'is': 1.0}]
    >>> print(list(human_noise(test_data)))
    [Observed value: {'a': 0.0, 'this': 'test!', 'is': 2}]

Add some machine noise (gaussian noise, data collection interruptions etc.)

    >>> from noisify.recipes import machine_error
    >>> machine_noise = machine_error(5)
    >>> print(list(machine_noise(test_data)))
    [Observed value: {'this': 1.12786393038729, 'is': 2.1387080616716307, 'a': 'test!'}]

If you want both, just add them together

    >>> combined_noise = machine_error(5) + human_error(5)
    >>> print(list(combined_noise(test_data)))
    [Observed value: {'this': 1.23854334573554, 'is': 20.77848220943227, 'a': 'tst!'}]

Add noise to numpy arrays

    >>> import numpy as np
    >>> test_array = np.arange(10)
    >>> print(test_array)
    [0 1 2 3 4 5 6 7 8 9]
    >>> print(list(combined_noise(test_array)))
    [Observed value: [0.09172393 2.52539794 1.38823741 2.85571154 2.85571154 6.37596668
                      4.7135771  7.28358719 6.83600156 9.40973018]]

Add noise to images

    >>>

**Noisify** allows you to build flexible data augmentation (and corruption) pipelines for arbitrary objects.
All pipelines are built from simple high level objects, plugged together like lego.
Use noisify to stress test application interfaces, verify data cleaning pipelines, and to make your ML algorithms more
robust to real world conditions.

Features
----------------

Noisify provides data augmentation through a simple high level abstraction

- Build reporters to apply augmentation to any object
- Compose augmentations from configurable flaw objects
- Build recipes to configure new reporters using single parameters
- Everything is composable, everything is polymorphic

Noisify is built for python 3+.

The Basics
----------

What is noisify and how to use it.

.. toctree::
   :maxdepth: 2

   basics/introduction
   basics/install
   basics/quickstart
   basics/advanced


The Community Guide
-------------------

Our release process and community support process.

.. toctree::
   :maxdepth: 2

   community/support
   community/updates
   community/release-process

The API Documentation / Guide
-----------------------------

Full documentation of the noisify API, generated from doc strings.

.. toctree::
   :maxdepth: 2

   api


The Contributor Guide
---------------------

If you'd like to contribute, this is for you.

.. toctree::
   :maxdepth: 2

   dev/contributing
   dev/philosophy
