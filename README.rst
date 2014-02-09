=======
Pagrant
=======

- `GitHub <https://github.com/markshao/pagrant>`_
- `Pagrant Site <http://markshao.github.io/pagrant>`_

Pagrant is the next generation test framework on the cloud.

Pagrant support lxc by default. You can directly create the multiple test machines of the test environment though the Pagrant. With the help of the plug-in you can make Pagrant support the other cloud platform such as AWS,OpenStack,vCloud,etc.


Install
=======
::

    pip install pagrant

Vmprovider management
=====================

Pagrant natively support the lxc container as the vmprovider . But to be a ecosystem,we provider the way to create the vmprovider as the 3rd party plugin-in.
Pagrant provider a bundle of command lines to manage the vmprovider.

List all the vmproviders installed
----------------------------------
::

    pagrant vmprovider list


Install the vmprovider
----------------------
::

    pagrant vmprovider install [vmprovider name]


Uninstall the vmprovider
------------------------
::

    pagrant vmprovider remove [vmprovider name]



