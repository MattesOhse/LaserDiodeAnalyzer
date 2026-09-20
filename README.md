## The Laser Diode Analyzer
This Python-bases analysis tool automates the evaluation of raw measurement data obtained during the investigation of pulsed laser diodes.

**Note**: This code was developed between 2021 and 2023 without AI assistance.

### This Respository

This repository contains two directories. In the directory `small_testdataset`, you will find a typical example of a raw dataset obtained during the electro-optical investigation of a pulsed laser diode.
The dataset contains measurements of an intensity autocorrelation (ACF), the current-voltage-power characteristics of the laserdiode (PUI), the optical spectrum (S), and the radio-frequency spectrum of the laser diode (RF) for different frequency spans.

**Analyse the Data**
In the directory `LaserDiodeAnalyzer`, you will find the program for analyzing the test dataset.
To start the analysis, run the script `gui_main.py`. A graphical user interface (GUI) will open, allowing you to select multiple folder containing the raw measurement datasets using the Browse button.
Using the checkboxes , you can select which types of measurement data you want to analyze (PUI, ACF, optische Spektren, Rf Spektren). 
Press the **"Auswertung Starten"** button to start the analysis.



