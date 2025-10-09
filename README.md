# Singular-Templates-Of-Imaging-Cherenkov-Showers (STOICS)

**An analysis package for IACT gamma-ray data using singular-template background modeling**

---

## Table of Contents

1. [Overview](#overview)  
2. [Features & Motivation](#features-motivation)  
3. [Quick Start / Example](#quick-start)  

---

This package can be used locally for IACT data analysis. 

Requirements 
------------ 

- Python 3.8 or newer
- Recommended packages: numpy, scipy, matplotlib, astropy, ROOT, csv

This section summarizes the main scripts provided. 

- make_vts_db_script.py: Generates shell scripts for run querying.
- make_condor_scripts.py: Builds job scripts for Condor clusters.
- save_big_matrices.py: Saves matrices of OFF run observations later for SVD construction of background templates.
- build_eigenvectors.py: Performs singular value decomposition and saves singular vectors (templates).
- save_skymaps.py: Analyzes ON run data and builds background models from the singular templates, then save the background-subtracted data sky maps.
- plot_analysis_result.py: Generates diagnostic and summary plots.
  

## 1. Overview

This package implements a **singular template method** for background estimation in **Imaging Atmospheric Cherenkov Telescopes (IACT)** gamma-ray data.  
It constructs background templates from cosmic-ray–like (OFF) events via singular value decomposition (SVD), and applies them to estimate gamma-like background in ON (signal) regions.

The goal is to reduce systematic background bias and improve sensitivity in source detection and morphology studies.

---

## 2. Features & Motivation

- Uses **data-driven templates** extracted from matched OFF-run events  
- Applies **SVD / eigenvector decomposition** to stabilize background modeling  
- Modular scripts covering:  
  - Querying observational runs  
  - Building background templates  
  - Predicting backgrounds for signal runs  
  - Visualization & comparison of results  
- Designed to interface with ROOT / VEGAS data formats common in IACT workflows

---

## 3. Quick Start / Example

Here’s a minimal end-to-end example (assuming you have prepared input data):

# 1. Setup environment variables (example)
In bash:

export SMI_INPUT=/path/to/root/files

export SMI_AUX=/path/to/auxiliary/files

export SMI_DIR=/path/to/working/dir

export SMI_RUNLIST=/path/to/job/output

export SMI_OUTPUT=/path/to/analysis/outputs

export SKY_TAG="fullspec16"

# 2. Generate run scripts

Execute "python3 make_vts_db_script.py"

The script you will be using is veritas_db_query.py,
you will need to define an output dir in the script, 
e.g. output_dir = "output_vts_query_default", and create this dir in your working space.
Then you can run "python3 make_vts_db_script.py", which will create shell scripts in the "run" folder, e.g. "vts_db_Geminga.sh"
You can add new sources in make_vts_db_script.py, e.g.
input_params += [ ['source_name', source_RA, source_DEC  , min_elevation, max_elevation] ]

Execute "sh vts_db_Geminga.sh"

You can execute "sh vts_db_Geminga.sh", and the code will search for ON runs and OFF runs in the database and save the run lists in the "output_vts_query_default" folder.
Use Geminga as an example, you can find the ON runlist in this file: output_vts_query_default/RunList_Geminga_V6.txt
and the OFF runs in output_vts_query_default/PairList_Geminga_V6.txt 
In PairList_Geminga_V6.txt, the first column is the ON runs, and the second column is the matched OFF runs.

# 3. Serialize the background maps of the OFF runs and build a large matrix of OFF runs:

Run "python3 make_condor_scripts.py" 

This creates shell scripts for the matrix method jobs. The scripts will be stored in the "run" folder.

Execute "sh run/save_mtx_Geminga_ON.sh" 

This will read all OFF-run ROOT files and build a large matrix of the OFF-run background templates.
The output files will be stored in $SMI_OUTPUT

# 4. SVD the large metrix and build eigenvectors of the background templates:

Execute "sh run/eigenvtr_Geminga_ON.sh", 

This performs singular value decomposition on the large matrix and build singular vectors of the background template.
The output files will be stored in $SMI_OUTPUT, and you can see plots of the singular vectors in "output_plots" folder.

# 5. Analyze the ON runs and use the eigenvectors to predict background model:

Execute "sh run/skymap_Geminga_ON.sh"

This will analyze the ON runs, produce sky map data of the source, and store output files in $SMI_OUTPUT.

# 6. Make plots for the paper:

Execute "sh run/plot_Geminga_ON.sh"

Your analysis plots, including sky maps (significance, flux, count), spectra, surface brightness profiles, will be created in the "output_plots" folder.

## Future plans

- Accelerate gradient descent to find the optimal signular template solution. 
- Implement uncertainty propagation.
- Support for next-generation CTA data format.


## Acknowledgments 

Developed by **Ruo Yu Shang** at Barnard College / Columbia University. 
Special thanks to the VERITAS collaboration for access to data and infrastructure.


