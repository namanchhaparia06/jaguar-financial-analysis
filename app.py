import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import FuncFormatter
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page configuration
st.set_page_config(
    page_title="Jaguar Land Rover Financial Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the data
fiscal_years = ['FY21/22', 'FY22/23', 'FY23/24']
data = pd.DataFrame({
    'fiscal_years': fiscal_years,
    'revenue': [18.3, 22.8, 29.0],  # in billion £
    'net_profit': [-0.4, -0.1, 2.2],  # in billion £, profit before tax & exceptional items
    'free_cash_flow': [-1.1, 0.5, 2.3],  # in billion £
    'net_debt': [3.2, 3.0, 0.7],  # in billion £
    'unit_sales': [376381, 354662, 431733]  # number of units
})

# Calculate year-over-year changes
data['revenue_yoy'] = data['revenue'].pct_change() * 100
data['net_profit_yoy'] = data['net_profit'].diff()
data['free_cash_flow_yoy'] = data['free_cash_flow'].diff()
data['net_debt_yoy'] = data['net_debt'].pct_change() * 100
data['unit_sales_yoy'] = data['unit_sales'].pct_change() * 100

# Replace NaN values with 0 for the first year
data.fillna(0, inplace=True)

# Function to format large numbers
def format_number(num):
    if abs(num) >= 1e9:
        return f"£{num/1e9:.1f}B"
    elif abs(num) >= 1e6:
        return f"£{num/1e6:.1f}M"
    elif abs(num) >= 1e3:
        return f"£{num/1e3:.1f}K"
    else:
        return f"£{num:.1f}"

# Function to format percentages
def format_pct(num):
    return f"{num:.1f}%"

# Set custom Seaborn theme
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 12})

# Custom color palette
jlr_colors = ["#0C2340", "#2F6F7E", "#41B6E6", "#A4C639", "#D32F2F"]

# Header
st.title("Jaguar Land Rover Financial Analysis Dashboard")
st.markdown("### FY21/22 - FY23/24")
st.markdown("*Analysis of JLR's financial performance during its 'Reimagine' strategic transformation*")

# Overview section
st.header("1. Overview & Strategic Context")
st.markdown("""
    Jaguar Land Rover has been executing its "Reimagine" strategy with remarkable results. 
    This dashboard analyzes the financial impact of JLR's transformation across three key pillars:
    
    * **Electrification**: Transitioning to electric-powered models including the flagship Range Rover Electric
    * **Modern Luxury & Brand Distinction**: Repositioning its brands to deliver distinctive luxury experiences
    * **Operational & Financial Turnaround**: Successfully addressing supply chain issues, reducing debt, and improving cash flow
    
    The analysis below demonstrates how these strategic initiatives have driven significant financial improvements.
""")

# Create tabs for different sections
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Dashboard",
    "Revenue & Sales",
    "Profitability",
    "Cash Flow & Debt",
    "Strategic Analysis"
])

# Tab 1: Dashboard
with tab1:
    st.header("Financial Performance Dashboard")
    
    # Key metrics in columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Revenue FY23/24", 
            f"£{data['revenue'].iloc[-1]}B", 
            f"{data['revenue_yoy'].iloc[-1]:.1f}%",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Net Profit FY23/24", 
            f"£{data['net_profit'].iloc[-1]}B", 
            f"{data['net_profit_yoy'].iloc[-1]:.1f}B",
            delta_color="normal"
        )
    
    with col3:
        st.metric(
            "Free Cash Flow FY23/24", 
            f"£{data['free_cash_flow'].iloc[-1]}B", 
            f"{data['free_cash_flow_yoy'].iloc[-1]:.1f}B",
            delta_color="normal"
        )
    
    with col4:
        # Net debt reduction is good, so reverse the delta color
        st.metric(
            "Net Debt FY23/24", 
            f"£{data['net_debt'].iloc[-1]}B", 
            f"{data['net_debt_yoy'].iloc[-1]:.1f}%",
            delta_color="inverse"
        )
    
    # Combined dashboard using Plotly
    st.subheader("Key Financial Metrics (FY21/22 - FY23/24)")
    
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "scatter"}, {"type": "bar"}],
               [{"type": "scatter"}, {"type": "scatter"}]],
        subplot_titles=("Revenue (Billion £)", "Net Profit (Billion £)", 
                       "Free Cash Flow (Billion £)", "Net Debt (Billion £)"),
        vertical_spacing=0.12,
        horizontal_spacing=0.08
    )
    
    # Revenue plot
    fig.add_trace(
        go.Scatter(
            x=fiscal_years, 
            y=data['revenue'], 
            mode='lines+markers+text',
            name='Revenue',
            line=dict(color=jlr_colors[0], width=3),
            marker=dict(size=12),
            text=[f"£{val}B" for val in data['revenue']],
            textposition="top center"
        ),
        row=1, col=1
    )
    
    # Net profit plot
    colors = ['#D32F2F' if x < 0 else '#4CAF50' for x in data['net_profit']]
    for i, (year, profit, color) in enumerate(zip(fiscal_years, data['net_profit'], colors)):
        fig.add_trace(
            go.Bar(
                x=[year], 
                y=[profit],
                name=year if i == 0 else None,
                marker_color=color,
                text=[f"£{profit}B"],
                textposition="outside",
                showlegend=False
            ),
            row=1, col=2
        )
    
    # Free cash flow
    fig.add_trace(
        go.Scatter(
            x=fiscal_years, 
            y=data['free_cash_flow'], 
            mode='lines+markers+text',
            name='Free Cash Flow',
            line=dict(color=jlr_colors[2], width=3),
            marker=dict(size=12),
            text=[f"£{val}B" for val in data['free_cash_flow']],
            textposition="top center",
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Net debt
    fig.add_trace(
        go.Scatter(
            x=fiscal_years, 
            y=data['net_debt'], 
            mode='lines+markers+text',
            name='Net Debt',
            line=dict(color=jlr_colors[4], width=3),
            marker=dict(size=12),
            text=[f"£{val}B" for val in data['net_debt']],
            textposition="top center",
            showlegend=False
        ),
        row=2, col=2
    )
    
    # Add zero reference lines
    fig.add_hline(y=0, line=dict(color="black", width=1), row=1, col=2)
    fig.add_hline(y=0, line=dict(color="black", width=1), row=2, col=1)
    
    fig.update_layout(
        height=700,
        title_text="",
        hovermode="x unified",
        template="plotly_white",
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Unit sales chart
    st.subheader("Unit Sales Performance")
    
    fig_units = px.line(
        data, 
        x='fiscal_years', 
        y='unit_sales',
        markers=True,
        labels={'unit_sales': 'Units Sold', 'fiscal_years': 'Fiscal Year'},
        template="plotly_white",
        color_discrete_sequence=[jlr_colors[3]]
    )
    
    fig_units.update_traces(
        line=dict(width=3),
        marker=dict(size=12),
        text=[f"{val:,}" for val in data['unit_sales']],
        textposition="top center"
    )
    
    fig_units.update_layout(
        height=400,
        yaxis=dict(title='Units Sold'),
        xaxis=dict(title='Fiscal Year'),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_units, use_container_width=True)

# Tab 2: Revenue & Sales
with tab2:
    st.header("2. Revenue & Unit Sales Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Revenue chart
        fig_rev = px.line(
            data, 
            x='fiscal_years', 
            y='revenue',
            markers=True,
            labels={'revenue': 'Revenue (Billion £)', 'fiscal_years': 'Fiscal Year'},
            template="plotly_white",
            color_discrete_sequence=[jlr_colors[0]]
        )
        
        fig_rev.update_traces(
            line=dict(width=3),
            marker=dict(size=12),
            text=[f"£{val}B" for val in data['revenue']],
            textposition="top center"
        )
        
        fig_rev.update_layout(
            title="Revenue Trend",
            height=400,
            yaxis=dict(title='Revenue (Billion £)'),
            xaxis=dict(title='Fiscal Year'),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_rev, use_container_width=True)
        
        # Revenue analysis
        st.subheader("Revenue Analysis")
        st.markdown("""
        **Key Observations:**
        * **FY21/22 to FY22/23:** 24% increase from £18.3B to £22.8B
        * **FY22/23 to FY23/24:** 27% increase from £22.8B to £29.0B
        * **Overall Growth:** 58% increase over the three-year period
        
        **Reasoning:**
        * **Improved Production & Supply Chain:** Resolution of semiconductor shortages and supply chain constraints
        * **Premium Product Mix:** Successful launches of new Range Rover models and SV Edition vehicles
        * **Electrification Strategy:** Growing market interest in JLR's electrified offerings
        * **Recovery in Global Demand:** Strengthening consumer confidence in luxury vehicle segment
        """)
    
    with col2:
        # Unit sales chart
        fig_units = px.line(
            data, 
            x='fiscal_years', 
            y='unit_sales',
            markers=True,
            labels={'unit_sales': 'Units Sold', 'fiscal_years': 'Fiscal Year'},
            template="plotly_white",
            color_discrete_sequence=[jlr_colors[3]]
        )
        
        fig_units.update_traces(
            line=dict(width=3),
            marker=dict(size=12),
            text=[f"{val:,}" for val in data['unit_sales']],
            textposition="top center"
        )
        
        fig_units.update_layout(
            title="Unit Sales Performance",
            height=400,
            yaxis=dict(title='Units Sold'),
            xaxis=dict(title='Fiscal Year'),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_units, use_container_width=True)
        
        # Unit sales analysis
        st.subheader("Unit Sales Analysis")
        st.markdown("""
        **Key Observations:**
        * **FY21/22 to FY22/23:** 5.8% decrease from 376,381 to 354,662 units
        * **FY22/23 to FY23/24:** 21.7% increase from 354,662 to 431,733 units
        * **Overall Growth:** 14.7% increase over the three-year period
        
        **Reasoning:**
        * **Initial Decline:** Production constraints and market uncertainty in FY22/23
        * **Strong Recovery:** Supply improvements and pent-up demand in FY23/24
        * **Market Confidence:** Return of consumer confidence in JLR's luxury offerings
        * **New Model Impact:** Success of refreshed Range Rover and Discovery product lines
        """)
    
    # Additional insights
    st.subheader("Revenue vs. Unit Sales Relationship")
    
    # Calculate revenue per unit
    data['revenue_per_unit'] = (data['revenue'] * 1e9) / data['unit_sales']
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Create the chart
        fig_rev_unit = px.bar(
            data,
            x='fiscal_years',
            y='revenue_per_unit',
            labels={'revenue_per_unit': 'Revenue per Unit (£)', 'fiscal_years': 'Fiscal Year'},
            template="plotly_white",
            color_discrete_sequence=[jlr_colors[1]]
        )
        
        fig_rev_unit.update_traces(
            text=[f"£{val:,.0f}" for val in data['revenue_per_unit']],
            textposition="outside"
        )
        
        fig_rev_unit.update_layout(
            title="Revenue per Unit",
            height=400,
            yaxis=dict(title='Revenue per Unit (£)'),
            xaxis=dict(title='Fiscal Year')
        )
        
        st.plotly_chart(fig_rev_unit, use_container_width=True)
    
    with col2:
        st.markdown("""
        **Revenue per Unit Analysis:**
        
        * **FY21/22:** £48,620 per vehicle
        * **FY22/23:** £64,286 per vehicle
        * **FY23/24:** £67,171 per vehicle
        
        **Key Insights:**
        * **Premium Mix Shift:** The significant increase in revenue per unit (32% from FY21/22 to FY22/23) indicates a successful shift toward higher-margin vehicles
        * **Value Enhancement:** JLR's "Modern Luxury" strategy is yielding higher transaction prices
        * **Brand Strength:** The ability to command premium pricing demonstrates the strength of JLR's brand positioning
        * **Profitable Growth:** This metric shows that growth is coming from both volume and value, supporting improved profitability
        """)

# Tab 3: Profitability
with tab3:
    st.header("3. Profitability & Operating Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Net profit chart
        colors = ['#D32F2F' if x < 0 else '#4CAF50' for x in data['net_profit']]
        
        fig_profit = go.Figure()
        
        for i, (year, profit, color) in enumerate(zip(fiscal_years, data['net_profit'], colors)):
            fig_profit.add_trace(
                go.Bar(
                    x=[year], 
                    y=[profit],
                    name=year,
                    marker_color=color,
                    text=[f"£{profit}B"],
                    textposition="outside",
                    showlegend=False
                )
            )
        
        fig_profit.add_hline(y=0, line=dict(color="black", width=1))
        
        fig_profit.update_layout(
            title="Net Profit Before Tax & Exceptional Items",
            height=400,
            yaxis=dict(title='Net Profit (Billion £)'),
            xaxis=dict(title='Fiscal Year'),
            template="plotly_white"
        )
        
        st.plotly_chart(fig_profit, use_container_width=True)
        
        # Profit margin calculation and chart
        data['profit_margin'] = (data['net_profit'] / data['revenue']) * 100
        
        fig_margin = px.line(
            data, 
            x='fiscal_years', 
            y='profit_margin',
            markers=True,
            labels={'profit_margin': 'Profit Margin (%)', 'fiscal_years': 'Fiscal Year'},
            template="plotly_white",
            color_discrete_sequence=[jlr_colors[2]]
        )
        
        fig_margin.update_traces(
            line=dict(width=3),
            marker=dict(size=12),
            text=[f"{val:.1f}%" for val in data['profit_margin']],
            textposition="top center"
        )
        
        fig_margin.add_hline(y=0, line=dict(color="black", width=1))
        
        fig_margin.update_layout(
            title="Profit Margin",
            height=400,
            yaxis=dict(title='Profit Margin (%)'),
            xaxis=dict(title='Fiscal Year'),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_margin, use_container_width=True)
    
    with col2:
        # Net profit analysis
        st.subheader("Profitability Analysis")
        st.markdown("""
        **Key Observations:**
        * **FY21/22:** £0.4B loss
        * **FY22/23:** £0.1B loss (75% reduction in losses)
        * **FY23/24:** £2.2B profit (dramatic turnaround)
        
        **Reasoning:**
        * **Operational Efficiencies:** Resolution of production bottlenecks and supply chain optimization
        * **Economies of Scale:** Higher production volumes lowering per-unit costs
        * **Premium Product Mix:** Higher-margin vehicles improving overall profitability
        * **Strategic Investments Paying Off:** Technology investments yielding productivity improvements
        * **Cost Discipline:** Successful implementation of cost-saving initiatives
        
        **Profit Margin Transformation:**
        * **FY21/22:** -2.2% margin
        * **FY22/23:** -0.4% margin
        * **FY23/24:** 7.6% margin
        
        This represents a nearly 10 percentage point improvement in profit margin, demonstrating the effectiveness of JLR's "Reimagine" strategy in transforming its business model.
        """)
        
        # Operating efficiency
        st.subheader("Operating Efficiency")
        st.markdown("""
        **Key Efficiency Drivers:**
        
        1. **Supply Chain Optimization:**
           * Resolution of semiconductor shortages
           * Improved component sourcing
           * Enhanced logistics management
        
        2. **Production Improvements:**
           * Increased plant utilization
           * Streamlined manufacturing processes
           * Higher throughput with better quality control
        
        3. **Strategic Cost Management:**
           * Fixed cost optimization
           * Targeted reduction in non-essential spending
           * Better supplier partnerships and negotiations
        
        4. **Technology Integration:**
           * Digital transformation initiatives
           * Automation of key processes
           * Data-driven decision making
        
        The combined effect has transformed JLR from an operationally challenged business to one demonstrating industry-competitive margins and financial performance.
        """)

# Tab 4: Cash Flow & Debt
with tab4:
    st.header("4. Cash Flow & Debt Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Free cash flow chart
        fig_fcf = px.line(
            data, 
            x='fiscal_years', 
            y='free_cash_flow',
            markers=True,
            labels={'free_cash_flow': 'Free Cash Flow (Billion £)', 'fiscal_years': 'Fiscal Year'},
            template="plotly_white",
            color_discrete_sequence=[jlr_colors[2]]
        )
        
        fig_fcf.update_traces(
            line=dict(width=3),
            marker=dict(size=12),
            text=[f"£{val}B" for val in data['free_cash_flow']],
            textposition="top center"
        )
        
        fig_fcf.add_hline(y=0, line=dict(color="black", width=1))
        
        fig_fcf.update_layout(
            title="Free Cash Flow Trend",
            height=400,
            yaxis=dict(title='Free Cash Flow (Billion £)'),
            xaxis=dict(title='Fiscal Year'),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_fcf, use_container_width=True)
        
        # Cash flow analysis
        st.subheader("Free Cash Flow Analysis")
        st.markdown("""
        **Key Observations:**
        * **FY21/22:** -£1.1B (negative free cash flow)
        * **FY22/23:** £0.5B (transition to positive cash flow)
        * **FY23/24:** £2.3B (strong positive free cash flow generation)
        
        **Reasoning:**
        * **Working Capital Management:** Improved inventory management and accounts receivable/payable processes
        * **Operational Efficiencies:** Higher earnings from core operations
        * **Capital Expenditure Optimization:** More targeted and efficient use of capital investments
        * **Cash Flow Discipline:** Strategic focus on cash generation across the organization
        
        This remarkable improvement in free cash flow has been a key enabler of JLR's debt reduction strategy.
        """)
    
    with col2:
        # Net debt chart
        fig_debt = px.line(
            data, 
            x='fiscal_years', 
            y='net_debt',
            markers=True,
            labels={'net_debt': 'Net Debt (Billion £)', 'fiscal_years': 'Fiscal Year'},
            template="plotly_white",
            color_discrete_sequence=[jlr_colors[4]]
        )
        
        fig_debt.update_traces(
            line=dict(width=3),
            marker=dict(size=12),
            text=[f"£{val}B" for val in data['net_debt']],
            textposition="top center"
        )
        
        fig_debt.update_layout(
            title="Net Debt Reduction",
            height=400,
            yaxis=dict(title='Net Debt (Billion £)'),
            xaxis=dict(title='Fiscal Year'),
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_debt, use_container_width=True)
        
        # Debt analysis
        st.subheader("Net Debt Analysis")
        st.markdown("""
        **Key Observations:**
        * **FY21/22:** £3.2B net debt
        * **FY22/23:** £3.0B net debt (6.3% reduction)
        * **FY23/24:** £0.7B net debt (76.7% reduction)
        
        **Reasoning:**
        * **Enhanced Free Cash Flow:** Surplus cash deployed to pay down debt
        * **Deleveraging Strategy:** Focused effort to strengthen the balance sheet
        * **Financial Resilience Building:** Creating capacity for future strategic investments
        * **Lower Interest Burden:** Reduced debt leads to lower interest expenses, further improving profitability
        
        The dramatic 78% reduction in net debt over the three-year period highlights the effectiveness of JLR's financial management strategy and positions the company for future growth investments, particularly in electrification.
        """)
        
        # Debt to Free Cash Flow Ratio
        data['debt_to_fcf'] = data['net_debt'] / data['free_cash_flow'].replace(0, float('nan'))
        data['debt_to_fcf'] = data['debt_to_fcf'].replace([float('inf'), float('-inf')], float('nan'))
        
        st.markdown("""
        **Debt to Free Cash Flow Ratio:**
        * **FY22/23:** 6.0x
        * **FY23/24:** 0.3x
        
        This dramatic improvement in debt to free cash flow ratio indicates that JLR has achieved a significantly more sustainable financial position, with debt levels that can be serviced comfortably by operating cash flows.
        """)

# Tab 5: Strategic Analysis
with tab5:
    st.header("5. Strategic Analysis & Future Outlook")
    
    # Key drivers of turnaround
    st.subheader("Key Drivers of JLR's Financial Turnaround")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Operational Drivers
        
        1. **Supply Chain Resilience:**
           * Resolution of semiconductor constraints
           * Diversification of supplier base
           * Enhanced logistics operations
        
        2. **Production Optimization:**
           * Improved manufacturing efficiency
           * Better capacity utilization
           * Quality improvements reducing waste
        
        3. **Premium Product Mix:**
           * Focus on higher-margin vehicles
           * Successful Range Rover portfolio update
           * "Modern Luxury" positioning driving higher transaction prices
        
        4. **Cost Discipline:**
           * Fixed cost optimization 
           * Strategic sourcing initiatives
           * Digital transformation reducing operational costs
        """)
    
    with col2:
        st.markdown("""
        ### Strategic Drivers
        
        1. **"Reimagine" Strategy Execution:**
           * Clear strategic direction
           * Focused implementation of key initiatives
           * Measurable outcomes and accountability
        
        2. **Electrification Progress:**
           * Investment in electric vehicle platforms
           * Announcement of Range Rover Electric
           * Building capabilities for future growth
        
        3. **Brand Strengthening:**
           * Enhanced brand differentiation
           * Customer experience improvements
           * Higher perceived value in marketplace
        
        4. **Financial Management:**
           * Working capital optimization
           * Disciplined capital allocation
           * Strategic debt reduction
        """)
    
    # Visualization of strategic pillars
    st.subheader("'Reimagine' Strategy Impact on Financial Performance")
        
    # Create a figure with subplots - removed subplot titles to avoid overlap
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "domain"}, {"type": "domain"}, {"type": "domain"}]],
    )

    # Electrification KPIs
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=29.0,
            title={"text": "<b>Electrification</b><br>Revenue (£B)", "font": {"size": 14}},
            delta={"reference": 18.3, "relative": True, "valueformat": ".1%"},
            domain={"row": 0, "column": 0}
        ),
        row=1, col=1
    )

    # Modern Luxury KPIs
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=67171,
            title={"text": "<b>Modern Luxury</b><br>Revenue per Unit (£)", "font": {"size": 14}},
            delta={"reference": 48620, "relative": True, "valueformat": ".1%"},
            number={"valueformat": ",.0f"},
            domain={"row": 0, "column": 1}
        ),
        row=1, col=2
    )

    # Operational Turnaround KPIs
    fig.add_trace(
        go.Indicator(
            mode="number+delta",
            value=0.7,
            title={"text": "<b>Operational Turnaround</b><br>Net Debt (£B)", "font": {"size": 14}},
            delta={"reference": 3.2, "relative": True, "valueformat": ".1%", "increasing": {"color": "red"}, "decreasing": {"color": "green"}},
            domain={"row": 0, "column": 2}
        ),
        row=1, col=3
    )

    fig.update_layout(
        height=300,
        grid={"rows": 1, "columns": 3, "pattern": "independent"},
        margin=dict(t=30, b=0, l=30, r=30)
    )

    st.plotly_chart(fig, use_container_width=True) 
       
    # Future outlook
    st.subheader("Future Outlook & Strategic Implications")
    
    st.markdown("""
    ### Key Strategic Implications
    
    Based on JLR's financial transformation over the past three years, several strategic implications emerge:
    
    1. **Financial Foundation for Electrification**
       * The improved financial position provides the foundation for accelerating JLR's electrification strategy
       * Reduced debt and strong cash flow enable higher R&D and capital investments in electric vehicle platforms
       * JLR can now self-fund its transition to electrification rather than relying on external financing
    
    2. **Competitive Positioning**
       * JLR has strengthened its competitive position in the luxury automotive segment
       * The combination of improved operations, distinctive brand positioning, and financial resilience creates a sustainable advantage
       * The company is better positioned to respond to market shifts and competitive threats
    
    3. **Growth Potential**
       * With operational excellence established, JLR can focus on strategic growth initiatives
       * The strong unit sales recovery indicates market receptiveness to JLR's modern luxury positioning
       * Future product launches, particularly in the electrified segment, can build on this momentum
    
    4. **Risk Management**
       * Significantly lower net debt reduces financial risk
       * Operational improvements create resilience against supply chain disruptions
       * The business can better withstand economic cycles and industry shifts
    
    ### Future Outlook
    
    JLR's transformation positions the company for continued success, though several factors will influence its future trajectory:
    
    1. **Electrification Execution**
       * Success of Range Rover Electric and other EV launches
       * Consumer adoption rates of luxury electric vehicles
       * Charging infrastructure development
    
    2. **Global Market Conditions**
       * Economic growth in key markets
       * Luxury consumer confidence
       * Regulatory environment for automotive manufacturers
    
    3. **Supply Chain Evolution**
       * Component availability for electric vehicles
       * Raw material costs, especially for batteries
       * Global logistics developments
    
    4. **Competitive Landscape**
       * Actions by traditional luxury automotive competitors
       * New entrants from technology sector
       * Evolution of mobility models and consumer preferences
    
    The financial data clearly indicates that JLR's "Reimagine" strategy is delivering tangible results. With continued disciplined execution, the company is well-positioned to capitalize on the luxury electric vehicle opportunity while maintaining its distinctive brand positioning.
    """)

# Sidebar
st.sidebar.image("logo.webp", width=200)
st.sidebar.title("About This Analysis")
st.sidebar.markdown("""
This dashboard presents a comprehensive analysis of Jaguar Land Rover's financial performance from FY21/22 to FY23/24, during the implementation""")