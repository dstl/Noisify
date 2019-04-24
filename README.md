# Noisify

[![Documentation Status](https://readthedocs.org/projects/noisify/badge/?version=latest)](https://noisify.readthedocs.io/en/latest/?badge=latest)

Noisify is a simple light weight library for augmenting and modifying data by adding realistic noise.
 
## Introduction

Add some human noise (typos, things in the wrong boxes etc.)

    >>> from noisify.recipes import human_error
    >>> test_data = {'this': 1.0, 'is': 2, 'a': 'test!'}
    >>> human_noise = human_error(5)
    >>> print(list(human_noise(test_data)))
    [{'a': 'tset!', 'this': 2, 'is': 1.0}]
    >>> print(list(human_noise(test_data)))
    [{'a': 0.0, 'this': 'test!', 'is': 2}]

Add some machine noise (gaussian noise, data collection interruptions etc.)

    >>> from noisify.recipes import machine_error
    >>> machine_noise = machine_error(5)
    >>> print(list(machine_noise(test_data)))
    [{'this': 1.12786393038729, 'is': 2.1387080616716307, 'a': 'test!'}]

If you want both, just add them together

    >>> combined_noise = machine_error(5) + human_error(5)
    >>> print(list(combined_noise(test_data)))
    [{'this': 1.23854334573554, 'is': 20.77848220943227, 'a': 'tst!'}]

Add noise to numpy arrays

    >>> import numpy as np
    >>> test_array = np.arange(10)
    >>> print(test_array)
    [0 1 2 3 4 5 6 7 8 9]
    >>> print(list(combined_noise(test_array)))
    [[0.09172393 2.52539794 1.38823741 2.85571154 2.85571154 6.37596668
                      4.7135771  7.28358719 6.83600156 9.40973018]]

Read an image

    >>> from PIL import Image
    >>> test_image = Image.open(noisify.jpg)
    >>> test_image.show()


![alt text](docs/_static/noisify.jpg "Original Image")

And now with noise

    >>> from noisify.recipes import human_error, machine_error
    >>> combined_noise = machine_error(5) + human_error(5)
    >>> for out_image in combined_noise(test_image):
    ...     out_image.show()

![alt text](docs/_static/noisy_noisify.jpg "Noisy Image")

*Noisify* allows you to build flexible data augmentation pipelines for arbitrary objects.
All pipelines are built from simple high level objects, plugged together like lego.
Use noisify to stress test application interfaces, verify data cleaning pipelines, and to make your ML algorithms more
robust to real world conditions.

## Installation

#### Prerequisites
Noisify relies on Python 3.5+
 
#### Installation from pipy
    $ pip install noisify

## Additional Information

Full documentation is available at [ReadTheDocs](https://noisify.readthedocs.io/en/latest/).
## Licence

Dstl (c) Crown Copyright 2019

Noisify is released under the MIT licence
