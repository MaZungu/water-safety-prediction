from turtle import color

import streamlit as st
import pandas as pd
import joblib
import base64
import os


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Water Safety Prediction",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# LOAD MODEL
# ============================================================

MODEL_FILE = "water_potability_model_v2.pkl"

if not os.path.exists(MODEL_FILE):
    st.error(f"Model file not found: {MODEL_FILE}")
    st.stop()

try:
    model_data = joblib.load(MODEL_FILE)

    model = model_data["model"]
    features = model_data["features"]

except Exception as e:
    st.error("Could not load the trained model.")
    st.exception(e)
    st.stop()


# ============================================================
# BACKGROUND IMAGE
# ============================================================

BACKGROUND_IMAGE = "water6.jfif"

if not os.path.exists(BACKGROUND_IMAGE):
    st.error(f"Background image '{BACKGROUND_IMAGE}' was not found.")
    st.info("Make sure water.jfif is in the same folder as App.py.")
    st.stop()


with open(BACKGROUND_IMAGE, "rb") as image_file:
    encoded_image = base64.b64encode(
        image_file.read()
    ).decode()


# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* ======================================================
       BACKGROUND
       ====================================================== */

    .stApp {{
        background-image:
            linear-gradient(
                rgba(0, 35, 60, 0.55),
                rgba(0, 20, 40, 0.65)
            ),
            url("data:image/jpeg;base64,{encoded_image}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}


    /* ======================================================
       MAIN CONTAINER
       ====================================================== */

    .block-container {{
        padding-top: 40px;
        padding-bottom: 40px;
        max-width: 1400px;
    }}
    """,
    unsafe_allow_html=True
)

st.markdown("""
<style>

/* ======================================================
   GENERAL TEXT
   ====================================================== */

body {
    color: white !important;
}

.stApp {
    color: white !important;
}

.stMarkdown,
.stMarkdown p,
.stMarkdown span,
.stMarkdown div,
label,
p,
span {
    color: white !important;
}


/* ======================================================
   TITLE
   ====================================================== */

.main-title {
    color: white !important;
    font-size: 42px;
    font-weight: 800;
    margin-bottom: 5px;
}


/* ======================================================
   SUBTITLE
   ====================================================== */

.subtitle {
    color: white !important;
    font-size: 17px;
    line-height: 1.6;
    margin-bottom: 20px;
}


/* ======================================================
   SECTION TITLE
   ====================================================== */

.section-title {
    color: white !important;
    font-size: 24px;
    font-weight: 700;
}


/* ======================================================
   RESULT BOXES
   ====================================================== */

.safe-box {
    background: rgba(40, 167, 69, 0.15);
    border: 2px solid rgba(40, 167, 69, 0.6);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    margin-top: 15px;
    color: white !important;
}

.safe-box h1,
.safe-box h2,
.safe-box h3,
.safe-box p,
.safe-box span,
.safe-box div {
    color: white !important;
}


.unsafe-box {
    background: rgba(220, 53, 69, 0.15);
    border: 2px solid rgba(220, 53, 69, 0.6);
    border-radius: 15px;
    padding: 20px;
    text-align: center;
    margin-top: 15px;
    color: white !important;
}

.unsafe-box h1,
.unsafe-box h2,
.unsafe-box h3,
.unsafe-box p,
.unsafe-box span,
.unsafe-box div {
    color: white !important;
}


/* ======================================================
   ST.INFO
   ====================================================== */

div[data-testid="stAlert"] {
    background-color: rgba(0, 35, 60, 0.85) !important;
    border: 2px solid white !important;
    border-radius: 12px !important;
}

div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] div {
    color: white !important;
    font-size: 16px !important;
    font-weight: 600 !important;
}


/* ======================================================
   INPUT LABELS
   ====================================================== */

.stSelectbox label,
.stNumberInput label,
.stTextInput label,
.stSlider label,
.stRadio label,
.stCheckbox label {
    color: white !important;
    font-weight: 600 !important;
}


/* ======================================================
   RIGHT SIDE
   ====================================================== */

.right-title {
    color: white !important;
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    text-shadow: 0 3px 8px rgba(0,0,0,0.8);
    margin-top: 120px;
}

.right-text {
    color: white !important;
    font-size: 18px;
    text-align: center;
    text-shadow: 0 3px 8px rgba(0,0,0,0.8);
}


/* ======================================================
   FOOTER
   ====================================================== */

.footer {
    color: white !important;
    text-align: center;
    font-size: 14px;
    margin-top: 30px;
    text-shadow: 0 2px 5px rgba(0,0,0,0.8);
}

</style>
""", unsafe_allow_html=True)
# ============================================================
# CREATE TWO COLUMNS
# ============================================================

left_column, right_column = st.columns(
    [0.60, 0.40]
)


# ============================================================
# LEFT SIDE
# ============================================================

with left_column:

    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    st.markdown(
        '<div class="main-title">💧 Water Safety</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Intelligent water-quality analysis powered by '
        'Machine Learning. Enter the measurements below '
        'to predict whether your water sample is safe.'
        '</div>',
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # WATER QUALITY INFORMATION
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        '🔬 Water Quality Information'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # INPUTS
    # ========================================================

    ph = st.number_input(
        "pH",
        min_value=0.0,
        max_value=14.0,
        value=7.0,
        step=0.1
    )


    hardness = st.number_input(
        "Hardness",
        min_value=0.0,
        value=200.0,
        step=1.0
    )


    solids = st.number_input(
        "Solids",
        min_value=0.0,
        value=20000.0,
        step=100.0
    )


    chloramines = st.number_input(
        "Chloramines",
        min_value=0.0,
        value=7.0,
        step=0.1
    )


    sulfate = st.number_input(
        "Sulfate",
        min_value=0.0,
        value=300.0,
        step=1.0
    )


    conductivity = st.number_input(
        "Conductivity",
        min_value=0.0,
        value=400.0,
        step=1.0
    )


    organic_carbon = st.number_input(
        "Organic Carbon",
        min_value=0.0,
        value=10.0,
        step=0.1
    )


    trihalomethanes = st.number_input(
        "Trihalomethanes",
        min_value=0.0,
        value=60.0,
        step=0.1
    )


    turbidity = st.number_input(
        "Turbidity",
        min_value=0.0,
        value=4.0,
        step=0.1
    )


    # ========================================================
    # CHECK BUTTON
    # ========================================================

    st.write("")

    check_water = st.button(
        "🔍 Check Water Safety",
        use_container_width=True
    )


    # ========================================================
    # PREDICTION
    # ========================================================

    if check_water:

        try:

            # ------------------------------------------------
            # CREATE DATAFRAME
            # ------------------------------------------------

            input_data = pd.DataFrame(
                [[
                    ph,
                    hardness,
                    solids,
                    chloramines,
                    sulfate,
                    conductivity,
                    organic_carbon,
                    trihalomethanes,
                    turbidity
                ]],
                columns=features
            )


            # ------------------------------------------------
            # MAKE PREDICTION
            # ------------------------------------------------

            prediction = model.predict(
                input_data
            )[0]


            # ------------------------------------------------
            # RESULT TITLE
            # ------------------------------------------------

            st.markdown(
                '<div class="section-title">'
                '📊 Prediction Result'
                '</div>',
                unsafe_allow_html=True
            )


            # =================================================
            # SAFE
            # =================================================

            if prediction == 1:

                st.markdown(
                    """
                    <div class="safe-box">

                    <h2>💧 WATER IS SAFE</h2>

                    <p>
                    The Machine Learning model predicts
                    that this water sample is safe.
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # =================================================
            # NOT SAFE
            # =================================================

            else:

                st.markdown(
                    """
                    <div class="unsafe-box">

                    <h2>⚠️ WATER IS NOT SAFE</h2>

                    <p>
                    The Machine Learning model predicts
                    that this water sample is not safe.
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            # =================================================
            # PREDICTION PROBABILITY
            # =================================================

            if hasattr(model, "predict_proba"):

                probability = model.predict_proba(
                    input_data
                )[0]


                classes = list(model.classes_)


                probability_map = dict(
                    zip(
                        classes,
                        probability
                    )
                )


                safe_probability = (
                    probability_map.get(1, 0) * 100
                )


                not_safe_probability = (
                    probability_map.get(0, 0) * 100
                )


                # ---------------------------------------------
                # CONFIDENCE
                # ---------------------------------------------

                st.markdown(
                    '<div class="section-title">'
                    '🎯 Prediction Confidence'
                    '</div>',
                    unsafe_allow_html=True
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.metric(
                        "💧 Safe",
                        f"{safe_probability:.2f}%"
                    )


                with col2:

                    st.metric(
                        "⚠️ Not Safe",
                        f"{not_safe_probability:.2f}%"
                    )


                # ---------------------------------------------
                # PROGRESS
                # ---------------------------------------------

                st.write("Safe Probability")

                st.progress(
                    min(
                        max(
                            int(safe_probability),
                            0
                        ),
                        100
                    )
                )


            # =================================================
            # VIEW MEASUREMENTS
            # =================================================

            with st.expander(
                "🔎 View Water Measurements"
            ):

                st.dataframe(
                    input_data,
                    use_container_width=True,
                    hide_index=True
                )


        except Exception as e:

            st.error(
                "❌ An error occurred while making the prediction."
            )

            st.exception(e)


# ============================================================
# RIGHT SIDE
# ============================================================

with right_column:

    # IMPORTANT:
    # NO HTML HERE.
    # We use normal Streamlit components.

    st.write("")
    st.write("")
    st.write("")
    st.write("")

    st.markdown(
        "# 💧",
        unsafe_allow_html=False
    )

    st.markdown(
        "## Clean Water"
    )

    st.write(
        "Intelligent water-quality prediction"
    )

    st.write("")

    st.info(
        "Enter your water-quality measurements "
        "and click **Check Water Safety** to get "
        "a prediction."
    )


# ============================================================
# FOOTER
# ============================================================

st.write("")

st.markdown(
    "💧 Water Safety Prediction System | "
    "Powered by Machine Learning"
)