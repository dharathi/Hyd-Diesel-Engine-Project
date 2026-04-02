# Smart energy management system (SEMS) for hydrogen based engines

<p align="center">
  <img width="236" height="374" alt="image" src="https://github.com/user-attachments/assets/8bf38f43-5601-4f39-a5ca-35269dc34d34" />
</p>

This repository contains the work on the research which focuses on developing a software-based SEMS for a hydrogen–diesel hybrid engine. The hybrid system generates hydrogen on-demand using a PEM electrolyzer powered by the engine.
This work aims to build a control system for the hybrid engine to:
- Control the hydrogen–diesel fuel blend dynamically based on engine load conditions
- Manage energy flow intelligently between subsystems (diesel engine, electrolyzer, fuel cell, battery if applicable)

## Datasets
| Sl. No | Dataset Name | Description | Source |
|--------|-------------|------------|--------|
| 1 | VED (Vehicle Energy Dataset) | Time-stamped naturalistic driving records of 383 vehicles (including gasoline ICE vehicles, EV, HEV, PHEV). Load changes and respective fuel consumption is recorded. | [Link](https://github.com/gsoh/VED/blob/master/README.md) |
| 2 | Dual-Fuel Engine Combustion Dataset | Contains 1463 records of data on performance and emission characteristics of a dual-fuel ICE operating under various load conditions and fuel ratios. | [Link](https://www.kaggle.com/datasets/ziya07/dual-fuel-engine-combustion-dataset) |
| 3 | Diesel Engine OBD2 Dataset (Ford Fiesta TDCi) | Experimental dataset collected using an OBD2 data logger from a Ford Fiesta TDCi diesel engine, including real-time vehicle parameters such as speed, engine RPM, and fuel consumption under varying operating conditions. | Self-collected |
