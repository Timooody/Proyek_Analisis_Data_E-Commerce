import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load datasets
products_df = pd.read_csv('./Data/products_dataset.csv')
sellers_df = pd.read_csv('./Data/sellers_dataset.csv')
customers_df = pd.read_csv('/Data/customers_dataset.csv')
geolocation_df = pd.read_csv('/Data/geolocation_dataset.csv')
orders_df = pd.read_csv('./Data/orders_dataset.csv')

# Convert timestamps
orders_df['order_purchase_timestamp'] = pd.to_datetime(orders_df['order_purchase_timestamp'])

#Side Dashboard
st.sidebar.title('📈 E-commerce Dashboard')
st.sidebar.image("foto.jpg",use_container_width=True)
# Profil Developer
st.sidebar.write("**Nama:** Zaenal Syamsyul Arief")
st.sidebar.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/zaenal-syamsyul-arief/)")
st.sidebar.markdown("[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/zaenalSamsul)")
    
# ---- FOOTER ----
st.sidebar.markdown(" " * 20)  # Spacer untuk mendorong footer ke bawah
st.sidebar.markdown("---")
st.sidebar.write("Developed by Zaenal Syamsyul Arief")

# Sidebar filters
def sidebar_filters():
    st.sidebar.header("Filter Data")
    start_date, end_date = st.sidebar.date_input(
        "Pilih Rentang Tanggal", 
        [orders_df['order_purchase_timestamp'].min().date(), orders_df['order_purchase_timestamp'].max().date()],
        key="date_range",
    )
    return start_date, end_date

# Filter data based on user input
def filter_data(start_date, end_date):
    filtered_orders = orders_df[(orders_df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
                                (orders_df['order_purchase_timestamp'] <= pd.Timestamp(end_date))]
    return filtered_orders

# Summary metrics
def show_summary(filtered_orders):
    st.markdown("### 📊 E-commerce Analysis Dashboard")
    st.markdown("Data diperbarui: Menampilkan Pemesanan dari {} hingga {}".format(
        filtered_orders['order_purchase_timestamp'].min().strftime('%Y-%m-%d'),
        filtered_orders['order_purchase_timestamp'].max().strftime('%Y-%m-%d')
    ))
    
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("🛒 Total Orders", f"{filtered_orders.shape[0]:,}")
    col2.metric("📦 Total Products", f"{products_df.shape[0]:,}")
    col3.metric("🧑‍💼 Total Sellers", f"{sellers_df.shape[0]:,}")
    col4.metric("👤 Total Customers", f"{customers_df.shape[0]:,}")
    col5.metric("📍 Total Geolocations", f"{geolocation_df['geolocation_state'].nunique():,}")

# Visualizations
def show_top_categories(filtered_orders):
    st.header("Produk dan Kategori Terlaris")
    top_categories = products_df['product_category_name'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y=top_categories.index, x=top_categories.values, palette="viridis", ax=ax)
    ax.set_title("Top 10 Categories by Sales")
    ax.set_xlabel("Number of Sales")
    ax.set_ylabel("Product Category")
    st.pyplot(fig)

def show_customer_locations():
    st.header("Wilayah Asal Pelanggan")
    customer_state_counts = customers_df['customer_state'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=customer_state_counts.index, y=customer_state_counts.values, palette="magma", ax=ax)
    ax.set_title("Top Customer States")
    ax.set_xlabel("State")
    ax.set_ylabel("Number of Customers")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def show_order_volume(filtered_orders):
    st.header("Volume Pesanan Tertinggi")
    filtered_orders['month'] = filtered_orders['order_purchase_timestamp'].dt.month
    monthly_orders = filtered_orders['month'].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=monthly_orders.index, y=monthly_orders.values, palette="viridis", ax=ax)
    ax.set_title("Monthly Order Volume")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Orders")
    plt.xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
    st.pyplot(fig)

def show_order_trends(filtered_orders):
    st.header("Tren Pesanan")
    filtered_orders['week'] = filtered_orders['order_purchase_timestamp'].dt.to_period('W')
    weekly_orders = filtered_orders['week'].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    weekly_orders.plot(kind='line', marker='o', color='blue', ax=ax)
    ax.set_title("Weekly Order Trends")
    ax.set_xlabel("Week")
    ax.set_ylabel("Number of Orders")
    ax.grid()
    st.pyplot(fig)

def show_geolocation_distribution():
    st.header("Distribusi Pesanan Berdasarkan Lokasi Geografis")
    geo_counts = geolocation_df['geolocation_state'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=geo_counts.index, y=geo_counts.values, palette="coolwarm", ax=ax)
    ax.set_title("Order Distribution by Geolocation")
    ax.set_xlabel("State")
    ax.set_ylabel("Number of Orders")
    plt.xticks(rotation=45)
    st.pyplot(fig)

def show_seasonal_patterns(filtered_orders):
    st.header("Identifikasi Pola Musiman")
    filtered_orders['month'] = filtered_orders['order_purchase_timestamp'].dt.month
    monthly_orders = filtered_orders['month'].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x=monthly_orders.index, y=monthly_orders.values, palette="viridis", ax=ax)
    ax.set_title("Monthly Order Volume")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Orders")
    plt.xticks(range(12), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
    ax.grid(axis='y')
    st.pyplot(fig)

def detect_anomalies(filtered_orders):
    st.header("Deteksi Anomali")
    filtered_orders['week'] = filtered_orders['order_purchase_timestamp'].dt.to_period('W')
    weekly_orders = filtered_orders['week'].value_counts().sort_index()
    
    fig, ax = plt.subplots(figsize=(15, 6))
    weekly_orders.plot(kind='line', marker='o', color='blue', ax=ax)
    ax.set_title("Weekly Order Trends")
    ax.set_xlabel("Week")
    ax.set_ylabel("Number of Orders")
    ax.grid()
    st.pyplot(fig)

    average_weekly_orders = weekly_orders.mean()
    st.write(f"Rata-rata jumlah pesanan per minggu: {average_weekly_orders:.2f}")

    anomalies = weekly_orders[(weekly_orders > average_weekly_orders * 1.5) | (weekly_orders < average_weekly_orders * 0.5)]
    st.write("Anomali Mingguan:", anomalies)

def show_yearly_trends(filtered_orders):
    st.header("Visualisasi Data Tahun ke Tahun")
    if 'year' not in filtered_orders.columns:
        filtered_orders['year'] = filtered_orders['order_purchase_timestamp'].dt.year

    filtered_orders['month'] = filtered_orders['order_purchase_timestamp'].dt.month
    annual_monthly_orders = filtered_orders.groupby(['year', 'month']).size().unstack(level=0)

    fig, ax = plt.subplots(figsize=(15, 8))
    annual_monthly_orders.plot(kind='line', marker='o', figsize=(15, 8), cmap='tab10', ax=ax)
    ax.set_title("Monthly Order Trends Year-over-Year")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Orders")
    plt.xticks(range(1, 13), ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], rotation=45)
    ax.legend(title="Year")
    ax.grid()
    st.pyplot(fig)

# Main app
def main():
    st.title("📈 E-Commerce Dashboard")
    start_date, end_date = sidebar_filters()
    filtered_orders = filter_data(start_date, end_date)

    show_summary(filtered_orders)
    show_top_categories(filtered_orders)
    show_customer_locations()
    show_order_volume(filtered_orders)
    show_order_trends(filtered_orders)
    show_geolocation_distribution()
    show_seasonal_patterns(filtered_orders)
    detect_anomalies(filtered_orders)
    show_yearly_trends(filtered_orders)
    


if __name__ == "__main__":
    main()
