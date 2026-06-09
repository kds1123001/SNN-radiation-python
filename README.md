# SNN-radiation-python
SNN Radiation is a high-performance, real-time 3D simulation framework engineered to model medical scanning hardware as it tracks metabolic anomalies within high-radiation environments. By simulating the complex interaction between diagnostic hardware and ionizing interference, the system provides a robust platform for testing fault-tolerant neural architectures under hardware-level stress.

The engine generates a high-fidelity 128-cubed voxel brain environment. This voxel space is processed in real-time, slicing the data along three critical clinical planes and rendering the output directly to the terminal via ANSI truecolor, providing immediate visual feedback on the state of the simulation.

Core Architecture & Capabilities
3D Volumetric Anatomy: The system constructs a 2-million-voxel brain model. By integrating structural elements—including the cortex, ventricles, thalamus, cerebellum, and brainstem—and applying Gaussian smoothing, the engine authenticates the simulation by mimicking the specific noise characteristics and structural properties of clinical MRI data.

Fault-Tolerant SNN Core: At the heart of the system is a 30-node input population layout, configured with overlapping Gaussian tuning curves. This design is specifically engineered for resilience; even if background radiation simulates corruption in the weight matrix, the network retains its spatial awareness and continues to process data effectively.

Biomimetic Dynamics: To achieve true time-scale invariance, the simulation implements explicit physical membrane potential decay. This is augmented by a sophisticated running trace homeostasis mechanism that dynamically manages neuronal thresholds, effectively preventing threshold chattering and ensuring the system remains stable during continuous operation.

Trajectory Tracking: To account for sensor noise, the engine utilizes a 4-state linear Kalman Filter. This module is essential for sanitizing incoming sensor data, allowing the simulation to generate clean, predictive paths for metabolic anomalies as they move through the voxel space.

SNN Radiation serves as a specialized tool for developers and researchers exploring the intersection of neuro-inspired computing and hardware reliability. By providing a controlled environment for testing how spike-based neural networks respond to environmental degradation, it enables the refinement of resilient algorithms suitable for deployment in high-interference or mission-critical diagnostic scenarios.


                            #NO PART OF THIS REPOSITORY WAS MADE USING AI NOR IMPROVED USING AI#
