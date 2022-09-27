.. _mlayer_docs:

======================
M-layer-concept design
======================

There are two distinct parts to the m-layer-concept package. 
One part consists of data in JSON files, the other is a collection of Python modules.

The JSON data is indicative of the information that will be kept on an
authoritative M-layer register. In this concept implementation, the coverage 
of the JSON data is limited (many more entries are needed to properly
support something like the SI Brochure). The JSON data is just
intended to show what will be needed in a full implementation.

.. toctree::
   :maxdepth: 1

   JSON register entries <m_layer_json>

The `m-layer-concept` Python package is an implementation 
indicative of client-side software that will make use of the M-layer.

This package may itself be considered to have two distinct parts. 
One part is a Python class that provides an API
to access the M-layer register (in this case, JSON data). 
The other part implements functionality that third-party
applications could use to annotate data with the M-layer.

.. toctree::
   :maxdepth: 1

   Python m-layer-concept modules <m_layer_src> 
