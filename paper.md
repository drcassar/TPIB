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
bibliography: references.bib
---

# Summary

This is an algorithm that takes a transformation peak data as an input, computes a transformation-aware iterative baseline, and returns the peak data with subtracted baseline. It is based on the works by Reis and co-authors [1,2], where they were interested in the calorimetric crystallization peak of liquids under constant heating rates. 

During the crystallization peak, two different phases are present at the same time: the liquid and the crystal. These phases have different thermal properties (such as heat capacity, for example) and because of this a linear baseline is often not the optimal solution. This algorithm takes into account the amount of transformed phase for each peak datapoint to compute a physically reasonable baseline.

![Example of a raw calorimetric data obtained via Differential Scanning Calorimetry (DSC)](raw_data.png)
Figure 1: Example of a raw calorimetric data obtained via Differential Scanning Calorimetry (DSC). In this case the X data is the absolute temperature and the Y data is the DSC signal.

![Crystallization peak from Figure 1 after running the TPIB algorithm](peak.png)
Figure 2: Crystallization peak from Figure 1 after running the TPIB algorithm. The peak was normalized to have area equal to one.

There are commercial software available that compute what is called "a sigmoidal baseline". However, two problems arise due to the closed nature of these software: different software can yield different results; and results done in the same software for different samples may yield unreliable results due to some assumption made in the code that is not clear to the end user. These two problems can be solved with this open-source code.

# References

[1] Reis, R.M.C.V. (2012). Assessments of viscous sintering models and determination of crystal growth rate and crystallized fraction in glasses. Ph.D. thesis. Universidade Federal de São Carlos.

[2] Reis, R.M.C.V., Fokin, V.M., and Zanotto, E.D. (2016). Determination of Crystal Growth Rates in Glasses Over a Temperature Range Using a Single DSC Run. Journal of the American Ceramic Society 99, 2001–2008.
