from common import init_page, section_card
import streamlit as st

init_page()

section_card(
    "What is DemandPilot?",
    "DemandPilot is a client-ready retail demand intelligence product. It turns historical transaction data into executive KPIs, demand forecasts, model evaluation reports, and upload-based forecasting workflows."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="dp-section-card">
          <div class="dp-section-title">Problem</div>
          <div class="dp-section-copy">
            Retail teams need to anticipate demand across regions and product categories,
            but transaction data is usually fragmented across sales, discounts, margins,
            shipping cost, and product behavior.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="dp-section-card">
          <div class="dp-section-title">Solution</div>
          <div class="dp-section-copy">
            DemandPilot builds a daily forecasting panel, engineers time-series and business
            features, compares baseline and ML models, and serves forecasts through a live dashboard.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="dp-section-card">
          <div class="dp-section-title">Impact</div>
          <div class="dp-section-copy">
            The product helps business users understand demand risk, compare forecasting models,
            and generate forecasts from client-uploaded retail transaction files.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("### Product Workflow")

st.markdown(
    """
    <div class="dp-section-card">
      <div class="dp-section-title">From raw retail transactions to forecast-ready decisions</div>
      <div class="dp-section-copy">
        <b>1.</b> Clean and standardize historical retail data<br>
        <b>2.</b> Aggregate demand by date, region, and product category<br>
        <b>3.</b> Build lag, rolling, calendar, discount, profit, margin, and shipping features<br>
        <b>4.</b> Compare naive baselines, linear models, and nonlinear tree-based ML models<br>
        <b>5.</b> Persist the best model as a backend inference artifact<br>
        <b>6.</b> Let users upload client CSV files and download forecast outputs
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Best Model", "Random Forest")
col2.metric("SMAPE", "17.1%")
col3.metric("Forecast Level", "Region × Category")
col4.metric("Deployment", "Live App")

st.markdown("### Why this matters")

st.markdown(
    """
    <div class="dp-section-card">
      <div class="dp-section-title">Business value</div>
      <div class="dp-section-copy">
        Demand forecasting affects inventory planning, promotion strategy, staffing,
        purchasing, and revenue risk. DemandPilot frames forecasting as a product workflow:
        users can inspect trends, compare models, upload data, and export forecast results.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Use the sidebar navigation to open each workspace")

st.markdown(
    """
    <div class="dp-pill-row">
        <div class="dp-pill"><strong>Executive Overview</strong> KPI monitoring</div>
        <div class="dp-pill"><strong>Demand Explorer</strong> trend discovery</div>
        <div class="dp-pill"><strong>Forecasting Lab</strong> model comparison</div>
        <div class="dp-pill"><strong>Client Upload</strong> model inference</div>
        <div class="dp-pill"><strong>Profit & Discount</strong> margin intelligence</div>
    </div>
    """,
    unsafe_allow_html=True,
)
