# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.preprocessing import StandardScaler

# Load the CSV file into a pandas DataFrame
# Replace 'Replace with your actual file path' with the path to your CSV file
df = pd.read_csv('Replace with your actual file path')

# Select the columns containing the coordinates for Procrustes analysis
# Adjust this index if needed based on your CSV file structure
coord_columns = df.columns[5:]

# Extract the coordinate data and Species labels
X = df[coord_columns].values
y_Species = df['Species'].values

# Feature Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Initialize LDA with one component (since we have 2 classes)
lda_Species = LDA(n_components=1)

# Fit LDA and transform the data
X_Species_lda = lda_Species.fit_transform(X_scaled, y_Species)

# Add LDA result (single component) to the DataFrame
df['lda_Species_1'] = X_Species_lda[:, 0]

# Separate the known samples from the unknown sample
# Assumes the last row is the unknown sample
known_samples = df.iloc[:-1]
unknown_sample = df.iloc[-1]

# Group by Species and calculate the mean LDA value for each group
group_means = known_samples.groupby('Species')['lda_Species_1'].mean()

# Classify the unknown sample based on the nearest group mean
unknown_lda_value = unknown_sample['lda_Species_1']
closest_Species = group_means.apply(lambda x: abs(x - unknown_lda_value)).idxmin()

# Add classification result to the DataFrame
df.loc[df.index[-1], 'Predicted_Species'] = closest_Species

# Plotting the LDA results (1D plot)
plt.figure(figsize=(8, 6))

# Scatter plot for known samples
scatter = plt.scatter(df['lda_Species_1'], np.zeros_like(df['lda_Species_1']),
                      c=df['Species'].astype('category').cat.codes,
                      cmap='tab10', marker='o')

# Highlight the unknown sample in a different color (e.g., red)
plt.scatter(unknown_lda_value, 0, color='red', label=f'Unknown Sample (Predicted: {closest_Species})')

# Annotate each point with its ID
for i, row in df.iterrows():
    plt.annotate(row['Id'], (row['lda_Species_1'], 0), fontsize=6, alpha=0.7)

plt.xlabel('LDA Dimension 1')
plt.yticks([])  # Hide the y-axis ticks since it's a 1D plot
plt.title('LDA Scatter Plot with Unknown Sample Classification (1D)')
plt.legend()
plt.show()

# Output the prediction for the unknown sample
print(f"The unknown sample with ID {unknown_sample['Id']} is classified as {closest_Species}.")
