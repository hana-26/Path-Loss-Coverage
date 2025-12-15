# Path Loss & Coverage Prediction Tool

A graphical **Path Loss & Coverage Calculator** built with Python that predicts received power and coverage boundaries using **Friis Free Space** and **Two-Ray Ground Reflection** models, with a **receiver sensitivity threshold**.


# Project Overview

Wireless communication performance strongly depends on how signal power decays with distance and environment. This calculaator allows users to:

* Compute **path loss** and **received power** over distance
* Compare **Free Space (Friis)** and **Two-Ray Ground Reflection** models
* Visualize **coverage limits** based on receiver sensitivity
* Identify where communication is possible and where it fails

The application is implemented using **Tkinter** for the GUI and **Matplotlib** for visualization.



# Objectives 
The tool predicts received power under:

* Free Space (Friis Model)
*  Two-Ray Ground Reflection Model
* Receiver sensitivity threshold

It also:

* Shows where communication is possible
* Marks where received power drops below sensitivity
* Compares the realism and limitations of each model



#Theory Summary

### 1. Wireless Channel

A wireless channel describes how electromagnetic waves propagate from a transmitter to a receiver. During propagation, signals suffer from **attenuation**, **spreading loss**, and environmental effects such as reflections.

### 2. Why Path Loss Matters

Path loss determines the maximum communication distance and directly affects:

* Coverage area
* Link reliability
* Network planning and deployment



### 3. Friis Transmission Equation (Free Space Model)

The Friis model assumes ideal free-space propagation with a clear line-of-sight (LOS):


**Key Characteristics:**

* Power decays proportional to (1/d^2)
* Works best for unobstructed LOS scenarios
* Often **overestimates received power** in real environments



### 4. Two-Ray Ground Reflection Model

The Two-Ray model considers:

* A direct LOS path
* A reflected path from the ground

**Key Characteristics:**

* More realistic for mobile and terrestrial links
* Shows faster power decay ((1/d^4))
* Usually *more conservative* than Friis


### 5. Receiver Sensitivity

Receiver sensitivity is the **minimum received power** required for reliable signal decoding.

In this project, sensitivity is used to:

* Define the **coverage boundary**
* Determine the maximum communication distance

# Practical Implementation

### Input Parameters

The program accepts:

* Frequency (MHz or GHz)
* Transmit power (dBm)
* Transmit antenna gain (dBi)
* Receive antenna gain (dBi)
* Distance range (minimum to maximum)
* Transmitter height (m)
* Receiver height (m)
* Receiver sensitivity (dBm)


### Computations Performed

For each distance value, the program computes:

1. Path loss using Friis model
2. Path loss using Two-Ray model
3. Received power for both models
4. Coverage distance

# Output & Visualization

The tool generates:

* **Received Power vs Distance plot**

  * Friis model curve
  * Two-Ray model curve
  * Receiver sensitivity threshold (horizontal dashed line)
* **Vertical markers** showing maximum communication distance
* Annotated coverage distances for both models

Additionally, a results panel displays:

* Path loss values
* Received power at maximum distance
* Coverage comparison between models



# GUI Features

* Clean, professional Tkinter interface
* Input validation with error handling
* Embedded Matplotlib plots
* Sample values for quick testing
* Clear visual distinction between models



# Technologies Used

* **Python 3**
* **Tkinter** – GUI design
* **NumPy** – numerical computations
* **Matplotlib** – plotting and visualization


#Discussion

 **When does Free Space fail?**
  In urban or ground-level scenarios where reflections, diffraction, and obstacles dominate.

* **Why is Two-Ray more realistic?**
  It accounts for ground reflections and antenna heights, which are common in mobile communication systems.

* **Which model overestimates power?**
  The Friis Free Space model generally overestimates received power compared to Two-Ray.



# Conclusion

This project implements a complete **Path Loss & Coverage Prediction Tool**. It demonstrates both theoretical understanding and practical application of wireless propagation models.



# 📎 How to Run

```bash
python main.py
```

Ensure all required libraries are installed and Python 3 is used.
