# Digital Twin Design for DRL

## Purpose

This document maps the current neural-network work in this repository to the next thesis stage: a digital twin that can generate synthetic trajectories for deep reinforcement learning (DRL) training and testing.

The key idea is:

- the current notebooks are supervised learning models
- the digital twin must become a step-based simulation model
- the DRL agent will interact with that simulator through actions, rewards, and state transitions

So the next phase is not only "improve prediction accuracy". It is "convert the learned model into an environment that evolves over time".

## What We Have So Far

Current work in this repository already provides useful building blocks:

- `Dual_Fuel_Engine_Combustion_Dataset.ipynb`
  - predicts dual-fuel energy share
- `NN_VED.ipynb`
  - predicts fuel rate and SOC from VED hybrid-engine data
- `NN_VED_OBD2_Test.ipynb`
  - tests the saved VED model on diesel OBD2 data
- `NN_VED_OBD2_Transfer_Learning.ipynb`
  - shared-feature transfer learning between VED and OBD2
- `NN_VED_OBD2_Union_Multidomain.ipynb`
  - union-of-features, domain-aware model for VED and OBD2

These are valuable because they learn vehicle and engine behavior from data. However, they are still row-wise predictors, not digital twins.

## What a Digital Twin Must Add

A DRL-ready digital twin needs five core elements.

### 1. State

The state is the information describing the current engine or vehicle condition at time step `t`.

Candidate state variables for this project:

- vehicle speed
- engine RPM
- engine load
- manifold pressure
- coolant temperature
- fuel rate
- trip time or elapsed time
- latitude and longitude if route context is needed
- ambient temperature
- battery SOC for hybrid vehicles
- battery current and voltage for hybrid vehicles
- previous control action

The state should be compact enough for learning, but rich enough to capture engine dynamics.

### 2. Action

The action is the control decision chosen by the DRL agent.

This depends on the thesis problem. Examples:

- hydrogen substitution ratio
- diesel injection level
- fuel blending ratio
- torque split
- power management command
- engine operating mode

If the thesis is about hydrogen-diesel optimization, then the action should directly represent the controllable hydrogen/diesel decision.

### 3. Transition Model

The transition model determines how the system moves from:

`state_t + action_t -> state_t+1`

This is where a neural network or hybrid physics-data model can act as the core of the digital twin.

Instead of only predicting one target such as fuel rate, the transition model should predict the next-step system variables, for example:

- next fuel rate
- next SOC
- next speed
- next RPM
- next load
- next manifold pressure
- next temperatures

The exact list depends on which variables are observable and important for the controller.

### 4. Reward Function

The reward tells the DRL agent what "good" behavior means.

Possible reward terms:

- lower fuel consumption
- lower hydrogen consumption cost
- lower emissions
- maintain required performance
- avoid unsafe operating regions
- penalize unstable control actions

A generic form could be:

`reward = -a*fuel_use - b*emissions - c*constraint_violation + d*performance_score`

The reward should align with the research goal, not just predictive accuracy.

### 5. Termination Rules

The episode should stop when:

- the trip segment ends
- the simulated cycle ends
- SOC exceeds physical limits
- fuel or operating constraints are violated
- a fixed horizon is reached

## Recommended Thesis Architecture

The most practical next architecture is:

### Layer 1: Domain-Specific Surrogate Models

Use the existing NN work to create predictive components for:

- hybrid domain
- diesel domain
- dual-fuel / hydrogen-diesel domain later

These are not the full twin. They are internal predictive modules.

### Layer 2: Unified Transition Model

Build a step-based model that predicts the next state from current state and action.

Recommended form:

- input:
  - current state
  - chosen action
  - domain indicator
  - feature-availability mask if needed
- output:
  - next state variables
  - optional outputs such as fuel rate, SOC, emissions

This could be:

- a feedforward next-state model with lagged inputs
- an LSTM/GRU sequence model
- a physics-informed neural network
- a hybrid model combining rules and learned residuals

For this thesis, a feedforward next-state model with lagged variables is the simplest realistic next step.

### Layer 3: Gym-Style Environment

Wrap the transition logic in an environment with:

- `reset()`
- `step(action)`
- returned values:
  - `next_state`
  - `reward`
  - `done`
  - `info`

This is the component the DRL algorithm will actually train against.

## Suggested State for Version 1

A practical first digital twin state could be:

- `speed_t`
- `rpm_t`
- `load_t`
- `fuel_rate_t`
- `coolant_temp_t`
- `manifold_pressure_t`
- `ambient_temp_t`
- `soc_t` if hybrid
- `prev_action_t`
- `time_index_t`

If some variables are missing in diesel data, use a domain-aware design so the diesel branch does not require hybrid-only variables.

## Suggested Action for Version 1

If the thesis target is hydrogen-diesel optimization, a clean first action space is:

- continuous hydrogen substitution ratio in `[0, 1]`

Optional extensions:

- diesel injection level
- air-fuel ratio control
- mode-switch signal

If the thesis does not yet have real hydrogen control data, then the first twin can be built with a placeholder action model and later refined when the hydrogen-diesel experimental data is available.

## Suggested Outputs for Version 1

The transition model should predict:

- `fuel_rate_t+1`
- `speed_t+1`
- `rpm_t+1`
- `load_t+1`
- `soc_t+1` for hybrid domain

Optional additional outputs:

- emissions proxy
- efficiency proxy
- battery current/voltage next step

## How Current NN Work Fits In

### `NN_VED.ipynb`

Useful as:

- a hybrid-domain surrogate
- a source of feature engineering ideas
- a baseline for fuel + SOC prediction

Not enough by itself because:

- it is not step-based
- it does not model actions

### `NN_VED_OBD2_Transfer_Learning.ipynb`

Useful as:

- evidence that cross-domain prediction is possible but limited by shared features

### `NN_VED_OBD2_Union_Multidomain.ipynb`

Useful as:

- the strongest current bridge toward the digital twin
- a domain-aware architecture that can preserve richer signals

Still incomplete because:

- it predicts outputs from rows
- it does not simulate explicit next-state transitions
- it does not yet expose an RL action interface

## What To Build Next

The next milestone should be a notebook or module called something like:

- `Digital_Twin_Transition_Model.ipynb`

Its job should be:

1. convert raw data into sequential transitions
2. build training rows of the form:
   - current state
   - action
   - next state
3. train a next-state model
4. evaluate one-step prediction quality
5. run rollout tests over many time steps

After that, the next step should be:

- `digital_twin_env.py`

This file should wrap the learned transition model into a DRL environment.

## Recommended Data Structure for Transition Training

Training table layout:

- `state_t`
- `action_t`
- `state_t+1`
- `reward_t`

If no real action exists yet in current datasets:

- use a placeholder control input for now
- or define a rule-based proxy action
- or wait until hydrogen-diesel experimental data is available before final DRL training

This is important: a DRL environment without a meaningful action is not a proper control problem yet.

## Thesis Narrative You Can Use

The thesis progression can be framed as:

1. develop data-driven predictive models for hybrid and diesel engine behavior
2. evaluate domain transfer and feature mismatch across datasets
3. design a multi-domain surrogate model that preserves domain-specific information
4. convert the surrogate model into a digital twin transition model
5. use the digital twin as a safe and scalable environment for DRL training and evaluation

That is a strong and defensible story.

## Honest Assessment of Readiness

Current readiness:

- predictive surrogate models: yes
- cross-domain modeling foundation: yes
- digital twin: partially
- DRL-ready environment: not yet

So you are close to the digital twin conceptually, but the critical next jump is:

`row-wise prediction -> sequential transition simulation`

That should now be the focus.

## Recommended Immediate Next Deliverables

1. Define the exact control action for the thesis.
2. Decide the state variables for the first twin version.
3. Build a transition dataset from sequential rows.
4. Train a next-state model.
5. Validate multi-step rollouts.
6. Wrap it in a Gym-style environment for DRL.

## Best Next Coding Task

The most useful next file to create is:

- `Python notebooks/Digital_Twin_Transition_Model.ipynb`

That notebook should:

- explain the digital twin concept for the thesis
- define state, action, next state
- create transition tuples from sequential data
- train a next-state neural network
- test one-step and multi-step rollouts

Once that notebook exists, the project will be much closer to an actual DRL pipeline.
