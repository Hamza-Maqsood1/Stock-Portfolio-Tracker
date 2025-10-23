# CodeAlpha Task 2: Stock Portfolio Tracker (Simplified Realistic Version)
# Author: [Your Name]
# Internship: CodeAlpha Python Programming Internship

import pandas as pd
import datetime

# ======================================================
# Step 1: Load a realistic dataset from a public source
# ======================================================

# We'll use a small sample of Apple, Tesla, Google, Amazon, and Microsoft prices.
url = "https://raw.githubusercontent.com/datasets/stock-prices/master/data/all.csv"

try:
    df = pd.read_csv(url)
    print("✅ Dataset loaded successfully from public source!\n")
except Exception as e:
    print(f"⚠ Could not load dataset: {e}")
    exit()

# ======================================================
# Step 2: Filter dataset for a few companies
# ======================================================

companies = ["AAPL", "TSLA", "GOOG", "AMZN", "MSFT"]
df = df[df["Symbol"].isin(companies)]

# Get the most recent closing price for each company
latest_data = (
    df.groupby("Symbol")
    .apply(lambda x: x.sort_values("Date", ascending=False).iloc[0])
    .reset_index(drop=True)
)

# Dictionary: stock -> latest closing price
stock_prices = dict(zip(latest_data["Symbol"], latest_data["Close"]))

print("📈 Available Stocks and Latest Prices:")
for stock, price in stock_prices.items():
    print(f"{stock}: ${price:.2f}")

# ======================================================
# Step 3: Take user input
# ======================================================

portfolio = {}
total_value = 0

while True:
    stock_name = input("\nEnter stock symbol (or 'done' to finish): ").upper()
    if stock_name == "DONE":
        break

    if stock_name not in stock_prices:
        print("❌ Invalid stock symbol. Please choose from the list.")
        continue

    try:
        quantity = int(input(f"Enter quantity of {stock_name}: "))
        if quantity <= 0:
            print("⚠ Quantity must be positive.")
            continue
    except ValueError:
        print("⚠ Please enter a valid number.")
        continue

    investment = stock_prices[stock_name] * quantity
    portfolio[stock_name] = investment
    total_value += investment

    print(f"✅ Added {quantity} of {stock_name} worth ${investment:.2f}")

# ======================================================
# Step 4: Display portfolio summary
# ======================================================

print("\n📊 Portfolio Summary:")
print("-" * 35)
for stock, value in portfolio.items():
    print(f"{stock:<10} | Investment: ${value:.2f}")
print("-" * 35)
print(f"💰 Total Portfolio Value: ${total_value:.2f}")

# ======================================================
# Step 5: Save portfolio summary
# ======================================================

save_choice = input("\nDo you want to save your summary to CSV? (yes/no): ").lower()

if save_choice == "yes":
    file_name = f"portfolio_summary_{datetime.date.today()}.csv"
    pd.DataFrame(list(portfolio.items()), columns=["Stock", "Investment ($)"]).to_csv(file_name, index=False)
    print(f"✅ Portfolio summary saved as '{file_name}'")

print("\n🎯 Thank you for using the Stock Portfolio Tracker!")
