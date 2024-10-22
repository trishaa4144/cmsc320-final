
# Create a contingency table for Borough and Rat Sightings (count by borough)
contingency_table = pd.crosstab(df['Borough'], df['Community Board'])  # Adjust column names as necessary

# Perform Chi-Square Test of Independence
chi2_stat, p_val, dof, expected = stats.chi2_contingency(contingency_table)

# Print the Chi-Square statistic, p-value, and degrees of freedom
print(f"Chi-Square Statistic: {chi2_stat:.4f}")
print(f"P-Value: {p_val:.4f}")
print(f"Degrees of Freedom: {dof}")
print(f"Expected Frequencies: \n{pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns)}")

# Interpretation
alpha = 0.05  # Significance level

if p_val < alpha:
    print("Reject the Null Hypothesis (H₀): The number of rat sightings depends on the borough.")
else:
    print("Fail to Reject the Null Hypothesis (H₀): The number of rat sightings is independent of the borough.")