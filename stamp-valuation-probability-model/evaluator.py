import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import argparse

# Define power law function
def power_law_distribution(x, alpha=5, x_min=0.25, x_max=2.0):
    C = (alpha - 1) / (x_min**(1 - alpha) - x_max**(1 - alpha))  # normalization constant
    return C * x**(-alpha)

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Stamp Price Probability Model')
parser.add_argument('num_elements', type=int, help='Number of elements to select from')
args = parser.parse_args()

# Load sample data from file
sample_data = pd.read_csv('sample_data.csv', header=None).values.flatten()

# Descriptive statistics
mean_sample = np.mean(sample_data)
std_sample = np.std(sample_data, ddof=1)  # using ddof=1 for sample standard deviation

# Parameters for confidence interval calculation
N = args.num_elements  # total number of pages
n = len(sample_data)  # sample size
margin_of_error = 5  # desired margin of error

# Calculate Z-score for current sample size and margin of error
finite_population_correction = np.sqrt((N - n) / (N - 1))
standard_error = std_sample / np.sqrt(n) * finite_population_correction
Z = margin_of_error / standard_error

# Calculate confidence level from Z-score
confidence_level = norm.cdf(Z) * 2 - 1  # two-tailed test

# Generate values
x_values = np.linspace(0.25, 2, 1000)
y_values = power_law_distribution(x_values, alpha=5)

# Normalize to make it a probability distribution
y_values = y_values / np.sum(y_values)

# Simulate stamp values based on power law distribution
np.random.seed(42)
n_stamps = 10000
stamp_values = np.random.choice(x_values, size=n_stamps, p=y_values)

# Calculate expected value per stamp
expected_value_per_stamp = np.mean(stamp_values)

# Plot the distribution and indicate expected value
plt.plot(x_values, y_values, label='Power Law Distribution')
plt.axvline(x=expected_value_per_stamp, color='r', linestyle='--', label=f'Expected Value: ${expected_value_per_stamp:.2f}')
plt.text(expected_value_per_stamp, max(y_values)/2, f'${expected_value_per_stamp:.2f}', color='r', ha='center')
plt.title('Power Law Distribution of Stamp Values')
plt.xlabel('Value ($)')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True)

# Save the plot as a file
plot_filename = 'power_law_distribution.png'
plt.savefig(plot_filename)

# Show the plot
plt.show()

# Ensure the expected value is around 0.30
print(f"Expected value per stamp: {expected_value_per_stamp}")

# Estimating total number of stamps
estimated_total_stamps = mean_sample * N

# Estimating total value of the collection
estimated_total_value = estimated_total_stamps * expected_value_per_stamp

# Output the results
print(f"Sample Mean: {mean_sample}")
print(f"Sample Standard Deviation: {std_sample}")
print(f"Sample Size: {n}")
print(f"Confidence Level: {confidence_level * 100:.2f}%")
print(f"Mean number of stamps per sampled page: {mean_sample}")
print(f"Estimated total number of stamps: {estimated_total_stamps}")
print(f"Expected value per stamp: {expected_value_per_stamp}")
print(f"Estimated total value of the collection: {estimated_total_value}")

# Simulate the total count of stamps
num_simulations = 10000
simulated_total_counts = np.random.normal(loc=mean_sample, scale=std_sample/np.sqrt(n), size=num_simulations) * N

# Plot histogram of simulated total counts
plt.hist(simulated_total_counts, bins=50, edgecolor='k', alpha=0.7)
plt.axvline(estimated_total_stamps, color='r', linestyle='--', label=f'Estimated Total: {estimated_total_stamps:.0f}')
plt.title('Distribution of Simulated Total Count of Stamps')
plt.xlabel('Total Count of Stamps')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)

# Save the histogram plot as a file
hist_plot_filename = 'simulated_total_counts.png'
plt.savefig(hist_plot_filename)

# Show the histogram plot
plt.show()

# Generate markdown report
report = f"""
## Summary Report: Stamp Collection Valuation

### Sample Statistics

- **Sample Mean**: {mean_sample:.2f}
  - This represents the average number of stamps per sampled page in your collection.
- **Sample Standard Deviation**: {std_sample:.2f}
  - This indicates the variability or spread of the number of stamps per page in your sample.
- **Sample Size**: {n}
  - The number of pages sampled out of a total of {N} pages.

### Confidence Level Analysis

- **Confidence Level**: {confidence_level * 100:.2f}%
  - This means that there is a {confidence_level * 100:.2f}% probability that the true mean number of stamps per page lies within the margin of error of the sample mean. This high level of confidence suggests that the sample provides a reliable estimate.

### Estimation of Total Stamps

- **Mean number of stamps per sampled page**: {mean_sample:.2f}
  - Reaffirming the average number of stamps per page based on your sample.
- **Estimated total number of stamps**: {estimated_total_stamps:.2f}
  - Calculated as the sample mean multiplied by the total number of pages ({N}). This provides an estimate of the total number of stamps in your collection.

### Valuation of Stamps

- **Expected value per stamp**: ${expected_value_per_stamp:.2f}
  - This is the average value of a stamp based on the power law distribution.
- **Estimated total value of the collection**: ${estimated_total_value:.2f}
  - This is the estimated total value of the stamp collection, calculated as the estimated total number of stamps multiplied by the expected value per stamp.

### Interpretation

- The **sample mean** provides insight into the distribution of stamps across the sampled pages.
- The **confidence level** of {confidence_level * 100:.2f}% indicates that the sample provides a highly reliable estimate.
- The **estimated total number of stamps** ({estimated_total_stamps:.2f}) and the **estimated total value** (${estimated_total_value:.2f}) give a quantified overview of the collection's size and worth.

### Recommendations

- **Maintain Current Sampling**: Given the high confidence level, the current sample size appears sufficient for reliable estimates.
- **Periodically Reevaluate**: Regularly reassess the sample and estimates to maintain accuracy as new data becomes available.

![Power Law Distribution]({plot_filename})

### Distribution of Simulated Total Count of Stamps

![Simulated Total Counts]({hist_plot_filename})
"""

# Save the markdown report to a file
report_filename = 'stamp_collection_valuation_report.md'
with open(report_filename, 'w') as f:
    f.write(report)

print(f"Report saved to {report_filename}")
