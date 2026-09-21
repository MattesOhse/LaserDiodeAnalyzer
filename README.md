## The Laser Diode Analyzer
This Python-bases analysis tool automates the evaluation of raw measurement data obtained during the investigation of pulsed laser diodes.

**Note**: This code was developed between 2021 and 2023 without AI assistance.

### This Respository

This repository contains two directories. In the directory `small_testdataset`, you will find a typical example of a raw dataset obtained during the electro-optical investigation of a pulsed laser diode.
The dataset contains measurements of an intensity autocorrelation (ACF), the current-voltage-power characteristics of the laserdiode (PUI), the optical spectrum (S), and the radio-frequency spectrum of the laser diode (RF) over different frequency spans.

#### Analyse the Data
In the directory `LaserDiodeAnalyzer`, you will find the program for analyzing the test dataset.
To start the analysis, run the script `gui_main.py`. A graphical user interface (GUI) will open, allowing you to select multiple folder containing the raw measurement datasets using the Browse button.
Using the checkboxes , you can select which types of measurement data you want to analyze (PUI, ACF, optische Spektren, Rf Spektren). 
Press the **"Auswertung Starten"** button to start the analysis.

## Discription of what this Program does 

### Backgrund to the experimental measurement
First, we apply a constant voltage to the absorber of the laser Diode. To investigate the electro-optical characteristics of the laser diode, we apply an excitation current to the active region and sweep this current. For each current step, we measure the optical output power, the opptical spectrum,the intensity autocorrelation of the light pulses, and the raidio-frequeny spectrum over different frequency spans.

#### The Results
When the analysis is complete, you will find a directory called `Auswertung`inside the directory containing the raw measurement data. Depending on which checkboxes you selected, you will find the corresponding analysis results.

If you run the full analysis with all chckboxes selected, you will get the following results:

1. **The dirctories `ACF`, `Opt`, `PUI` and `RF`**
    These directories contain the analysis results for the different measurements.

2. **A large number of CSV files**
    These files contain the most relevant results of the analyses for the different measurements.

In the following sections, I will explain the physical and mathematical background of these results for the different measurements and indicate the correspondinng files in which these results cen be found.








