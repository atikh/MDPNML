<p align="center">
    <img src="https://img.shields.io/badge/contributions-welcome!-green" alt="Contributions welcome!"/>
</p>

# MDPNML

MDPNML is a PNML-compatible representation for Multidimensional Stochastic Petri Nets (MDSPNs). Our goal is to encode every modeling element required for MDSPN simulation while remaining compatible with standard PNML parsers and simulators. MDPNML preserves PNML’s core structure (places, transitions, arcs, names, markings), while adding explicit dimension definitions and transition-level impact annotations for non-temporal dimensions, such as energy use and waste generation. MDSPN also records probability distributions, guard functions, and initial marking to ensure reproducibility and reliable model regeneration.
As illustrated in the following figure, MDPNML supports four main uses after MDSPN model extraction from the real system (though it is not limited to these four):

<img width="3244" height="1198" alt="4" src="https://github.com/user-attachments/assets/0e5f3643-3757-40e8-badd-3d11b3eef85d" />


1.	Unidimensional model analysis: MDPNML enables per-dimension model projections (time, energy, waste, CO₂), allowing  analysts to isolate, inspect, and edit a single dimension independently of the others.
2.	Time-oriented DTs: The time-oriented SPN remains in standard PNML format and can run unchanged on existing PNML-compliant simulators, enabling conventional discrete-event simulation studies and seamless deployment as time-oriented DTs.
3.	CDTs: The full MDPNML code preserves cross-dimension behavior and transition impacts, enabling synchronized simulation and what-if analysis across multiple objectives. By providing a standard encoding of the extracted MDSPN, MDPNML establishes a direct pipeline from model extraction to execution. The same model can run in different MDSPN simulators and be deployed in CDTs.
4.	Utilized for Explainability of CDTs

For detailed information on MDPNML generation, please refer to our published paper [1]. A case study example is available in the corresponding file on GitHub.


## Usage & Attribution

If you are using the tool for a scientific project please consider citing our [publication]
 #  - [...](https://www.researchgate.net/profile/Atieh-Khodadadi)
 [1].   @misc{Khodadadi2026,
    url = {[https://www.researchgate.net/publication/375758652_PySPN_An_Extendable_Python_Library_for_Modeling_Simulation_of_Stochastic_Petri_Nets](https://www.researchgate.net/publication/398860321_MDPNML_A_Multidimensional_Petri_Net_Markup_Language_Enabling_Construction_and_Simulation_of_Comprehensive_Digital_Twin_Models?_tp=eyJjb250ZXh0Ijp7InBhZ2UiOiJwcm9maWxlIiwicHJldmlvdXNQYWdlIjpudWxsLCJwb3NpdGlvbiI6InBhZ2VDb250ZW50In19)},
    year = 2026,
    month = {March},
    author = {Khodadadi, Atieh and Lazarova-Molnar, Sanja},
    title = {MDPNML: A Multidimensional Petri Net Markup Language Enabling Construction and Simulation of Comprehensive Digital Twin Models},
    conference = {14th International Conference on Model-Based Software and Systems Engineering (MODELSWARD},
    note = {preprint}
}  

For questions/feedback feel free to contact me: atieh.khodadadi@kit.edu


 
