<p align="center">
    <img src="https://img.shields.io/badge/contributions-welcome!-green" alt="Contributions welcome!"/>
</p>

# MDPNML

MDPNML is a PNML-compatible representation for Multidimensional Stochastic Petri Nets (MDSPNs). Our goal is to encode every modeling element required for MDSPN simulation while remaining compatible with standard PNML parsers and simulators. MDPNML preserves PNML’s core structure (places, transitions, arcs, names, markings), while adding explicit dimension definitions and transition-level impact annotations for non-temporal dimensions, such as energy use and waste generation. MDSPN also records probability distributions, guard functions, and initial marking to ensure reproducibility and reliable model regeneration.
As illustrated in the following figure, MDPNML supports four main uses after MDSPN model extraction from the real system (though it is not limited to these four):

<img width="442" height="130" alt="image" src="https://github.com/user-attachments/assets/4c5b42ef-46ac-40c2-afff-955dfb8138c3" />

1.	Unidimensional model analysis: MDPNML enables per-dimension model projections (time, energy, waste, CO₂), allowing  analysts to isolate, inspect, and edit a single dimension independently of the others.
2.	Time-oriented DTs: The time-oriented SPN remains in standard PNML format and can run unchanged on existing PNML-compliant simulators, enabling conventional discrete-event simulation studies and seamless deployment as time-oriented DTs.
3.	CDTs: The full MDPNML code preserves cross-dimension behavior and transition impacts, enabling synchronized simulation and what-if analysis across multiple objectives. By providing a standard encoding of the extracted MDSPN, MDPNML establishes a direct pipeline from model extraction to execution. The same model can run in different MDSPN simulators and be deployed in CDTs.
4.	Utilized for Explainability of CDTs

For detailed information on MDPNML generation, please refer to our published paper [1]. A case study example is available in the corresponding file on GitHub.


## Usage & Attribution

If you are using the tool for a scientific project please consider citing our [publication]
 #  - ...
 [1].   @misc{} 

For questions/feedback feel free to contact me: atieh.khodadadi@kit.edu


 
