---
title: 'TPIB - Transformation Peak Iterative Baseline'
tags:
  - transformation peak
  - baseline
  - python
authors:
 - name: Daniel Roberto Cassar
   orcid: 0000-0001-6472-2780
   affiliation: Vitreous Materials Lab., Federal University of Sao Carlos, Sao Carlos-SP, Brazil
date: 11 August 2016
bibliography: paper.bib
---

# Summary

This is an algorithm that takes transformation peak data as input, computes a transformation-aware iterative baseline, and returns the peak data with subtracted baseline. It is based on the works of Reis and co-authors (@reis_assessments_2012, @reis_determination_2016), who were interested in the calorimetric crystallization peak of liquids under constant heating rates.

During the crystallization peak, two different phases are present at the same time: the liquid and the crystal. These phases have different thermal properties (such as heat capacity, for example) and thus a linear baseline is often not the optimal solution. This algorithm takes into account the amount of transformed phase for each peak datapoint to compute a physically reasonable baseline that is often of sigmoidal shape.

![Example of a raw calorimetric data obtained via Differential Scanning Calorimetry (DSC)](raw_data.png)

Figure 1: Example of a raw calorimetric data obtained via Differential Scanning Calorimetry (DSC). In this case the X data is the absolute temperature and the Y data is the DSC signal.

![Crystallization peak from Figure 1 after running the TPIB algorithm](peak.png)

Figure 2: Crystallization peak from Figure 1 after running the TPIB algorithm. The peak was normalized to have area equal to one.

There are commercial software available that compute what is called "a sigmoidal baseline". However, two problems arise because of the closed nature of these software: different software can yield different results, and results obtained from the same software for different samples may be unreliable because of some assumption in the code that is not clear to the end user. These two problems can be solved with this open-source code.

# References
