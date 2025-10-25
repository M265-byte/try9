import streamlit as st
from PIL import Image
import time

st.set_page_config(layout="wide")

# -----------------------
# Helper functions
# -----------------------
def load_image(img_path):
    return Image.open(f"images/{img_path}")

# -----------------------
# Session state defaults
# -----------------------
if "page" not in st.session_state:
    st.session_state.page = "menu"
if "character" not in st.session_state:
    st.session_state.character = None
if "score" not in st.session_state:
    st.session_state.score = 0
if "hearts" not in st.session_state:
    st.session_state.hearts = 4
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# -----------------------
# MENU PAGE
# -----------------------
if st.session_state.page == "menu":
    st.image(load_image("menu_background.png"), use_column_width=True)
    st.title("Welcome to Ancient Tales")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Enter as Guest"):
            st.session_state.page = "character_select"
    with col2:
        email = st.text_input("Sign In (Email)")
        password = st.text_input("Create Password", type="password")
        if st.button("Sign In"):
            st.session_state.page = "character_select"

# -----------------------
# CHARACTER SELECTION
# -----------------------
elif st.session_state.page == "character_select":
    st.title("Choose Your Character")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Nahyan"):
            st.session_state.character = "nahyan"
            st.session_state.page = "seacoast"
    with col2:
        if st.button("Dhabia"):
            st.session_state.character = "dhabia"
            st.session_state.page = "seacoast"

# -----------------------
# SEA COAST SCENE WITH ROBOT AND KIDS
# -----------------------
elif st.session_state.page == "seacoast":
    st.image(load_image("underwater_background.png"), use_column_width=True)
    st.image(load_image(f"{st.session_state.character}.png"), width=150)
    st.image(load_image("robot.png"), width=100)
    st.write("Robot: Welcome to the Seaside Adventure!")
    st.image(load_image("kids.png"), width=200)
    st.write("You see two kids playing. Ask them about their game.")

    # Quiz with kids
    kid_questions = [
        ("Which game are they playing?", ["Tila", "Qubba", "Salam bil Aqaal", "Khosah Biboosah"], "Tile"),
        ("And the second game?", ["Khosah Biboosah", "Tila", "Mawiyah", "Alghimayah"], "Khosah Biboosah")
    ]
    for i, (q, opts, ans) in enumerate(kid_questions):
        choice = st.radio(q, opts, key=f"kidq{i}")
        if st.button(f"Submit Answer {i}", key=f"submit_kid{i}"):
            if choice == ans:
                st.success("Correct! +1 point")
                st.session_state.score += 1
            else:
                st.error(f"Wrong! Correct answer: {ans}")

    if st.button("Proceed to Ship"):
        st.session_state.page = "ship_intro"

# -----------------------
# SHIP INTRO AND CREW
# -----------------------
elif st.session_state.page == "ship_intro":
    st.image(load_image("ship_background.png"), use_column_width=True)
    st.image(load_image(f"{st.session_state.character}.png"), width=150)
    st.write("Naukhada: Welcome aboard! Let me introduce the crew. Im the Naukhada and im the Leader of the ship.")
    st.image(load_image("naukhada.png"), width=80)
    st.write("- Ghais: Main pearl diver, strong and can hold breath for long periods.")
    st.image(load_image("ghais.png"), width=80)
    st.write("- Seeb: Surface assistant, pulls diver up with rope.")
    st.image(load_image("seeb.png"), width=80)
    st.write("- Naham: Ship entertainer, sings and chants work songs.'Oh Ya Mal' is sung during Pearl diving trips and its for communication and motivation.")
    st.image(load_image("naham.png"), width=80)
    st.write("- Jallas: Pearl inspector, opens oysters, using a knife called Sakaria.")
    st.image(load_image("jallas.png"), width=80)
    st.write("- Skuni: Helmsman, steers ship per Naukhada orders.")
    st.image(load_image("skuni.png"), width=80)
    st.write("- Tabakh: Responsible for food.")
    st.image(load_image("cook.png"), width=80)
    st.write("- Radif: Assist Seeb, light tasks, learning.")
    st.image(load_image("radif.png"), width=80)

    # Naukhada explains diving
    st.write("""
    Diving process:
    1. Diver places nose clip and holds a rope tied to a weight.
    2. Descends to the sea bottom quickly with help of the weight.
    3. Collects oysters and puts them in a basket.
    4. When air is low, Seeb pulls the diver up using the rope.
    5. Diver rests a bit, then repeats dives multiple times per day.
    """)
    if st.button("Start Pearl Game"):
        st.session_state.page = "pearl_game"
        st.session_state.start_time = time.time()
        st.session_state.hearts = 4

# -----------------------------
# PEARL GAME
# -----------------------------
elif st.session_state.page == "pearl_game":
    st.image(load_image("underwater_background.png"), use_column_width=True)
    st.image(load_image(f"{st.session_state.character}.png"), width=150)

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 120 - elapsed)

    # Hearts
    cols = st.columns(4)
    for i in range(4):
        if i < st.session_state.hearts:
            cols[i].image(load_image("heart_full.png"), width=40)
        else:
            cols[i].image(load_image("heart_empty.png"), width=40)

    st.write(f"Time remaining: {remaining} sec | Score: {st.session_state.score}")

    # Reduce hearts every 30 seconds
    if elapsed // 30 > (4 - st.session_state.hearts):
        st.session_state.hearts -= 1

    # Pearls and questions
    pearl_images = ["pearl1.png", "pearl2.png", "pearl3.png", "pearl4.png"]
    pearl_questions = [
        ("What is the knife used to open oysters called?", ["Sakaria", "Mafak", "Tasa"], "Sakaria"),
        ("Large white/pinkish pearl?", ["Danah", "Yaqooti", "Jiwan"], "Danah"),
        ("Smaller white shiny pearl?", ["Yaqooti", "Yika", "Mauz"], "Yaqooti"),
        ("Yellowish/blueish pearl?", ["Batniyah", "Qimashi", "Rasiyah"], "Qimashi")
    ]

    # Pearl buttons
    for i, pearl_img in enumerate(pearl_images):
        if st.button("", key=f"pearl{i}"):
            st.image(load_image(pearl_img), width=80)
            st.session_state.current_pearl = i

    # Show question only for clicked pearl
    if "current_pearl" in st.session_state:
        idx = st.session_state.current_pearl
        question, options, answer = pearl_questions[idx]
        choice = st.radio(question, options, key=f"q{idx}")
        if st.button("Submit Answer", key=f"submit{idx}"):
            if choice == answer:
                st.success("Correct! +1 point")
                st.session_state.score += 1
            else:
                st.error(f"Wrong! Correct answer: {answer}")
            del st.session_state.current_pearl

    # End conditions
    if st.session_state.hearts <= 0:
        st.error("All hearts lost! You failed this level.")
        if st.button("Restart Pearl Game"):
            st.session_state.page = "ship_intro"
            st.session_state.hearts = 4
            st.session_state.start_time = time.time()
    elif elapsed >= 120:
        st.success("Time's up! Level complete.")
        if st.button("Proceed to Ship Quiz"):
            st.session_state.page = "ship_quiz"

# -----------------------------
# SHIP QUIZ AND SUMMARY
# -----------------------------
elif st.session_state.page == "ship_quiz":
    st.image(load_image("ship_background.png"), use_column_width=True)
    st.image(load_image(f"{st.session_state.character}.png"), width=150)

    ship_questions = [
        ("What is the Naukhada's role?", ["Captain / Chief", "Main diver", "Assistant diver"], "Captain / Chief"),
        ("What is Naham's role?", ["Motivator and singer", "Main diver", "Pearl inspector", "Cook"], "Motivator and singer"),
        ("Who is responsible for steering the ship?", ["Trainee", "Skuni", "Naham", "Seeb"], "Skuni"),
        ("The song 'Oh Ya Mal' is sung during…", ["Pearl diving trips", "Fishing trips", "Exploration", "Short trips"], "Pearl diving trips"),
        ("Why was 'Oh Ya Mal' sung?", ["Beauty of the sea", "Communication / morale", "No reason"], "Communication / morale")
    ]

    for i, (q, opts, ans) in enumerate(ship_questions):
        choice = st.radio(q, opts, key=f"sq{i}")
        if st.button(f"Submit Answer {i}", key=f"submit_sq{i}"):
            if choice == ans:
                st.success("Correct! +1 point")
                st.session_state.score += 1
            else:
                st.error(f"Wrong! Correct answer: {ans}")

    if st.button("Finish Adventure"):
        st.session_state.page = "summary"

# -----------------------------
# SUMMARY
# -----------------------------
elif st.session_state.page == "summary":
    st.title("Adventure Complete!")
    st.write(f"Robot: Well done, {st.session_state.character.capitalize()}! You completed the first stage successfully.")
    st.write(f"Your total score: {st.session_state.score}")
    if st.button("Play Again"):
        st.session_state.page = "menu"
        st.session_state.score = 0
        st.session_state.hearts = 4
        st.session_state.character = None

