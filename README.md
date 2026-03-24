# E-commerce Return Analysis

## Overview
This project analyzes **returns in an e-commerce dataset** (Olist dataset) to answer key business questions and provide insights that can help **reduce return losses**.  

The analysis focuses on:
- Overall **Return Rate**
- **Product Return Pattern**
- **Category Risk**

---

## Business Questions
1. **Return rate?**  
   What percentage of orders are returned?

2. **Product return pattern?**  
   Which products are returned most frequently?

3. **Category risk?**  
   Which product categories have the highest return rates?

**Objective:** Reduce return losses by identifying high-risk products and categories.

---

## Dataset
The analysis uses **4 CSV files from the Brazilian E-Commerce Public Dataset by Olist**:

1. `olist_customers_dataset.csv` – customer details  
2. `olist_orders_dataset.csv` – order details including status  
3. `olist_order_items_dataset.csv` – items in each order  
4. `olist_orders_dataset.csv` – product details and categories  

---

## Analysis & Visualizations

1. **Return Rate (Overall)**
   - Pie chart showing Delivered vs Returned orders
   - Insight: Shows the **overall scale of returns**

2. **Top 10 Returned Products**
   - Horizontal bar chart with exact counts on top
   - Insight: Identifies products causing the most returns

3. **Top 10 Risky Categories**
   - Horizontal bar chart (and optional pie chart with legend)
   - Insight: Highlights categories with the **highest return rates**

---

## Key Findings

- **Return Rate:** '0.49%' of orders were returned  
- **Top Products:** Product IDs 'X' and 'Y' had the highest number of returns  
- **Category Risk:** Category 'pc_gamer' had the highest return rate (11.1%) 

---

## Technologies Used
- Python  
- Pandas (data manipulation)  
- NumPy (numerical operations)  
- Matplotlib (visualization)  
- Jupyter Notebook / VSCode (for running the notebook)

## Credits
Dataset: [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) <br>
License: [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) <br>
Changes made: None