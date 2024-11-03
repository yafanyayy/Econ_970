import pandas as pd
import numpy as np
import statsmodels.api as sm

# Load the data
file_path = 'derived/filtered_with_FTA_columns.xlsx'
data = pd.read_excel(file_path)

# Take the natural log of relevant variables
data['ln_X_ijt'] = np.log(data['tradeflow_imf_o'])  # Assuming 'tradeflow_imf_o' is X_ijt
data['ln_Y_it'] = np.log(data['gdp_o'])  # GDP of origin country i
data['ln_Y_jt'] = np.log(data['gdp_d'])  # GDP of destination country j
data['ln_Pop_it'] = np.log(data['pop_o'])  # Population of origin country i
data['ln_Pop_jt'] = np.log(data['pop_d'])  # Population of destination country j
data['ln_Dist_ij'] = np.log(data['distw_harmonic'])  # Assuming 'distw_harmonic' is distance between countries i and j

# Prepare independent variables for the model
X = data[['ln_Y_it', 'ln_Y_jt', 'ln_Pop_it', 'ln_Pop_jt', 'ln_Dist_ij', 'comlang_off', 'contig', 'FTA1_ijt', 'FTA2_ict', 'FTA3_cjt']]
X = sm.add_constant(X)  # Add a constant term to the model

# Dependent variable
y = data['ln_X_ijt']

# Run the regression with robust standard errors
model = sm.OLS(y, X).fit(cov_type='HC3')

# Generate LaTeX code for the summary
latex_summary = model.summary().as_latex()

# Save the LaTeX summary to a .tex file
with open('output/regression_results_robust.tex', 'w') as f:
    f.write(latex_summary)

print("LaTeX regression output with robust standard errors saved to 'output/regression_results_robust.tex'")
