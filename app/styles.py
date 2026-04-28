import streamlit as st


def apply_brand_style():
    st.markdown(
        """
        <style>
        :root {
            --dp-bg: #F8FAFC;
            --dp-bg-2: #EEF2FF;
            --dp-panel: rgba(255, 255, 255, 0.88);
            --dp-panel-2: rgba(239, 246, 255, 0.92);
            --dp-border: rgba(37, 99, 235, 0.16);
            --dp-text: #0F172A;
            --dp-muted: #475569;
            --dp-blue: #2563EB;
            --dp-indigo: #4F46E5;
            --dp-cyan: #0891B2;
            --dp-mint: #059669;
            --dp-soft: #DBEAFE;
            --dp-lavender: #EDE9FE;
        }

        .stApp {
            background:
                radial-gradient(circle at 8% 8%, rgba(79, 70, 229, 0.16), transparent 28%),
                radial-gradient(circle at 90% 12%, rgba(8, 145, 178, 0.12), transparent 26%),
                radial-gradient(circle at 50% 95%, rgba(5, 150, 105, 0.09), transparent 24%),
                linear-gradient(135deg, #F8FAFC 0%, #EEF2FF 45%, #F0FDFA 100%);
            color: var(--dp-text);
        }

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(239, 246, 255, 0.94)),
                radial-gradient(circle at 40% 5%, rgba(79, 70, 229, 0.12), transparent 34%);
            border-right: 1px solid var(--dp-border);
        }

        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span {
            color: var(--dp-text) !important;
        }

        .block-container {
            padding-top: 1.25rem;
            padding-bottom: 4rem;
            max-width: 1380px;
        }

        .dp-hero {
            position: relative;
            overflow: hidden;
            padding: 2.15rem 2.2rem;
            border-radius: 30px;
            border: 1px solid rgba(37, 99, 235, 0.18);
            background:
                linear-gradient(135deg, rgba(255, 255, 255, 0.94), rgba(239, 246, 255, 0.90)),
                radial-gradient(circle at 78% 18%, rgba(8, 145, 178, 0.15), transparent 22%),
                radial-gradient(circle at 18% 0%, rgba(79, 70, 229, 0.15), transparent 24%);
            box-shadow: 0 24px 70px rgba(30, 41, 59, 0.14);
            margin-bottom: 1.2rem;
        }

        .dp-hero:before {
            content: "";
            position: absolute;
            inset: -2px;
            background:
                linear-gradient(90deg, transparent, rgba(37, 99, 235, 0.14), transparent);
            transform: skewX(-18deg) translateX(-80%);
            animation: dp-shimmer 7s infinite;
        }

        @keyframes dp-shimmer {
            0% { transform: skewX(-18deg) translateX(-95%); }
            45% { transform: skewX(-18deg) translateX(125%); }
            100% { transform: skewX(-18deg) translateX(125%); }
        }

        .dp-eyebrow {
            display: inline-flex;
            gap: 0.45rem;
            align-items: center;
            padding: 0.38rem 0.75rem;
            border-radius: 999px;
            color: #FFFFFF;
            background: linear-gradient(90deg, var(--dp-blue), var(--dp-cyan));
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 0.85rem;
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.18);
        }

        .dp-title {
            font-size: clamp(2.3rem, 5vw, 4.7rem);
            line-height: 0.95;
            font-weight: 900;
            letter-spacing: -0.075em;
            margin: 0 0 0.8rem 0;
            background: linear-gradient(90deg, #0F172A 0%, #2563EB 42%, #0891B2 78%, #059669 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .dp-subtitle {
            max-width: 900px;
            color: var(--dp-muted);
            font-size: 1.08rem;
            line-height: 1.65;
            margin-bottom: 1.15rem;
        }

        .dp-pill-row {
            display: flex;
            flex-wrap: wrap;
            gap: 0.65rem;
            margin-top: 1.1rem;
        }

        .dp-pill {
            padding: 0.58rem 0.82rem;
            border-radius: 999px;
            border: 1px solid rgba(37, 99, 235, 0.14);
            background: rgba(255, 255, 255, 0.72);
            color: #1E293B;
            font-size: 0.88rem;
            font-weight: 650;
            backdrop-filter: blur(12px);
            box-shadow: 0 10px 24px rgba(30, 41, 59, 0.08);
        }

        .dp-pill strong {
            color: var(--dp-blue);
        }

        .dp-section-card {
            border-radius: 24px;
            padding: 1.1rem 1.25rem;
            border: 1px solid var(--dp-border);
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.90), rgba(239, 246, 255, 0.82));
            box-shadow: 0 16px 42px rgba(30, 41, 59, 0.10);
            margin: 0.75rem 0 1rem 0;
        }

        .dp-section-title {
            color: #0F172A;
            font-size: 1.1rem;
            font-weight: 850;
            letter-spacing: -0.02em;
            margin-bottom: 0.25rem;
        }

        .dp-section-copy {
            color: var(--dp-muted);
            font-size: 0.95rem;
            line-height: 1.55;
        }

        div[data-testid="stMetric"] {
            border-radius: 22px;
            padding: 1rem 1.05rem;
            border: 1px solid var(--dp-border);
            background:
                linear-gradient(135deg, rgba(255, 255, 255, 0.92), rgba(239, 246, 255, 0.78)),
                radial-gradient(circle at 80% 0%, rgba(8, 145, 178, 0.10), transparent 36%);
            box-shadow: 0 18px 40px rgba(30, 41, 59, 0.10);
        }

        div[data-testid="stMetric"] label {
            color: var(--dp-muted) !important;
            font-weight: 700 !important;
        }

        div[data-testid="stMetricValue"] {
            color: #0F172A !important;
            font-weight: 900 !important;
            letter-spacing: -0.04em;
        }

        .stTabs [data-baseweb="tab-list"] {
            gap: 0.45rem;
            background: rgba(255,255,255,0.70);
            border: 1px solid var(--dp-border);
            padding: 0.4rem;
            border-radius: 18px;
            box-shadow: 0 10px 30px rgba(30, 41, 59, 0.07);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 14px;
            padding: 0.7rem 1rem;
            color: #475569;
            font-weight: 750;
        }

        .stTabs [aria-selected="true"] {
            color: #FFFFFF !important;
            background: linear-gradient(90deg, var(--dp-blue), var(--dp-cyan)) !important;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid var(--dp-border);
            box-shadow: 0 18px 50px rgba(30, 41, 59, 0.10);
        }

        .stButton button,
        .stDownloadButton button {
            border-radius: 999px !important;
            border: 1px solid rgba(37, 99, 235, 0.18) !important;
            background: linear-gradient(90deg, var(--dp-blue), var(--dp-cyan)) !important;
            color: #FFFFFF !important;
            font-weight: 850 !important;
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.18);
        }

        .stFileUploader {
            border-radius: 24px;
            border: 1px dashed rgba(37, 99, 235, 0.35);
            background: rgba(219, 234, 254, 0.45);
            padding: 1rem;
        }

        .stAlert {
            border-radius: 18px;
        }

        h1, h2, h3 {
            letter-spacing: -0.04em;
            color: #0F172A;
        }

        hr {
            border-color: rgba(37, 99, 235, 0.14);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_brand_header():
    st.markdown(
        """
        <div class="dp-hero">
          <div class="dp-eyebrow">Demand Intelligence OS</div>
          <div class="dp-title">DemandPilot</div>
          <div class="dp-subtitle">
            A live retail forecasting product for executive analytics, model-backed demand prediction,
            and client-upload inference. Built as a polished ML system, not a notebook.
          </div>
          <div class="dp-pill-row">
            <div class="dp-pill"><strong>Live</strong> Streamlit Cloud</div>
            <div class="dp-pill"><strong>17.1%</strong> SMAPE best model</div>
            <div class="dp-pill"><strong>Upload</strong> forecast workflow</div>
            <div class="dp-pill"><strong>Docker</strong> ready</div>
            <div class="dp-pill"><strong>AWS</strong> planned</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_card(title, copy):
    st.markdown(
        f"""
        <div class="dp-section-card">
          <div class="dp-section-title">{title}</div>
          <div class="dp-section-copy">{copy}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
