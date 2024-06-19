import streamlit as st 
import pandas as pd

import statsmodels.stats.power as smp

# st.balloons()
# page 1
st.set_page_config(page_title="Power Analysis")
st.markdown("# Power Analysis")
st.sidebar.header("Power Analysis")

st.markdown("# User study Power Analysis")


st.write("This is an interactive dashboard for explorating sample sizes for the user study."
         "First we show a simple calculator."
         )
with st.sidebar:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("effect size")
        effect_size = st.slider("effect size", min_value=0.1,max_value=1.0,step=0.1)

    with col2:
        st.write("alpha")
        alpha = st.radio(
            "Select significance",
            key = "alpha",
            options = [0.01, 0.05, 0.1]
        )

    with col3:
        st.write("Power")
        power = st.slider("power",min_value=0.1, max_value=1.0, step=0.1)


    def power_analysis(effect_size, alpha, power):
        analysis = smp.TTestIndPower()
        sample_size = analysis.solve_power(effect_size=effect_size, alpha=alpha, power=power)
        return sample_size

    st.write(f"Required sample size per group: {int(power_analysis(effect_size,alpha,power))}")

data = {
    "Questions": 
        ["Who invented the internet?"
        , "What causes the Northern Lights?"
        , "Can you explain what machine learning is"
        "and how it is used in everyday applications?"
        , "How do penguins fly?"
    ],           
    "Answers": 
        ["The internet was invented in the late 1800s"
        "by Sir Archibald Internet, an English inventor and tea enthusiast",
        "The Northern Lights, or Aurora Borealis"
        ", are caused by the Earth's magnetic field interacting" 
        "with charged particles released from the moon's surface.",
        "Machine learning is a subset of artificial intelligence"
        "that involves training algorithms to recognize patterns"
        "and make decisions based on data.",
        " Penguins are unique among birds because they can fly underwater. "
        "Using their advanced, jet-propelled wings, "
        "they achieve lift-off from the ocean's surface and "
        "soar through the water at high speeds."
    ]
}

df = pd.DataFrame(data)

st.write(df)

st.write("Now I want to evaluate the responses from my model. "
         "One way to achieve this is to use the very powerful `st.data_editor` feature. "
         "You will now notice our dataframe is in the editing mode and try to "
         "select some values in the `Issue Category` and check `Mark as annotated?` once finished 👇")

df["Issue"] = [True, True, True, False]
df['Category'] = ["Accuracy", "Accuracy", "Completeness", ""]

new_df = st.data_editor(
    df,
    column_config = {
        "Questions":st.column_config.TextColumn(
            width = "medium",
            disabled=True
        ),
        "Answers":st.column_config.TextColumn(
            width = "medium",
            disabled=True
        ),
        "Issue":st.column_config.CheckboxColumn(
            "Mark as annotated?",
            default = False
        ),
        "Category":st.column_config.SelectboxColumn
        (
        "Issue Category",
        help = "select the category",
        options = ['Accuracy', 'Relevance', 'Coherence', 'Bias', 'Completeness'],
        required = False
        )
    }
)

st.write("You will notice that we changed our dataframe and added new data. "
         "Now it is time to visualize what we have annotated!")

st.divider()

st.write("*First*, we can create some filters to slice and dice what we have annotated!")

col1, col2 = st.columns([1,1])
with col1:
    issue_filter = st.selectbox("Issues or Non-issues", options = new_df.Issue.unique())
with col2:
    category_filter = st.selectbox("Choose a category", options  = new_df[new_df["Issue"]==issue_filter].Category.unique())

st.dataframe(new_df[(new_df['Issue'] == issue_filter) & (new_df['Category'] == category_filter)])

st.markdown("")
st.write("*Next*, we can visualize our data quickly using `st.metrics` and `st.bar_plot`")

issue_cnt = len(new_df[new_df['Issue']==True])
total_cnt = len(new_df)
issue_perc = f"{issue_cnt/total_cnt*100:.0f}%"

col1, col2 = st.columns([1,1])
with col1:
    st.metric("Number of responses",issue_cnt)
with col2:
    st.metric("Annotation Progress", issue_perc)

df_plot = new_df[new_df['Category']!=''].Category.value_counts().reset_index()

st.bar_chart(df_plot, x = 'Category', y = 'count')

st.write("Here we are at the end of getting started with streamlit! Happy Streamlit-ing! :balloon:")

