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

  - ``--stylesheet``
  - ``--link-stylesheet``
  - ``--math-output mathjax``
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

:layout:
  s1  s1
  s21 s22
  s3  s3

Annotations
===========

.. container:: layout-s1

   - annotations use Rough Notation

.. container:: layout-s21

   - *>_underline annotation_<*
   - *>|box annotation|<*
   - *>(circle annotation)<*
   - *>!highlight annotation!<*

.. container:: layout-s22

   - *>~strike-through annotation~<*
   - *>+crossed-off annotation+<*
   - *>[bracket annotation]<*

:pause:

.. container:: layout-s3

   - *these might miss if the content is scaled*

----

Math
====

.. math::

   -b \pm \frac{\sqrt{b^2-4ac}}{2a}
