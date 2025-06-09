# ========== IMPORT LIBRARIES ============
import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np

# ========== DASHBOARD CONFIG ============
st.set_page_config(
    page_title="Car Sales Dashboard",
    page_icon=":car:",
    layout="wide",
    initial_sidebar_state="expanded" # Keep sidebar expanded by default
)

# ========== TEMA / CSS KUSTOM ==========
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    html, body, .stApp {
        font-family: 'Poppins', sans-serif;
        background-color: #F0F2F6; /* Light gray background for main app */
        color: #333333;
    }

    /* Top navigation bar (simulated header for a darker top section) */
    .stApp > header {
        background-color: #001F3F; /* Dark blue for top header */
        height: 70px; /* Adjust height as needed */
        display: flex;
        align-items: center;
        padding: 0 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        color: white; /* Text color for header */
    }
    .stApp > header h1 { /* Targeting the title in the header if it lands there */
        color: white !important;
        margin: 0;
    }


    .stSidebar {
        background-color: #001F3F; /* Dark blue for sidebar */
        border-right: 1px solid #003366;
        color: #FFFFFF; /* White text for sidebar */
    }

    /* Text within sidebar */
    .stSidebar .st-emotion-cache-1we6djp, /* target filter labels */
    .stSidebar .st-emotion-cache-nahz7x { /* target multiselect labels */
        color: #FFFFFF; /* White text for multiselect labels */
    }

    .stButton>button {
        background-color: #FFFFFF; /* White background for buttons */
        color: #001F3F; /* Dark blue text for buttons */
        border-radius: 12px;
        padding: 12px 25px;
        font-size: 16px;
        border: none;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.2);
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background-color: #ADD8E6; /* Light blue on hover */
        color: #001F3F;
        transform: translateY(-2px);
        box-shadow: 4px 4px 12px rgba(0,0,0,0.3);
    }

    h1, h2, h3, .chart-title {
        color: #1A1A1A; /* Darker heading color for main content */
        font-weight: 600;
    }

    .chart-title {
        font-size: 26px;
        font-weight: 700;
        color: #1A1A1A;
        margin-bottom: 20px;
        text-align: center;
        padding-top: 10px;
    }

    /* Metric Cards - White background, subtle shadow */
    [data-testid="stMetric"] {
        background-color: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #ddd;
        width: 100%;
        min-width: 200px;
        max-width: 280px;
        text-align: center;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {
        white-space: normal !important;
        word-wrap: break-word;
        font-size: 16px;
        text-align: center;
    }

    .css-1r6dm7m { /* Targets the main content block */
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    hr {
        border-top: 2px solid #D1D9E0;
        margin-top: 30px;
        margin-bottom: 30px;
    }

    /* Tab styling - White background for content, blue for active tab */
    .stTabs [data-testid="stTab"] {
        background-color: #E6EEF5;
        border-radius: 10px 10px 0 0;
        margin-right: 5px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 500;
        color: #555555;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
    }

    .stTabs [data-testid="stTab"][aria-selected="true"] {
        background-color: #0077B6; /* Active tab blue */
        color: white;
        border-bottom: 3px solid #005080;
        font-weight: 600;
    }

    .stTabs [data-testid="stTabContent"] {
        background-color: white;
        border-radius: 0 0 15px 15px;
        padding: 25px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.1);
        border: 1px solid #E0E0E0;
        margin-top: -10px;
    }

    /* Custom CSS for a subtle background image */
    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/gray-jean.png"); /* More neutral, subtle pattern */
        background-repeat: repeat;
        background-attachment: fixed;
    }

    /* Ensure plot backgrounds are white with subtle shadows */
    .plotly-container {
        background-color: white;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ========== LOAD DATA ============
try:
    # Use st.cache_data for better performance with large datasets
    @st.cache_data
    def load_data(path):
        data = pd.read_csv(path)
        data["Date"] = pd.to_datetime(data["Date"])
        data["order_month"] = data["Date"].dt.to_period("M").dt.to_timestamp()
        data["order_year"] = data["Date"].dt.year
        # Add 'Price Category' here as it's part of data processing
        bins = [0, 20000, 40000, 60000, 100000, np.inf]
        labels = ['<20K', '20K-40K', '40K-60K', '60K-100K', '>100K']
        data['Price Category'] = pd.cut(data['Price ($)'], bins=bins, labels=labels, right=False, ordered=True)
        return data

    # Path to your CSV file - make sure it's correct for your environment
    # For deployment, consider placing the CSV in the same directory as the script
    data = load_data(r"C:\Users\ASUS\Downloads\data python.csv") #
except FileNotFoundError:
    st.error("Error: 'data.csv' not found. Please ensure the data file is in the correct directory or path is correct.") #
    st.stop() # Stop execution if data is not found

# ========== SIDEBAR FILTER ============
st.sidebar.title("🚗 Data Filters")
st.sidebar.markdown("Adjust the parameters below to explore different segments of the data.")

body_style = st.sidebar.multiselect(
    "Select Body Style:",
    options=data["Body Style"].unique(),
    default=data["Body Style"].unique()
)
company = st.sidebar.multiselect(
    "Select Company:",
    options=data["Company"].unique(),
    default=data["Company"].unique()
)
year = st.sidebar.multiselect(
    "Select Year:",
    options=sorted(data["order_year"].unique()),
    default=sorted(data["order_year"].unique())
)

filtered_data = data[
    (data["Body Style"].isin(body_style)) &
    (data["Company"].isin(company)) &
    (data["order_year"].isin(year))
]

# Display an alert if no data is filtered
if filtered_data.empty:
    st.warning("No data matches the selected filters. Please adjust your selections.")
    st.stop()


# ========== HEADER (Simulated Top Bar) ============
# Streamlit's header is handled by the "stApp > header" CSS rule.
# The title below will appear in the main content area, but we've styled the Streamlit's native header space.
st.markdown("<h1 style='text-align: center; color: #1A1A1A;'>🚗 Car Sales Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #555555;'>Delving into Sales, Customer Behavior, and Regional Performance</h3>", unsafe_allow_html=True)
st.markdown("---")

# ========== KPI SECTION ============
st.markdown("<h2 style='text-align: center; color: #1A1A1A;'>Key Performance Indicators</h2>", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)

with col1:
    average_price = filtered_data["Price ($)"].mean()
    st.metric("Avg. Car Price", f"US$ {average_price:,.2f}")

with col2:
    std_price = filtered_data["Price ($)"].std()
    st.metric("Price Std. Dev.", f"US$ {std_price:,.2f}")

with col3:
    avg_income = filtered_data["Annual Income"].mean()
    st.metric("Avg. Customer Income", f"US$ {avg_income:,.2f}")

with col4:
    total_sales = len(filtered_data)
    st.metric("Total Transactions", f"{total_sales:,} Cars Sold")
st.markdown("---")

# ========== CHARTS SECTION ============
st.markdown("<h2 style='text-align: center; color: #1A1A1A;'>Interactive Insights</h2>", unsafe_allow_html=True)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Price Distribution", "Sales by Gender", "Avg Price by Body Style",
    "Income vs Price", "Sales by Region", "Sales Trend"
])

with tab1:
    st.markdown("<h3 class='chart-title'>Distribution of Car Prices</h3>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        fig_hist = px.histogram(filtered_data, x="Price ($)", nbins=40,
                                title="Histogram of Car Prices",
                                color_discrete_sequence=px.colors.sequential.Blues_r)
        fig_hist.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                                font=dict(family="Poppins"),
                                bargap=0.05)
        st.plotly_chart(fig_hist, use_container_width=True)
    with col_b:
        fig_box = px.box(filtered_data, y="Price ($)", title="Boxplot of Car Prices",
                         color_discrete_sequence=["#0077B6"])
        fig_box.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                              font=dict(family="Poppins"))
        st.plotly_chart(fig_box, use_container_width=True)

with tab2:
    st.markdown("<h3 class='chart-title'>Car Sales by Gender</h3>", unsafe_allow_html=True)
    gender_counts = filtered_data["Gender"].value_counts().reset_index()
    gender_counts.columns = ["Gender", "Count"]
    fig_gender = px.pie(gender_counts, names="Gender", values="Count",
                        title="Sales Distribution by Gender",
                        color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_gender.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                             font=dict(family="Poppins"))
    st.plotly_chart(fig_gender, use_container_width=True)

with tab3:
    st.markdown("<h3 class='chart-title'>Average Price by Body Style</h3>", unsafe_allow_html=True)
    avg_price_body = filtered_data.groupby("Body Style")["Price ($)"].mean().reset_index().sort_values(by="Price ($)", ascending=False)
    fig_body = px.bar(avg_price_body, x="Body Style", y="Price ($)",
                      title="Average Car Price by Body Style",
                      color="Price ($)", color_continuous_scale="Blues")
    fig_body.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                           font=dict(family="Poppins"),
                           xaxis_title="Body Style", yaxis_title="Average Price ($)")
    st.plotly_chart(fig_body, use_container_width=True)

with tab4:
    st.markdown("<h3 class='chart-title'>Annual Income vs Car Price</h3>", unsafe_allow_html=True)

    # Filter data for scatter/heatmap/box plot (Annual Income > 0)
    income_price_data = filtered_data[(filtered_data["Annual Income"] > 0)]

    # Add a selectbox for chart type
    plot_type = st.selectbox(
        "Choose Plot Type for Income vs Price:",
        ("Scatter Plot", "Heatmap", "Box Plot (by Price Category)")
    )

    if plot_type == "Scatter Plot":
        if not income_price_data.empty:
            fig_scatter = px.scatter(income_price_data, x="Price ($)", y="Annual Income",
                                     size="Annual Income", color="Body Style",
                                     hover_name="Car_id", title="Price vs Annual Income (Scatter)",
                                     log_y=True, template="plotly_white",
                                     color_discrete_sequence=px.colors.qualitative.D3)
            fig_scatter.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                                      font=dict(family="Poppins"))
            fig_scatter.add_vline(x=income_price_data["Price ($)"].mean(), line_dash="dash", line_color="red",
                                  annotation_text=f"Avg Price: {income_price_data['Price ($)'].mean():,.0f}")
            fig_scatter.add_hline(y=income_price_data["Annual Income"].mean(), line_dash="dash", line_color="green",
                                  annotation_text=f"Avg Income: {income_price_data['Annual Income'].mean():,.0f}")
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.info("No data available for 'Annual Income vs Car Price' after filtering for positive income.")

    elif plot_type == "Heatmap":
        if not income_price_data.empty:
            fig_heatmap = px.density_heatmap(income_price_data, x="Price ($)", y="Annual Income",
                                             nbinsx=50, nbinsy=50,
                                             title="Kepadatan Konsumen Berdasarkan Harga Mobil dan Pendapatan Tahunan (Heatmap)",
                                             color_continuous_scale="Viridis")
            fig_heatmap.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                                      font=dict(family="Poppins"),
                                      xaxis_title="Harga Mobil ($)", yaxis_title="Pendapatan Tahunan ($)")
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info("No data available for 'Annual Income vs Car Price' after filtering for positive income.")

    elif plot_type == "Box Plot (by Price Category)":
        if not income_price_data.empty:
            fig_box_income = px.box(income_price_data, x="Price Category", y="Annual Income",
                                    color="Price Category",
                                    title="Ringkasan Pendapatan Tahunan berdasarkan Kategori Harga Mobil (Box Plot)",
                                    category_orders={"Price Category": labels})
            fig_box_income.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                                         font=dict(family="Poppins"),
                                         xaxis_title="Kategori Harga Mobil", yaxis_title="Pendapatan Tahunan ($)")
            st.plotly_chart(fig_box_income, use_container_width=True)
        else:
            st.info("No data available for 'Annual Income vs Car Price' after filtering for positive income.")

with tab5:
    st.markdown("<h3 class='chart-title'>Sales by Dealer Region</h3>", unsafe_allow_html=True)
    region_sales = filtered_data["Dealer_Region"].value_counts().reset_index()
    region_sales.columns = ["Region", "Sales"]
    fig_region = px.bar(region_sales, x="Region", y="Sales",
                        title="Number of Cars Sold per Region",
                        color="Sales", color_continuous_scale="Purples")
    fig_region.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                             font=dict(family="Poppins"),
                             xaxis_title="Dealer Region", yaxis_title="Number of Sales")
    st.plotly_chart(fig_region, use_container_width=True)

with tab6:
    st.markdown("<h3 class='chart-title'>Monthly Sales Trend</h3>", unsafe_allow_html=True)
    trend_data = filtered_data.groupby("order_month")["Price ($)"].sum().reset_index()
    fig_trend = px.line(trend_data, x="order_month", y="Price ($)", markers=True,
                        title="Monthly Sales Trend (Total Revenue)",
                        template="plotly_white")
    fig_trend.update_traces(line_color="#0077B6", marker_color="#0077B6") # Use the theme blue
    fig_trend.update_layout(plot_bgcolor='white', paper_bgcolor='white',
                            font=dict(family="Poppins"),
                            xaxis_title="Month", yaxis_title="Total Sales Revenue ($)")
    st.plotly_chart(fig_trend, use_container_width=True)

# ========== DATA TABLE ============
st.markdown("---")
st.subheader("Filtered Data Preview")
st.dataframe(filtered_data, use_container_width=True)

# ========== FOOTER / CREDITS ============
st.markdown("---")
if st.button("Show Credits"):
    st.info("Dashboard developed by **Kelompok 2** | Data Source: **Car Sales Data**")