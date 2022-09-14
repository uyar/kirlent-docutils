.. title:: Demo

:author: Turgut Uyar

----

Usage
=====

- run the commands:

.. code::

   kirlent2impressjs demo.rst demo-impress.html

   kirlent2revealjs demo.rst demo-reveal.html

----

Flags
=====

- use docutils HTML writer flags, like:

..

- ``--stylesheet``
- ``--link-stylesheet``
- ``--math-output`` (for mathjax for example)
- ``--help``

----

Slide Size
==========

- slides are 1920x1080 by default
- can be changed with the ``--slide-size`` flag

----

:layout: col1 col2

Multicolumn
===========

.. container:: layout:col1

   - uses grid for layout

.. container:: layout:col2

   - item 1
   - item 2
   - item 3

----

Annotations
===========

- annotations use Rough Notation

..

- `click me <annotate://box>`_

- these might miss if the content is scaled

----

Math
====

.. math::

   -b \pm \frac{\sqrt{b^2-4ac}}{2a}
