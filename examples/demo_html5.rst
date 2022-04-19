.. title:: Document Title

================
Document Heading
================

:Author:  Document author. Also generates a :code:`head > meta`.
:License: Document license.

Document title is in :code:`head > title`.

Document heading is in :code:`body > main > h1`.
Normalized heading is id for :code:`main`.
Everything explained below is under :code:`main`.

Document info is in :code:`dl.docinfo`.
Normalized field names are classes for both :code:`dt` and :code:`dd`.
Colons are within :code:`span.colon`.

This is a paragraph.
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua.
*This is emphasized text.* (:code:`em`)
Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
aliquip ex ea commodo consequat.
**This is strong text.** (:code:`strong`)
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore
eu fugiat nulla pariatur.
``This is inline literal text.`` (:code:`span.literal`)
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia
deserunt mollit anim id est laborum.
This is an external link for
`reStructuredText <https://docutils.sourceforge.io/docs/user/rst/quickref.html>`_.
And this is an internal link to enumerated lists with
`lowercase alphabetic numbering`_.
An internal link target is a :code:`span` with the normalized text as its id.

| This is a paragraph where there is a line break (:code:`br`) at the end
  of every sentence (no :code:`div.line-block` for block and
  :code:`div.line` for each line).
| Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
  tempor incididunt ut labore et dolore magna aliqua.
| Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
  aliquip ex ea commodo consequat.

Lists
=====

This is a new section (:code:`section`).
Normalized section title is id for :code:`section`.
Section title is in :code:`section > h2`.
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Below is an itemized list (:code:`ul`):

- Item with single paragraph (no :code:`li > p`).

- Item with single paragraph.

- Item with multiple paragraphs. This is the first paragraph.

  This is the second paragraph. One :code:`li > p` for each paragraph.

- Item with single paragraph.

Below is an enumerated list (:code:`ol.arabic`):

#. Item with single paragraph (no :code:`li > p`).

#. Item with single paragraph.

#. Item with multiple paragraphs. This is the first paragraph.

   This is the second paragraph. One :code:`li > p` for each paragraph.

#. Item with single paragraph.

Numbering
---------

This is a subsection (:code:`section > section`).
Normalized subsection title is id for the inner :code:`section`.
Subsection title is :code:`section > section > h3`.
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Below is an enumerated list with _`lowercase alphabetic numbering`:
(:code:`ol.loweralpha`)

a. Item with single paragraph.
#. Item with single paragraph.
#. Item with single paragraph.

Below is an enumerated list with uppercase alphabetic numbering
(:code:`ol.upperalpha`):

A. Item with single paragraph.
#. Item with single paragraph.
#. Item with single paragraph.

Below is an enumerated list with lowercase Roman numbering:
(:code:`ol.lowerroman`)

i. Item with single paragraph.
#. Item with single paragraph.
#. Item with single paragraph.

Below is an enumerated list with uppercase Roman numbering
(:code:`ol.upperroman`):

I. Item with single paragraph.
#. Item with single paragraph.
#. Item with single paragraph.

Below is an enumerated list that starts from 7:

7. Item with single paragraph.
#. Item with single paragraph.
#. Item with single paragraph.

Definition List
---------------

Below is a definition list (:code:`dl`):

Definition term.
  A single paragraph description (no :code:`dd > p`).

Definition term.
  A multiple paragraph description. This is the first paragraph.

  This is the second paragraph. One :code:`dd > p` for each paragraph.

Definition term.
  A single paragraph description.

Field List
----------

Below is a field list (:code:`dl.field-list`):

:Field name:
  Single paragraph field value (no :code:`dd > p`).

:Field name:
  Multiple paragraph field value. This is the first paragraph.

  This is the second paragraph. One :code:`dd > p` for each paragraph.

:Field name:
  Single paragraph field value.

Literal Block
=============

Below is a literal block (:code:`pre`)::

  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
  tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
  quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
  consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
  cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
  non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Block Quote
===========

Below is a block quote (:code:`blockquote`):

  Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod
  tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
  quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
  consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse
  cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat
  non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Table
=====

Below is a grid table (:code:`table`).

+------------+------------+-----------+
| Header 1   | Header 2   | Header 3  |
+============+============+===========+
| body row 1 | column 2   | column 3  |
+------------+------------+-----------+
| body row 2 | Cells may span columns.|
+------------+------------+-----------+
| body row 3 | Cells may  | - Cells   |
+------------+ span rows. | - contain |
| body row 4 |            | - blocks. |
+------------+------------+-----------+

Below is a simple table (:code:`table`):

=====  =====  ======
  A      B    A or B
=====  =====  ======
False  False  False
True   False  True
False  True   True
True   True   True
=====  =====  ======

Code
====

This is an inline code example: :code:`body`.
This uses the :code:`code` element.

Below is a code block example (:code:`pre.code > code`).
The language name is also provided as a class name for :code:`pre`.

.. code:: c

   #include <stdio.h>

   int main(int argc, char* argv[])
   {
       printf("Hello, world!\n");
       return 0;
   }

Below is a transition (:code:`hr`).

----

**Footnotes**

Footnotes will be here.
