# ERPNext Smart Pricing Optimizer 📈

![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![ERPNext](https://img.shields.io/badge/ERPNext-v14%20%7C%20v15-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)

An algorithmic dynamic pricing and margin optimization engine for **ERPNext Item Price & Price Lists**. It monitors warehouse inventory age, competitor market benchmarks, and minimum target margins to compute automated price adjustments, clearance markdowns, and buy-box wins.

---

## 🚀 Key Features

- **Inventory Holding Age Analysis**: Automatically suggests liquidation discounts for items idle for >60 days to free up working capital.
- **Competitor Benchmark Matching**: Undercuts competitor pricing to win the market while strictly safeguarding minimum profit margins.
- **Margin Expansion Opportunities**: Detects items underpriced relative to market surges and recommends upward price revisions.
- **Direct ERPNext Hooks**: Integrates seamlessly with ERPNext `Item Price` DocType via Frappe background jobs.

---

## 📦 Installation & Setup

```bash
git clone https://github.com/shyampandey1104/erpnext-smart-pricing-optimizer.git
cd erpnext-smart-pricing-optimizer
pip install -r requirements.txt
```

---

## 🛠️ Usage Example

```python
from pricing.engine import SmartPricingOptimizer, ItemPricingData

optimizer = SmartPricingOptimizer()

item = ItemPricingData(
    item_code="SKU-8821",
    item_name="Noise-Canceling Wireless Headphones",
    cost_price=1200.0,
    current_selling_price=1800.0,
    competitor_market_price=1650.0,
    inventory_holding_days=10,
    target_margin_pct=20.0
)

rec = optimizer.optimize_price(item)
print(f"Action: {rec.action} | Recommended: ₹{rec.recommended_price} ({rec.rationale})")
```

---

## 🧪 Testing

```bash
pytest tests/
```

---

## 📄 License
MIT License. Created with ❤️ by [Shyam Pandey](https://github.com/shyampandey1104).
