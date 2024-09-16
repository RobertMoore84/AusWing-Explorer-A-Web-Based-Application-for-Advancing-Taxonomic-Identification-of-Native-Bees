# AusWing Explorer: A Web-Based Application for Advancing Taxonomic Identification of Native Bees Through Integrated Morphometric Analysis

## Project Overview
This repository contains the code and data used for the development and evaluation of AusWing Explorer, a web-based application designed to advance the taxonomic identification of Australian native bees. The project utilizes geometric morphometrics to analyze wing venation patterns, enabling classification from the family level down to species. The tool is accessible to both professional and non-professional users, providing an efficient method for bee identification and aiding in biodiversity conservation efforts.

## Abstract
The biodiversity crisis, coupled with the taxonomic impediment, underscores the need for advanced tools to accurately identify and monitor species. AusWing Explorer addresses this challenge by using geometric morphometrics for bee identification, with a focus on Australian native bees. The web-based application enables users to upload bee wing images, landmark them, and receive classification results. This project aims to enhance taxonomic research and conservation efforts by providing a user-friendly tool for precise bee identification.

## Keywords
- Geometric morphometrics
- Bee taxonomy
- Native bees
- Species identification
- Web-based application
- Biodiversity conservation

## Repository Structure
This repository is organized into the following folders and files:

### Folders:
- `Data/`: Contains the annotated bee images and classification results.
- `Scripts/`: Contains Python scripts for processing images, performing analysis, and generating results.

### Scripts:
- `auswing_explorer.py`: Main script for the AusWing Explorer application, handling image uploads, landmarking, and classification.
- `lda_analysis.py`: Script for performing Linear Discriminant Analysis (LDA) on the landmark data.
- `tsne_visualization.py`: Script for visualizing the landmark data using t-distributed Stochastic Neighbor Embedding (t-SNE).

## Scripts Overview

### 1. `auswing_explorer.py`
**Purpose:**
- Manages the web application interface.
- Handles image uploads, user landmarking, and classification.

**Outputs:**
- Classification results for uploaded bee images.
- Landmarking guidance and feedback.

**Dependencies:**
- Flask
- OpenCV
- NumPy
- Pandas

### 2. `lda_analysis.py`
**Purpose:**
- Performs Linear Discriminant Analysis (LDA) to classify bee species based on landmark data.

**Inputs:**
- Landmark data from annotated bee wing images.

**Outputs:**
- Classification results at the species level.

**Dependencies:**
- scikit-learn
- pandas
- numpy

### 3. `tsne_visualization.py`
**Purpose:**
- Visualizes the relationships between species, subgenera, genera, and families using t-SNE.

**Inputs:**
- Procrustes-aligned landmark data.

**Outputs:**
- 2D scatter plots with confidence ellipses for each taxonomic group.

**Dependencies:**
- scikit-learn
- matplotlib
- pandas

## Data Files
The dataset comprises annotated images of bee wings and their corresponding classification results:

- `Data/Images/`: Contains images of bee wings annotated with landmarks.
- `Data/Results/`: Contains the output files with classification results.

## Usage Instructions

### Setting Up the Environment:
1. Install the necessary packages: Flask, OpenCV, scikit-learn, matplotlib, pandas, numpy.

### Running the Application:
1. Update file paths in `auswing_explorer.py` to match your local directory.
2. Run the script to start the web application.
3. Upload bee wing images and follow the landmarking protocol to obtain classification results.

### Analyzing the Data:
1. Use `lda_analysis.py` to perform LDA on the landmark data.
2. Use `tsne_visualization.py` to generate t-SNE visualizations for exploring data relationships.

## Results
The results demonstrate the effectiveness of AusWing Explorer in classifying Australian native bees based on wing venation patterns. The tool provides accurate and accessible identification across various taxonomic levels, enhancing biodiversity research and conservation efforts.

## Citation
If you use this code or data for your own work, please cite the manuscript associated with this project:

**AusWing Explorer: A Web-Based Application for Advancing Taxonomic Identification of Native Bees Through Integrated Morphometric Analysis, [Your Name] (2024).**
