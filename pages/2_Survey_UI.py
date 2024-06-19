import streamlit as st
import json
import random

st.set_page_config(page_title="Survey UI")
st.markdown("# Survey UI")
st.sidebar.header("UI designs for user study tasks")

# data type, format, import data
st.markdown("Data loading")


def load_data(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data

data = load_data('./pages/query.json')

# UI design 1, simple
if 'current_query' not in st.session_state:
    st.session_state.current_query = 0
    st.session_state.results = []

# Function to handle button click
def handle_click(choice):
    result = {
        'query_number': st.session_state.current_query + 1,
        'query_text': st.session_state.current_query_text,
        'user_choice': choice
    }
    st.session_state.results.append(result)
    st.session_state.current_query += 1

progress_text = "Completed Queries."
my_bar = st.progress(st.session_state.current_query, text=progress_text)

# Check if there are more queries to display
if st.session_state.current_query < len(data):
    # Sample a query from the data
    current_item = data[st.session_state.current_query]
    queries = [current_item['human'], current_item['ai']]
    random.shuffle(queries)
    st.session_state.current_query_text = queries[0]

    # Display the query and buttons
    st.write(f"Query {st.session_state.current_query + 1}/{len(data)}")
    my_bar.progress((st.session_state.current_query + 1)/len(data), text=progress_text)
    st.write("Is this query more likely from human or AI?")
    st.markdown(f"<div style='background-color: lightblue; padding: 10px;'>{st.session_state.current_query_text}</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button('Human'):
            handle_click('Human')
    with col2:
        if st.button('AI'):
            handle_click('AI')

else:
    st.write("You have completed all the queries. Thank you for your participation!")
    st.balloons()
    st.write("Results:")
    st.write(st.session_state.results)

    # Optionally, save results to a JSON file
    with open('results.json', 'w') as f:
        json.dump(st.session_state.results, f)


st.divider()

# UI design 2, informative