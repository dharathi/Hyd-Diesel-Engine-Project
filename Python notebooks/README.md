## Notebook details

**1. Dual_Fuel_Engine_Combustion_Dataset.ipynb:** 
- Dataset: Kaggle-dual-fuel-data
- Models used: Linear regressor, Random forest
- Parameters predicted: Diesel energy share/Gasoline energy share
- Results:
  <img width="852" height="240" alt="Screenshot 2026-03-27 at 11 10 46" src="https://github.com/user-attachments/assets/eebb20a0-694f-4460-a4ff-c9b12edbed61" />

**2. Data-preparation-VED.ipynb:**
- Dataset: VED-dataset
- Details: Code to analyse the data and separate the hybrid engines' (HEV & PHEV) dynamic data from other engine data

**3. NN_VED.ipynb:**
- Dataset: VED-dataset
- Model: Self-built neural network
- Parameters predicted: Fuel rate (L/hr) and state of charge (SOC)
- Results:
<img width="337" height="150" alt="image" src="https://github.com/user-attachments/assets/7704bda8-cdd4-4d62-816c-e62835b06428" />

**4. NN_VED_OBD2_Test.ipynb:**
- Dataset: OBD2-datalogger/Fiesta-TD-Ci
- NN built in 'NN_VED.ipynb' trained on VED dataset was loaded and tested on data collected from a diesel engine car using OBD2 data logger.

