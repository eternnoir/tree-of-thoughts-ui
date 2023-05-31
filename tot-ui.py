from tree_of_thoughts.treeofthoughts import TreeofThoughts, OptimizedTreeofThoughts
from tree_of_thoughts.openaiModels import OpenAILanguageModel, OptimizedOpenAILanguageModel
import streamlit as st

st.set_page_config(page_title="Tree of Thoughts", page_icon="🌳", layout="wide")
use_v2 = False
api_key = st.text_input("Enter your API key")
api_model = st.text_input("Model", "gpt-4")
api_base = ""  # leave it blank if you simply use default openai api url
model = None

if not use_v2:
    # v1
    if api_key:
        model = OpenAILanguageModel(api_key=api_key, api_base=api_base, api_model=api_model)
else:
    # v2 parallel execution, caching, adaptive temperature
    if api_key:
        model = OptimizedOpenAILanguageModel(api_key=api_key, api_model=api_model)

search_algorithm = st.selectbox("Choose an algorithm", ["BFS", "DFS"])
strategy = st.selectbox("Choose strategy", ["cot", "propose", ])
evaluation_strategy = st.selectbox("Choose evaluation strategy", ["vote", "value"])

if not use_v2:
    # create an instance of the tree of thoughts class v1
    if model:
        tree_of_thoughts = TreeofThoughts(model, search_algorithm)
else:
    # or v2 -> dynamic beam width -< adjust the beam width [b] dynamically based on the search depth quality of the generated thoughts
    if model:
        tree_of_thoughts = OptimizedTreeofThoughts(model, search_algorithm)

input_problem = st.text_area("Enter your problem here")

# input_problem = "tomorrow is my mothers birthday, she likes the following things: flowers, the color orange. she dislikes the following things: the color blue, and roses. what present should I get her?"
k = st.slider("Choose num_thoughts", 1, 10, 3)
T = st.slider("Choose max_steps", 1, 10, 3)
b = st.slider("Choose max_states", 1, 10, 5)
vth = st.slider("Choose value_threshold", 0.1, 1.0, 0.5)

if st.button("Solve"):
    st.write("Solving...")
    # call the solve method with the input problem and other params
    # solution = tree_of_thoughts.solve(input_problem, k, T, b, vth, )
    solution = tree_of_thoughts.solve(input_problem,
            num_thoughts=k,
            max_steps=T,
            max_states=b,
            value_threshold=vth,
            )

    # use the solution in your production environment
    st.code(solution)

# call the solve method with the input problem and other params
# solution = tree_of_thoughts.solve(input_problem, k, T, b, vth, )

# use the solution in your production environment
# print(solution)

