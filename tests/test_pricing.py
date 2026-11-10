"""Unit tests for SmartPricingOptimizer."""

from pricing.engine import SmartPricingOptimizer, ItemPricingData


def test_competitor_undercut():
    optimizer = SmartPricingOptimizer()
    data = ItemPricingData(
        item_code="ITM-HEADPHONES",
        item_name="Wireless ANC Headphones",
        cost_price=1200.0,
        current_selling_price=1999.0,
        competitor_market_price=1799.0,
        inventory_holding_days=10,
        target_margin_pct=25.0,
    )
    rec = optimizer.optimize_price(data)
    assert rec.action == "Match Competitor"
    assert rec.recommended_price == 1798.0
    assert rec.margin_at_recommended > 25.0


def test_clearance_slow_stock():
    optimizer = SmartPricingOptimizer()
    data = ItemPricingData(
        item_code="ITM-WINTER-JACKET",
        item_name="Winter Jacket",
        cost_price=800.0,
        current_selling_price=2200.0,
        inventory_holding_days=85,  # Stagnant inventory
        target_margin_pct=15.0,
    )
    rec = optimizer.optimize_price(data)
    assert rec.action == "Discount Clearance"
    assert rec.recommended_price < data.current_selling_price
