import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from model import train_model

# st.cache_data.clear()
# st.cache_resource.clear()

# dark graphs
sns.set_theme(style="darkgrid")
plt.rcParams.update({
    "axes.facecolor": "#0e1117",
    "figure.facecolor": "#0e1117",
    "axes.edgecolor": "#ffffff",
    "axes.labelcolor": "#ffffff",
    "xtick.color": "#ffffff",
    "ytick.color": "#ffffff",
    "text.color": "#ffffff"
})

# webpage css styling
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

.block-container {
    max-width: 1100px;
    padding-left: 2rem;
    padding-right: 2rem;
    margin: auto;
}

h1, h2, h3, h4 {
    color: #ffffff;
}
</style>
""", unsafe_allow_html=True) #treats the string as raw HTML, allowing us to apply custom styles to the Streamlit app


st.title("📦 E-commerce Return Analysis")
st.markdown("### 📊 Insights Dashboard")
st.write("""
This project analyzes product return patterns in an e-commerce setting to identify key factors contributing to returns and improve business decision-making. The dataset used is the Olist E-commerce Dataset, a real-world dataset from a Brazilian online marketplace that includes information on customers, orders, products, and transactions.

The goal is to generate actionable insights that help reduce return rates, improve product quality and descriptions, and enhance customer satisfaction.
""")

# Run this function once, save the result, and reuse it instead of running again
@st.cache_data
def load_data():
    customers = pd.read_csv("datasets/olist_customers_dataset.csv")
    orders = pd.read_csv("datasets/olist_orders_dataset.csv")
    items = pd.read_csv("datasets/olist_order_items_dataset.csv")
    products = pd.read_csv("datasets/olist_products_dataset.csv")

    orders = orders[orders['order_status'].isin(['delivered', 'canceled'])]

    df = orders.merge(customers, on='customer_id') \
               .merge(items, on='order_id') \
               .merge(products, on='product_id')

    df['is_return'] = df['order_status'] == 'canceled'
    return df

df = load_data()
returns = df[df['is_return']]

#prediction model
#caches the result of the function, so that if the function is called again with the same arguments, it will return the cached result instead of executing the function again.
@st.cache_resource
def get_model(df):
    return train_model(df)

model, columns = get_model(df)

with st.spinner("Analyzing data..."):

       st.markdown("### Step 1 of 5")
       st.subheader("Order Summary")

       return_counts = df['is_return'].value_counts()

       delivered = return_counts.get(False, 0)
       returned = return_counts.get(True, 0)

       col1, col2 = st.columns(2)

       with col1:
              st.metric("Delivered Orders", delivered)

       with col2:
              st.metric("Returned Orders", returned)
       st.divider()

       st.markdown("### Step 2 of 5")
       st.subheader("Return Rate")

       return_rate = (returned / (delivered + returned)) * 100

       st.metric("Return Rate", f"{return_rate:.2f}%")

       st.write("👉 Percentage of total orders that were returned.")
       st.divider()       

       # ---------------- GRAPH 1 ----------------
       st.markdown("### Step 3 of 5")
       st.subheader("Overall Return Rate")

       return_counts = df['is_return'].value_counts()
       labels = ['Delivered', 'Returned']
       colors = ['green', 'red']

       fig1, ax1 = plt.subplots(figsize=(3,3))
       ax1.pie(return_counts, labels=labels, autopct='%1.1f%%',
              colors=colors, startangle=90, textprops={'fontsize': 8})
       ax1.set_title('Overall Return Rate')

       st.pyplot(fig1, use_container_width=False)

       st.write("👉 This chart shows the proportion of returned vs successfully delivered products.")

       st.divider()

       # ---------------- GRAPH 2 ----------------
       st.markdown("### Step 4 of 5")
       st.subheader("Top 10 Returned Products")

       # Your original logic (clean and correct)
       product_returns = returns.groupby('product_id').size().sort_values(ascending=False)
       top_products = product_returns.head(10)

       fig2, ax2 = plt.subplots(figsize=(10,5))
       sns.barplot(
              x=top_products.values,
              y=top_products.index,
              ax=ax2
       )

       ax2.set_title("Top 10 Returned Products (by ID)")
       ax2.set_xlabel("Number of Returns")
       ax2.set_ylabel("Product ID")

       st.pyplot(fig2)

       st.write(f"👉 Products with IDs {top_products.index[0]} and {top_products.index[1]} have the highest number of returns and may indicate quality or expectation mismatches.")
       # ---------------- GRAPH 3 ----------------
       st.markdown("### Step 5 of 5")
       st.subheader("Top 10 Risky Categories")

       category_risk = (
              df.dropna(subset=['product_category_name'])
              .groupby('product_category_name')['is_return']
              .mean()
              .sort_values(ascending=False)
       )
       # Top 10 risky categories
       top_categories = category_risk.head(10)

       top_categories_percent = top_categories * 100

       fig3, ax3 = plt.subplots(figsize=(10,5))

       sns.barplot(
              x=top_categories_percent.values,
              y=top_categories_percent.index,
              color='orange',
              ax=ax3
       )

       ax3.set_xlabel('Return Rate (%)')
       ax3.set_title('Top 10 Risky Categories')

       # Add labels
       for i, v in enumerate(top_categories_percent.values):
              ax3.text(v + 0.1, i, f'{v:.1f}%', va='center')

       st.pyplot(fig3)

       st.write(f"👉 {top_categories.index[0]} has the highest return rate of {top_categories.values[0]*100:.1f}%.")

       st.divider()

       # ---------------- PREDICTION ----------------
       
       # -------- LOOP (CALCULATE) --------
       st.markdown("## 🤖 Prediction: Delivery Success Rate")

       category_probs = {}

       category_columns = [col for col in columns if col not in ['price', 'freight_value']]

       for cat in category_columns:
              temp = pd.DataFrame(0, index=[0], columns=columns)

              # use REAL data for that category
              cat_data = df[df['product_category_name'] == cat]

              temp['price'] = cat_data['price'].mean()
              temp['freight_value'] = cat_data['freight_value'].mean()

              temp[cat] = 1

              prob_return = model.predict_proba(temp)[0][1]
              category_probs[cat] = (1 - prob_return) * 100

       # dropdown UI
       selected_category = st.selectbox(
              "Select Product Category",
              sorted(category_probs.keys())
       )

       # result
       prob = category_probs[selected_category]

       st.metric("Predicted Success Rate", f"{prob:.2f}%")

       # optional insight
       if prob > 90:
              st.success("✅ Very high chance of successful delivery")
       elif prob > 75:
              st.info("👍 Good chance of delivery")
       else:
              st.warning("⚠️ Higher risk of return")

       st.divider()

       st.markdown("---")
       st.markdown("## 💡 Key Business Insights")

       st.success("High return rates indicate potential issues in product quality, sizing, or expectations.")
       st.warning("Top returned products should be reviewed for defects or misleading descriptions.")
       st.info("Reducing return rates can significantly improve customer satisfaction and profit margins.")