# Import necessary libraries
import pandas as pd
from matplotlib.colors import ListedColormap
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
import os
from tqdm import tqdm

# Set the maximum number of CPU cores to be used
os.environ["LOKY_MAX_CPU_COUNT"] = "12"  # Replace "12" with the desired number of cores

# Load the CSV file into a pandas DataFrame
# Replace 'Replace with your actual file path' with the path to your CSV file
df = pd.read_csv('Replace with your actual file path')

# Select the columns containing the coordinates for t-SNE
# Adjust this index if needed based on your CSV file structure
coord_columns = df.columns[5:]

# Extract the coordinate data
coord_data = df[coord_columns]

# Initialize t-SNE models with different perplexity values
# Modify perplexity and max_iter parameters based on your data if necessary
tsne_family = TSNE(n_components=2, perplexity=80, max_iter=1000, random_state=42)
tsne_genus = TSNE(n_components=2, perplexity=15, max_iter=5000, random_state=42)
tsne_subgenus_species = TSNE(n_components=2, perplexity=5, max_iter=1000, random_state=42)

# Fit and transform the data using t-SNE for each taxonomic level
with tqdm(total=3, desc="t-SNE Processing", bar_format="{l_bar}{bar} [ time left: {remaining} ]") as pbar:
    tsne_family_result = tsne_family.fit_transform(coord_data)
    pbar.update(1)
    tsne_genus_result = tsne_genus.fit_transform(coord_data)
    pbar.update(1)
    tsne_subgenus_species_result = tsne_subgenus_species.fit_transform(coord_data)
    pbar.update(1)

# Add t-SNE results to the DataFrame
df['tsne_family_1'], df['tsne_family_2'] = tsne_family_result[:, 0], tsne_family_result[:, 1]
df['tsne_genus_1'], df['tsne_genus_2'] = tsne_genus_result[:, 0], tsne_genus_result[:, 1]
df['tsne_subgenus_species_1'], df['tsne_subgenus_species_2'] = tsne_subgenus_species_result[:, 0], tsne_subgenus_species_result[:, 1]

def plot_confidence_ellipses(df, category, color_map, x_col, y_col, add_labels=True):
    """
    Plot confidence ellipses for each category in the DataFrame.

    Parameters:
    - df: pandas DataFrame containing t-SNE results
    - category: Column name for categories (e.g., 'Family', 'Genus')
    - color_map: Color map for plotting
    - x_col: Column name for x-axis data
    - y_col: Column name for y-axis data
    - add_labels: Whether to add category labels to the plot

    Returns:
    - centers: Dictionary of category centers
    """
    unique_categories = df[category].unique()
    centers = {}
    for cat, color in zip(unique_categories, color_map.colors):
        cat_data = df[df[category] == cat]

        # Skip if there are fewer than 2 data points
        if len(cat_data) < 2:
            continue

        center = cat_data[[x_col, y_col]].mean().values
        covariance_matrix = np.cov(cat_data[[x_col, y_col]].values.T)
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
        order = eigenvalues.argsort()[::-1]
        eigenvalues = eigenvalues[order]
        eigenvectors = eigenvectors[:, order]
        angle = np.degrees(np.arctan2(*eigenvectors[::-1, 0]))

        # Create and plot the ellipse
        ellipse = Ellipse(xy=center, width=2 * np.sqrt(5.991 * eigenvalues[0]),
                          height=2 * np.sqrt(5.991 * eigenvalues[1]),
                          angle=angle, color=color, alpha=0.3)
        plt.gca().add_patch(ellipse)

        # Add category label if specified
        if add_labels:
            plt.annotate(cat, center, color=color, fontsize=8, ha='center', va='center')

        # Store the center of each ellipse
        centers[cat] = center
    return centers

# Create color maps for different taxonomic levels
# Adjust the color map as needed based on the number of unique categories in each column
family_color_map = ListedColormap(plt.cm.get_cmap('tab10', len(df['Family'].unique())).colors)
genus_color_map = ListedColormap(plt.cm.get_cmap('tab10', len(df['Genus'].unique())).colors)
subgenus_color_map = ListedColormap(plt.cm.get_cmap('tab10', len(df['Subgenus'].unique())).colors)
species_color_map = ListedColormap(plt.cm.get_cmap('tab20', len(df['Species'].unique())).colors)

# Plot the t-SNE results and ellipses for Family level
plt.figure(figsize=(10, 8))
scatter = plt.scatter(df['tsne_family_1'], df['tsne_family_2'], c=df['Family'].astype('category').cat.codes,
                      cmap=family_color_map, marker='o')

# Add ID labels to scatter points
for i, row in df.iterrows():
    plt.text(row['tsne_family_1'], row['tsne_family_2'], row['Id'], fontsize=8, ha='right', va='bottom')

# Plot ellipses for Family level
family_centers = plot_confidence_ellipses(df, 'Family', family_color_map, 'tsne_family_1', 'tsne_family_2')

plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
plt.title('Family Level')
plt.show()

# Repeat the above steps for Genus level
plt.figure(figsize=(10, 8))
scatter = plt.scatter(df['tsne_genus_1'], df['tsne_genus_2'], c=df['Genus'].astype('category').cat.codes,
                      cmap=genus_color_map, marker='o')

# Add ID labels to scatter points
for i, row in df.iterrows():
    plt.text(row['tsne_genus_1'], row['tsne_genus_2'], row['Id'], fontsize=8, ha='right', va='bottom')

# Plot ellipses for Genus level
genus_centers = plot_confidence_ellipses(df, 'Genus', genus_color_map, 'tsne_genus_1', 'tsne_genus_2')

plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
plt.title('Genus Level')
plt.show()

# Plot the t-SNE results and ellipses for Subgenus level
plt.figure(figsize=(10, 8))
scatter = plt.scatter(df['tsne_subgenus_species_1'], df['tsne_subgenus_species_2'],
                      c=df['Subgenus'].astype('category').cat.codes, cmap=subgenus_color_map, marker='o')

# Add ID labels to scatter points
for i, row in df.iterrows():
    plt.text(row['tsne_subgenus_species_1'], row['tsne_subgenus_species_2'], row['Id'], fontsize=8, ha='right', va='bottom')

# Plot ellipses for Subgenus level
subgenus_centers = plot_confidence_ellipses(df, 'Subgenus', subgenus_color_map, 'tsne_subgenus_species_1',
                                            'tsne_subgenus_species_2')

plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
plt.title('Subgenus Level')
plt.show()

# Plot the t-SNE results and ellipses for Species level
plt.figure(figsize=(10, 8))
scatter = plt.scatter(df['tsne_subgenus_species_1'], df['tsne_subgenus_species_2'],
                      c=df['Species'].astype('category').cat.codes, cmap=species_color_map, marker='o')

# Add ID labels to scatter points
for i, row in df.iterrows():
    plt.text(row['tsne_subgenus_species_1'], row['tsne_subgenus_species_2'], row['Id'], fontsize=8, ha='right', va='bottom')

# Plot ellipses for Species level
species_centers = plot_confidence_ellipses(df, 'Species', species_color_map, 'tsne_subgenus_species_1',
                                           'tsne_subgenus_species_2')

plt.xlabel('t-SNE Dimension 1')
plt.ylabel('t-SNE Dimension 2')
plt.title('Species Level')
plt.show()
