.. _changes:

.. include:: ../CHANGES.rst

Roadmap
=======

    -   In version 0.2.x, the intention is to build up the basic M-layer structure in a collection of JSON files representing central-register information about scales, aspects, conversions, and castings. The aim is to build up sufficient information to support a few use-cases. No attempt is made to be comprehensive.

        At the same time a Python API will be developed. This will support a suite of examples and client-side usability to be assessed.

    -   Later versions will look at:

        - M-layer manifests that record the digital identifiers used in a dataset. Manifests would be intended to accompany datasets.
        - Multiple M-layer registers. Supplementary registers could hold records not available in a central register. This will provide a mechanism for growing the M-layer.
        - Strategies for constructing M-layer registry records will be developed. Logical relationships between many sets of units can be exploited to generate records algorithmically, but automatically including references to external information is more complicated.  
        - Strategies for testing and validating M-layer records will be developed.

