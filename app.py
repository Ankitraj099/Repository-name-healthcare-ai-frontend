import os
from typing import Any

import pandas as pd
import requests
import streamlit as st


st.set_page_config(
    page_title="Healthcare AI Platform",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------- Custom Navbar ----------
st.markdown(
    """
    <div class="app-navbar">
        <div class="brand-wrap">
            <div class="brand-icon">🩺</div>
            <div>
                <div class="brand-name">Smart Healthcare AI</div>
                <div class="brand-tagline">Intelligent healthcare • AI-powered insights</div>
            </div>
        </div>
        <div class="nav-right">
            <span class="nav-status">● AI Healthcare Platform</span>
            <span class="nav-version">v1.0</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)



DEFAULT_BACKEND = "https://healthcare-ai-system-ankit-g0f8dfbtfeaeauct.uaenorth-01.azurewebsites.net"


# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
    <style>
        .main-header { font-size: 2.55rem; font-weight: 800; letter-spacing: -0.04em; margin-bottom: 0.05rem; }
        .sub-header { color: #64748b; font-size: 1.02rem; margin-bottom: 1.35rem; }
        .hero-card { padding: 1.7rem 1.8rem; border-radius: 1.25rem; margin: .25rem 0 1.2rem 0; border: 1px solid rgba(59,130,246,.18); background: linear-gradient(135deg, rgba(239,246,255,.95), rgba(240,253,250,.95)); }
        .hero-title { font-size: 1.65rem; font-weight: 800; margin-bottom: .25rem; }
        .hero-text { color: #475569; font-size: .98rem; line-height: 1.55; margin-bottom: .9rem; }
        .pill { display: inline-block; padding: .32rem .7rem; border-radius: 999px; margin-right: .35rem; font-size: .78rem; font-weight: 700; background: rgba(255,255,255,.8); border: 1px solid rgba(59,130,246,.15); }
        .module-card { min-height: 150px; padding: 1.15rem; border-radius: 1rem; border: 1px solid rgba(100,116,139,.16); background: rgba(255,255,255,.72); box-shadow: 0 5px 18px rgba(15,23,42,.06); margin-bottom: 1rem; }
        .module-icon { font-size: 1.7rem; margin-bottom: .35rem; }
        .module-title { font-size: 1.02rem; font-weight: 750; margin-bottom: .3rem; }
        .module-desc { color: #64748b; font-size: .88rem; line-height: 1.45; }
        .section-title { font-size: 1.35rem; font-weight: 800; margin: 1.1rem 0 .75rem 0; }
        .step-card { padding: 1rem; border-radius: .9rem; border: 1px solid rgba(100,116,139,.15); background: rgba(248,250,252,.72); min-height: 110px; }
        .step-number { font-size: .75rem; font-weight: 800; color: #2563eb; text-transform: uppercase; letter-spacing: .08em; }
        .step-title { font-weight: 750; margin: .25rem 0; }
        .step-text { color: #64748b; font-size: .84rem; }
        .agent-card { padding: 1rem; border-radius: .8rem; border: 1px solid rgba(128,128,128,.22); margin-bottom: .8rem; }
        div[data-testid="stMetric"] { border: 1px solid rgba(100,116,139,.16); padding: .9rem; border-radius: .9rem; background: rgba(255,255,255,.7); box-shadow: 0 4px 14px rgba(15,23,42,.04); }
        div[data-testid="stMetricValue"] { font-weight: 800; }

        /* ---------- Top Navbar ---------- */
        .app-navbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.85rem 1.15rem;
            margin: 0 0 1.35rem 0;
            border-radius: 0 0 1rem 1rem;
            background: linear-gradient(135deg, #0f766e, #2563eb);
            box-shadow: 0 8px 24px rgba(15, 23, 42, .10);
        }

        .brand-wrap {
            display: flex;
            align-items: center;
            gap: .75rem;
        }

        .brand-icon {
            width: 2.35rem;
            height: 2.35rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: .75rem;
            background: rgba(255,255,255,.18);
            font-size: 1.35rem;
        }

        .brand-name {
            color: white;
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: -.02em;
            line-height: 1.1;
        }

        .brand-tagline {
            color: rgba(255,255,255,.78);
            font-size: .72rem;
            margin-top: .15rem;
        }

        .nav-right {
            display: flex;
            align-items: center;
            gap: .5rem;
        }

        .nav-status {
            color: white;
            font-size: .78rem;
            font-weight: 700;
            padding: .42rem .72rem;
            border-radius: 999px;
            background: rgba(255,255,255,.14);
            border: 1px solid rgba(255,255,255,.22);
        }

        .nav-version {
            color: rgba(255,255,255,.9);
            font-size: .72rem;
            font-weight: 700;
            padding: .35rem .55rem;
            border-radius: 999px;
            background: rgba(255,255,255,.10);
            border: 1px solid rgba(255,255,255,.18);
        }

        /* ---------- Footer ---------- */
        .app-footer {
            margin-top: 2.5rem;
            padding: 1.35rem 0 .55rem 0;
            border-top: 1px solid rgba(100,116,139,.18);
        }

        .footer-main {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            align-items: center;
            padding: .25rem 0;
        }

        .footer-brand {
            font-weight: 800;
            font-size: .95rem;
        }

        .footer-text {
            color: #64748b;
            font-size: .78rem;
            margin-top: .2rem;
        }

        .footer-badge {
            font-size: .75rem;
            font-weight: 700;
            padding: .42rem .7rem;
            border-radius: 999px;
            border: 1px solid rgba(37,99,235,.16);
            background: rgba(239,246,255,.75);
            white-space: nowrap;
        }

        .footer-bottom {
            text-align: center;
            color: #94a3b8;
            font-size: .72rem;
            margin-top: 1rem;
        }

        @media (max-width: 640px) {
            .app-navbar {
                padding: .75rem .85rem;
            }

            .brand-name {
                font-size: 1rem;
            }

            .nav-right {
                display: none;
            }

            .footer-main {
                flex-direction: column;
                align-items: flex-start;
            }
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# API helpers
# -----------------------------
def api_request(
    method: str,
    backend_url: str,
    path: str,
    *,
    json: dict | None = None,
    timeout: int = 120,
) -> tuple[bool, Any, str]:
    url = f"{backend_url.rstrip('/')}{path}"
    try:
        response = requests.request(
            method,
            url,
            json=json,
            timeout=timeout,
        )

        try:
            payload = response.json()
        except ValueError:
            payload = response.text

        if response.ok:
            return True, payload, ""

        if isinstance(payload, dict):
            detail = payload.get("detail") or payload.get("error") or str(payload)
        else:
            detail = str(payload)

        return False, None, f"HTTP {response.status_code}: {detail}"

    except requests.exceptions.ConnectionError:
        return (
            False,
            None,
            f"Could not connect to the backend at {backend_url}. "
            "Make sure the FastAPI server is running and the URL is correct.",
        )
    except requests.exceptions.Timeout:
        return False, None, "The backend request timed out."
    except requests.exceptions.RequestException as exc:
        return False, None, f"Request failed: {exc}"


def health_check(backend_url: str):
    return api_request("GET", backend_url, "/health", timeout=10)


def clean_history(records: list[dict]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame()

    df = pd.DataFrame(records)

    for col in ["created_at"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in ["age", "bmi", "HbA1c_level", "blood_glucose_level"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.markdown("## 🩺 Healthcare AI")
st.sidebar.caption("Streamlit frontend for the FastAPI backend")

backend_url = st.sidebar.text_input(
    "Backend URL",
    value=st.session_state.get("backend_url", DEFAULT_BACKEND),
    help="Example: http://127.0.0.1:8000 or your deployed Azure App Service URL.",
).rstrip("/")

st.session_state["backend_url"] = backend_url

if st.sidebar.button("Check backend", use_container_width=True):
    ok, data, error = health_check(backend_url)
    if ok:
        st.sidebar.success("Backend is healthy")
    else:
        st.sidebar.error(error)

st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "🧪 Diabetes Prediction",
        "👤 Add Patient",
        "📋 Patient History",
        "🤖 AI Assistant",
        "📚 Medical RAG",
        "📊 Analytics Agent",
    ],
)

st.sidebar.divider()
st.sidebar.caption("Backend API")
st.sidebar.code(backend_url, language="text")


# -----------------------------
# Header
# -----------------------------
st.markdown(
    '<div class="main-header">Healthcare AI Platform</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="sub-header">'
    "Diabetes prediction • Patient records • Multi-agent AI • Medical RAG • Analytics"
    "</div>",
    unsafe_allow_html=True,
)


# -----------------------------
# Dashboard
# -----------------------------
if page == "🏠 Dashboard":
    ok, health, error = health_check(backend_url)

    service_name = health.get("service", "Healthcare AI Platform") if ok else "Backend unavailable"
    status_label = "● System Online" if ok else "● System Offline"

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-title">🩺 Smart Healthcare AI</div>
            <div class="hero-text">
                An intelligent healthcare workspace for diabetes risk prediction,
                patient management, medical knowledge retrieval and AI-powered analytics.
            </div>
            <span class="pill">{status_label}</span>
            <span class="pill">FastAPI</span>
            <span class="pill">Machine Learning</span>
            <span class="pill">RAG + Agents</span>
            <span class="pill">Azure Cloud</span>
        </div>
        """, unsafe_allow_html=True,
    )

    st.markdown('<div class="section-title">System Status</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Backend", "Online" if ok else "Offline")
    c2.metric("API", "FastAPI" if ok else "Unavailable")
    c3.metric("ML Engine", "Ready" if ok else "—")
    c4.metric("AI Services", "Active" if ok else "—")

    if ok:
        st.success(f"Connected • {service_name}")
    else:
        st.error(error)

    st.markdown('<div class="section-title">What you can do</div>', unsafe_allow_html=True)
    modules = [
        ("🧪", "Diabetes Prediction", "Estimate diabetes risk using patient health indicators and the trained ML model."),
        ("👤", "Patient Records", "Create and manage patient information through the connected backend."),
        ("📋", "Patient History", "Review stored records and explore basic patient health statistics."),
        ("🤖", "AI Assistant", "Interact with the multi-agent healthcare assistant for intelligent responses."),
        ("📚", "Medical RAG", "Ask questions using information retrieved from the medical knowledge base."),
        ("📊", "Analytics Agent", "Ask natural-language questions about healthcare data and receive insights."),
    ]
    cols = st.columns(3)
    for i, (icon, title, desc) in enumerate(modules):
        with cols[i % 3]:
            st.markdown(f"""<div class="module-card"><div class="module-icon">{icon}</div><div class="module-title">{title}</div><div class="module-desc">{desc}</div></div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">How the platform works</div>', unsafe_allow_html=True)
    steps = [
        ("01", "Patient Input", "Health information is entered through the Streamlit interface."),
        ("02", "FastAPI Backend", "Requests are sent to the deployed Azure API."),
        ("03", "AI / ML Processing", "Prediction, RAG or agent workflows process the request."),
        ("04", "Actionable Result", "The frontend displays the result, insights or patient data."),
    ]
    cols = st.columns(4)
    for i, (number, title, desc) in enumerate(steps):
        with cols[i]:
            st.markdown(f"""<div class="step-card"><div class="step-number">Step {number}</div><div class="step-title">{title}</div><div class="step-text">{desc}</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.info("☁️ **Cloud-connected frontend:** This Streamlit app only communicates with your FastAPI backend. Azure, MongoDB and OpenAI credentials remain on the backend and are not exposed in the frontend.")

# -----------------------------
# Diabetes Prediction
# -----------------------------
elif page == "🧪 Diabetes Prediction":
    st.subheader("Diabetes Risk Prediction")
    st.caption(
        "Inputs match the PatientData schema and the encoders used by your backend."
    )

    with st.form("prediction_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            name = st.text_input("Patient name *")
            gender = st.selectbox("Gender *", ["Female", "Male", "Other"])
            age = st.number_input("Age *", min_value=1, max_value=120, value=45)
            hypertension = st.selectbox("Hypertension *", ["No", "Yes"])

        with col2:
            heart_disease = st.selectbox("Heart disease *", ["No", "Yes"])
            smoking_history = st.selectbox(
                "Smoking history *",
                ["No Info", "current", "ever", "former", "never", "not current"],
            )
            bmi = st.number_input(
                "BMI *",
                min_value=5.0,
                max_value=80.0,
                value=25.0,
                step=0.1,
            )

        with col3:
            hba1c = st.number_input(
                "HbA1c level *",
                min_value=2.0,
                max_value=20.0,
                value=5.5,
                step=0.1,
            )
            glucose = st.number_input(
                "Blood glucose level *",
                min_value=20,
                max_value=500,
                value=100,
                step=1,
            )
            save_patient = st.checkbox(
                "Also save this patient to MongoDB",
                value=True,
            )

        submitted = st.form_submit_button(
            "Run Diabetes Prediction",
            type="primary",
            use_container_width=True,
        )

    if submitted:
        if not name.strip():
            st.error("Patient name is required.")
            st.stop()

        payload = {
            "name": name.strip(),
            "gender": gender,
            "age": int(age),
            "hypertension": hypertension,
            "heart_disease": heart_disease,
            "smoking_history": smoking_history,
            "bmi": float(bmi),
            "HbA1c_level": float(hba1c),
            "blood_glucose_level": int(glucose),
        }

        with st.spinner("Running prediction..."):
            ok, result, error = api_request(
                "POST",
                backend_url,
                "/predict",
                json=payload,
                timeout=120,
            )

        if not ok:
            st.error(error)
        else:
            prediction = result.get("prediction")
            confidence = float(result.get("confidence", 0))
            status = result.get("status", "Unknown")

            if prediction == 1:
                st.error(f"Prediction: {status}")
            else:
                st.success(f"Prediction: {status}")

            c1, c2, c3 = st.columns(3)
            c1.metric("Result", status)
            c2.metric("Model confidence", f"{confidence:.2f}%")
            c3.metric("Patient", result.get("patient_name", name))

            st.progress(min(max(confidence / 100, 0.0), 1.0))

            if save_patient:
                with st.spinner("Saving patient record..."):
                    saved, saved_result, save_error = api_request(
                        "POST",
                        backend_url,
                        "/add-patient",
                        json=payload,
                        timeout=30,
                    )

                if saved and saved_result.get("success", False):
                    st.success("Patient record saved successfully.")
                elif saved:
                    st.warning(
                        saved_result.get("error", "Patient record was not saved.")
                    )
                else:
                    st.warning(f"Prediction succeeded, but saving failed: {save_error}")

            st.warning(
                "This is an AI/ML prediction, not a medical diagnosis. "
                "Clinical decisions should be made by a qualified healthcare professional."
            )


# -----------------------------
# Add Patient
# -----------------------------
elif page == "👤 Add Patient":
    st.subheader("Add Patient Record")

    with st.form("patient_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Patient name *")
            gender = st.selectbox("Gender *", ["Female", "Male", "Other"])
            age = st.number_input("Age *", min_value=1, max_value=120, value=30)
            hypertension = st.selectbox("Hypertension *", ["No", "Yes"])
            heart_disease = st.selectbox("Heart disease *", ["No", "Yes"])

        with col2:
            smoking_history = st.selectbox(
                "Smoking history *",
                ["No Info", "current", "ever", "former", "never", "not current"],
            )
            bmi = st.number_input("BMI *", min_value=5.0, max_value=80.0, value=25.0, step=0.1)
            hba1c = st.number_input(
                "HbA1c level *",
                min_value=2.0,
                max_value=20.0,
                value=5.5,
                step=0.1,
            )
            glucose = st.number_input(
                "Blood glucose level *",
                min_value=20,
                max_value=500,
                value=100,
            )

        submit = st.form_submit_button(
            "Save Patient",
            type="primary",
            use_container_width=True,
        )

    if submit:
        if not name.strip():
            st.error("Patient name is required.")
        else:
            payload = {
                "name": name.strip(),
                "gender": gender,
                "age": int(age),
                "hypertension": hypertension,
                "heart_disease": heart_disease,
                "smoking_history": smoking_history,
                "bmi": float(bmi),
                "HbA1c_level": float(hba1c),
                "blood_glucose_level": int(glucose),
            }

            with st.spinner("Saving patient..."):
                ok, result, error = api_request(
                    "POST",
                    backend_url,
                    "/add-patient",
                    json=payload,
                    timeout=30,
                )

            if not ok:
                st.error(error)
            elif result.get("success"):
                st.success(result.get("message", "Patient added successfully."))
                st.code(result.get("patient_id", ""), language="text")
            else:
                st.error(result.get("error", "Could not save patient."))


# -----------------------------
# Patient History
# -----------------------------
elif page == "📋 Patient History":
    st.subheader("Patient History")

    if st.button("🔄 Refresh history", type="primary"):
        st.session_state["history_refresh"] = st.session_state.get("history_refresh", 0) + 1

    with st.spinner("Loading patient history..."):
        ok, result, error = api_request(
            "GET",
            backend_url,
            "/patient-history",
            timeout=30,
        )

    if not ok:
        st.error(error)
    elif not result.get("success", False):
        st.error(result.get("error", "Unable to load patient history."))
    else:
        records = result.get("patients", [])
        df = clean_history(records)

        if df.empty:
            st.info("No patient records are available.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total records", len(df))

            diabetic_col = (
                pd.to_numeric(df["diabetes"], errors="coerce")
                if "diabetes" in df.columns
                else None
            )
            c2.metric(
                "Avg age",
                f"{df['age'].mean():.1f}" if "age" in df.columns else "—",
            )
            c3.metric(
                "Avg BMI",
                f"{df['bmi'].mean():.1f}" if "bmi" in df.columns else "—",
            )
            c4.metric(
                "Hypertension",
                int(
                    (df["hypertension"].astype(str).str.lower() == "yes").sum()
                )
                if "hypertension" in df.columns
                else "—",
            )

            search = st.text_input("Search by patient name")
            if search:
                df = df[
                    df["name"].astype(str).str.contains(
                        search, case=False, na=False
                    )
                ]

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

            if "hypertension" in df.columns:
                st.markdown("### Hypertension distribution")
                hypertension_counts = (
                    df["hypertension"].astype(str).value_counts().rename_axis("status").to_frame("patients")
                )
                st.bar_chart(hypertension_counts)

            if "heart_disease" in df.columns:
                st.markdown("### Heart disease distribution")
                heart_counts = (
                    df["heart_disease"].astype(str).value_counts().rename_axis("status").to_frame("patients")
                )
                st.bar_chart(heart_counts)


# -----------------------------
# Multi-agent AI
# -----------------------------
elif page == "🤖 AI Assistant":
    st.subheader("Healthcare Multi-Agent Assistant")
    st.caption(
        "The backend orchestrator can use the Medical RAG, Symptom Triage, "
        "and Analytics agents."
    )

    question = st.text_area(
        "Ask a healthcare question",
        placeholder="Example: I have fever and headache. What should I consider?",
        height=130,
    )

    if st.button("Ask AI Agents", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Running healthcare agents..."):
                ok, result, error = api_request(
                    "POST",
                    backend_url,
                    "/agent-chat",
                    json={"question": question.strip()},
                    timeout=180,
                )

            if not ok:
                st.error(error)
            elif not result.get("success", False):
                st.error(result.get("error", "Agent request failed."))
            else:
                responses = result.get("responses", [])
                st.success(f"Agents used: {result.get('agents_used', len(responses))}")

                for item in responses:
                    agent = item.get("agent", "Healthcare Agent")
                    response = item.get("response", "")
                    st.markdown(
                        f'<div class="agent-card"><h4>🤖 {agent}</h4></div>',
                        unsafe_allow_html=True,
                    )
                    st.markdown(response)


# -----------------------------
# Medical RAG
# -----------------------------
elif page == "📚 Medical RAG":
    st.subheader("Medical Document Assistant")
    st.caption(
        "Questions are sent to the backend RAG pipeline, which retrieves "
        "relevant medical-document chunks before generating the answer."
    )

    question = st.text_area(
        "Medical question",
        placeholder="Example: What are common risk factors for diabetes?",
        height=130,
    )

    if st.button("Search Medical Knowledge", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Retrieving medical context and generating answer..."):
                ok, result, error = api_request(
                    "POST",
                    backend_url,
                    "/Document Assistant Agent",
                    json={"question": question.strip()},
                    timeout=180,
                )

            if not ok:
                st.error(error)
            elif not result.get("success", False):
                st.error(result.get("error", "RAG request failed."))
            else:
                st.markdown("### Answer")
                st.write(result.get("response", ""))

                st.info(
                    "The answer is generated from the backend's medical RAG system. "
                    "It should not replace professional medical advice."
                )


# -----------------------------
# Analytics Agent
# -----------------------------
elif page == "📊 Analytics Agent":
    st.subheader("Healthcare Analytics Agent")
    st.caption(
        "Ask questions that the current backend analytics agent understands, "
        "such as total patients, diabetic patients, glucose, BMI, hypertension, "
        "or heart disease."
    )

    example = st.selectbox(
        "Quick question",
        [
            "Give me a healthcare dataset summary",
            "What are the total patients?",
            "How many diabetic patients are there?",
            "What is the average glucose level?",
            "What is the average BMI?",
            "How many patients have hypertension?",
            "How many patients have heart disease?",
            "Custom question",
        ],
    )

    if example == "Custom question":
        question = st.text_input("Your analytics question")
    else:
        question = example

    if st.button("Run Analytics", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Running analytics agent..."):
                ok, result, error = api_request(
                    "POST",
                    backend_url,
                    "/analytics-agent",
                    json={"question": question.strip()},
                    timeout=60,
                )

            if not ok:
                st.error(error)
            elif not result.get("success", False):
                st.error(result.get("error", "Analytics request failed."))
            else:
                response = result.get("response", {})
                if isinstance(response, dict):
                    st.markdown(f"**Agent:** {response.get('agent', 'DataAnalystAgent')}")
                    st.markdown(response.get("response", ""))
                else:
                    st.write(response)


# ---------- Footer ----------
st.markdown(
    """
    <div class="app-footer">
        <div class="footer-main">
            <div>
                <div class="footer-brand">🩺 Smart Healthcare AI</div>
                <div class="footer-text">
                    AI-powered diabetes prediction, patient insights and medical assistance.
                </div>
            </div>
            <div class="footer-badge">☁️ Powered by Azure • FastAPI • ML</div>
        </div>
        <div class="footer-bottom">
            © 2026 Smart Healthcare AI • Built for intelligent and accessible healthcare
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)