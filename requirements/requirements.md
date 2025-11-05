# Detecting Trajectory Spoofing Attacks on AIS

>isabella.marasco4@unibo.it

Modern maritime navigation is critically dependent on the Automatic Identification
System (AIS) for situational awareness and collision avoidance. However, this reliance
creates a significant cyber-physical vulnerability. AIS protocols were not initially
designed with robust security in mind, making them susceptible to cyberattacks, most
notably spoofing.

In a spoofing attack, an adversary transmits falsified AIS signals to deceive a vessel's
receiver about its true position, course, or speed. Such an attack can silently induce
dangerous course deviations, leading to potential collisions, groundings, or illicit
navigation into hostile waters. The consequences are potentially catastrophic.
This project aims to model this threat and build an intelligent system capable of
defending against it.

Goals:
- Data Curation & Attack Simulation: Curate a real-world AIS trajectory dataset
and synthesize two distinct, plausible attack scenarios to create a "ground truth"
compromised dataset:
    - Silent Drift: it changes the ship's position (Lat/Lon) by applying a small,
constant offset that increases over time. The ship is thus silently “pushed”
off course, toward danger or a hostile area.
    - Kinematic Inconsistency: it manipulates only certain data, creating a
physically impossible AIS message. For example, they change the
position (Lat/Lon) to show a sharp turn, but leave the SOG (speed) and
COG (course) fields unchanged, which still indicate straight navigation.

- Use LSTM and Liquid Neural Network (LNN) for the dual purpose of:
    - Predicting a vessel's future trajectory.
    - Detecting anomalous deviations indicative of an attack.

- Measure how well the model predicts not only the trajectory but also the
presence of anomalies.
- Compare the model's ability to correctly predict the trajectory in the dataset
without attacks and in the dataset with attacks

Dataset: U.S. Maritime Administration (focus on the 2024 and 2025 data for this project)

[Dataset](https://hub.marinecadastre.gov/pages/vesseltraffic)

References:

[Vessel Trajectory Prediction in Maritime Transportation: Current Approaches and Beyond](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9843851)

[AIS-Based Intelligent Vessel Trajectory Prediction Using Bi-LSTM](https://ieeexplore.ieee.org/abstract/document/9721877)
