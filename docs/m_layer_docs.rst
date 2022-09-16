.. _mlayer_docs:

======================
M-layer-concept design
======================

There are two distinct parts to the m-layer-concept package. 
One part consists of data in JSON files, the other is a collection of Python modules.

The JSON data is indicative of the information that will be kept on an
authoritative M-layer register. In this concept implementation, the coverage 
of the JSON data is limited (many more entries are needed to properly
support something like the SI Brochure). However, the JSON data is just
intended to show what is needed in a full implementation.

.. toctree::
   :maxdepth: 1

   JSON register entries <m_layer_json>

The `m-layer-concept` Python package is indicative of client-side software
that will make use of the M-layer register.

This module may itself be considered as two distinct parts. 
One is a Python class that provides an API
to access the M-layer register (in this case, JSON data). 
The other part provides functionality for third-party
applications that use the M-layer to annotate data.

.. toctree::
   :maxdepth: 1

   Python m-layer-concept modules <m_layer_src> 
