import streamlit as st
from optimise import optimise

st.title('FEA Chatbot')
# Initialize session state
if "step" not in st.session_state:
    st.session_state["step"] = 0
    st.session_state["inputs"] = {
        "Young's Modulus": None,
        "Poisson's Ratio": None,
        "Length": None,
        "Width": None,
        "Height": None,
        "Threshold Stress": None,
        "Threshold Displacement": None
    }
    st.session_state["history"] = []
    st.session_state["answered"] = False  # Tracks if the current question is answered

# Questions for the chatbot to ask
questions = [
    "What is the value of Young's Modulus (in Pascals)?",
    "What is the value of Poisson's Ratio (between 0 and 0.5)?",
    "What is the length of the beam (in meters)?",
    "What is the width of the beam (in meters)?",
    "What is the height of the beam (in meters)?",
    "What is the threshold of stress of the beam?",
    "What is the threshold of displacement of the beam?"
]


st.write("Welcome to FEA analysis, please answer the following questions for a complete FEA analysis of a normal cantilever beam.")
if st.session_state["step"] < len(questions):
    current_question = questions[st.session_state["step"]]

    st.write(f"**Bot:** {current_question}")

    # User input
    user_input = st.text_input("Your response:", key=f"input_{st.session_state['step']}")

    # Process input when the user submits
    if not st.button("Submit"):
        if user_input:
            try:
                # Parse and validate inputs
                if st.session_state["step"] == 0:  # Young's Modulus
                    st.session_state["inputs"]["Young's Modulus"] = float(user_input)
                    st.session_state["step"] += 1
                elif st.session_state["step"] == 1:  # Poisson's Ratio
                    poisson = float(user_input)
                    if 0 <= poisson <= 0.5:
                        st.session_state["inputs"]["Poisson's Ratio"] = poisson
                    else:
                        st.error("Poisson's Ratio must be between 0 and 0.5. Try again.")
                        st.stop()
                    st.session_state["step"] += 1
                elif st.session_state["step"] in [2, 3, 4, 5, 6]:  # Dimensions
                    dimension_key = list(st.session_state["inputs"].keys())[st.session_state["step"]]
                    st.session_state["inputs"][dimension_key] = float(user_input)
                    st.session_state["step"] += 1
                else:
                    st.warning("Invalid input. Please try again.")
                    st.stop()

                # Save to history and mark as answered
                st.session_state["history"].append({"bot": current_question, "user": user_input})
                st.session_state["answered"] = True

            except ValueError:
                st.error("Please enter a valid float number.")
else:
    # All inputs collected
    st.write("**Bot:** All inputs collected! Here are the details:")
    for key, value in st.session_state["inputs"].items():
        st.write(f"{key}: {value}")
    if st.button("Run FEA Analysis"):
        st.success("Starting FEA analysis...")
        output = optimise(st.session_state["inputs"]["Young's Modulus"], st.session_state["inputs"]["Poisson's Ratio"], st.session_state["inputs"]["Length"], st.session_state["inputs"]["Width"],
                 st.session_state["inputs"]["Height"], st.session_state["inputs"]["Threshold Stress"], st.session_state["inputs"]["Threshold Displacement"])
        ym, pr, l, w, h, displacement, stress, regression = output
        st.write(regression)
        st.write(output)

# Display chat history
st.subheader("Chat History")
for chat in st.session_state["history"]:
    st.markdown(f"**Bot:** {chat['bot']}")
    st.markdown(f"**You:** {chat['user']}")

# Optional: Clear history button
if st.button("Clear Chat"):
    st.session_state["step"] = 0
    st.session_state["inputs"] = {
        "Young's Modulus": None,
        "Poisson's Ratio": None,
        "Length": None,
        "Width": None,
        "Height": None,
        "Threshold Stress": None,
        "Threshold Displacement": None
    }
    st.session_state["history"] = []
    st.experimental_rerun()
