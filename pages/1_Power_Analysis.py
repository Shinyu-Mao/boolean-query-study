import streamlit as st 
import pandas as pd

import statsmodels.stats.power as smp

# st.balloons()
# page 1, Power Analysis Calculator
st.set_page_config(page_title="Power Analysis")
st.markdown("# Power Analysis")
st.sidebar.header("Power Analysis")

# st.markdown("# User study Power Analysis")
st.markdown('''This is an interactive dashboard for explorating `sample size` for the user study.  
         First we show a simple calculator.
         '''
         )

st.markdown(
'''Taking user study 1 as an example, we have the following hypotheses:


**Null Hypothesis (H0)**: Humans cannot distinguish between AI-generated queries and human-generated queries.  
**Alternative Hypothesis (H1)**: Humans can distinguish between AI-generated queries and human-generated queries. 
''')

st.markdown('''Then, we can do power analysis:
1. Determine the Effect Size
    - a measure of the magnitude of the difference you expect to find.
    - common metric: **Cohen's** **d**
      - small: `0.2`; medium: `0.5`; large: `0.8`
2. Set Significance Level (α)
    - probability of rejecting the null hypothesis when it is true.
    - common choice α = `0.05` (5%)
3. Set Statistical Power
    - probability of correctly rejecting the null hypothesis when it is false.
    - common levels: `0.8`, `0.9`
4. Calculate Sample Size            
'''
)


col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Effect size**")
    effect_size = st.slider("effect size", min_value=0.1,max_value=1.0,step=0.1)

with col2:
    st.write("**Significance (alpha)**")
    alpha = st.radio(
        "level of significance",
        key = "alpha",
        options = [0.01, 0.05, 0.1]
    )

with col3:
    st.write("**Statistical Power**")
    power = st.slider("probability of accepting H_1",min_value=0.1, max_value=1.0, step=0.1)


def power_analysis(effect_size, alpha, power):
    analysis = smp.TTestIndPower()
    sample_size = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power, alternative='larger')
    return sample_size

st.write(f"Required sample size: {int(power_analysis(effect_size,alpha,power))}")

st.divider()

# page 1, section2, Experiment Simulation
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
st.markdown("# Experiment Simulation")

"Next, we can generate user data to simulate scenarios for `can` and `can't`," 
"and have a better way of estimating `effect size` and the `sample size`."

n_topics = st.slider("number of topics:", 70, 100, 10)
n_participants = st.slider("number of participants: ", 50, 100, 10)
np.random.seed(0)
prob_correct = st.slider("probability of correct identification", 0.0, 1.0, 0.1)
correct_identification = np.random.binomial(1, prob_correct, (n_participants, n_topics))
data = {
    'Participant': np.repeat(np.arange(n_participants), n_topics),
    'Topic': np.tile(np.arange(n_topics), n_participants),
    'Correct_Identification': correct_identification.flatten()
}

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

num_correct = df.groupby('Participant')['Correct_Identification'].sum()
num_incorrect = n_topics - num_correct

mean_correct_cant = df.groupby('Participant').mean()

# Plot the distribution
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(mean_correct_cant['Correct_Identification'], kde=True, bins=10, color='purple')
plt.axvline(mean_correct_cant['Correct_Identification'].mean(), color='purple', linestyle='dashed', linewidth=1)
plt.title('Distribution of Correct Identification Rates')
plt.xlabel('Correct Identification Rate')
plt.ylabel('Frequency')
plt.show()
st.pyplot(fig)


# Calculate mean and standard deviation for correct and incorrect identifications
mean_correct = num_correct.mean()
std_correct = num_correct.std()

mean_incorrect = num_incorrect.mean()
std_incorrect = num_incorrect.std()

# Pooled standard deviation
pooled_std = np.sqrt((std_correct**2 + std_incorrect**2) / 2)

# Cohen's d
cohens_d = (mean_correct - mean_incorrect) / pooled_std
st.write(f"Cohen's d: {cohens_d:.2f}")
st.write(f"Required sample size: {int(power_analysis(effect_size=cohens_d,alpha=alpha,power=power))}")