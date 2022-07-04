.. _changes:

.. include:: ../CHANGES.rst

Roadmap
=======

    -   In version 0.2.x, the intention is to develop the basic M-layer structure using a simple collection of JSON files to represent the central register of information about scales, aspects, conversions, and castings. The aim is to create a register with sufficient detail to support a few use-cases. No attempt is made to be comprehensive.

        At the same time a Python API will be developed to explore client-side usability of the M-layer and to support a suite of examples.

    -   Later versions will look at:

        - Manifests of M-layer references that record the digital identifiers used in a dataset.
        - Multiple M-layer registers. Supplementary registers could hold records that are not available in the central register. This will provide a mechanism for growing the M-layer.
        - Strategies for constructing M-layer registry records. How can logical relationships between many sets of units be exploited to generate records algorithmically while also including references to external information (that is unstructured)?
        - Strategies for testing and validating M-layer records.

