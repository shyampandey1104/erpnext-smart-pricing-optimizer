"""Dynamic Pricing & Margin Optimizer for ERPNext."""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class ItemPricingData(BaseModel):
    item_code: str
    item_name: str
    cost_price: float
    current_selling_price: float
    competitor_market_price: Optional[float] = None
    inventory_holding_days: int = 15  # Age of stock in warehouse
    target_margin_pct: float = 20.0  # Desired minimum profit margin


class PriceRecommendation(BaseModel):
    item_code: str
    current_price: float
    recommended_price: float
    margin_at_recommended: float
    action: str  # Increase Price, Discount Clearance, Match Competitor, Maintain Price
    rationale: str


class SmartPricingOptimizer:
    """Calculates price elasticity and dynamic margin optimization."""

    def optimize_price(self, data: ItemPricingData) -> PriceRecommendation:
        min_acceptable_price = data.cost_price * (1 + (data.target_margin_pct / 100.0))

        # 1. Slow-moving stock clearance (held > 60 days) -> clearance markdown
        if data.inventory_holding_days > 60:
            discounted = max(data.cost_price * 1.05, data.current_selling_price * 0.88)
            margin = ((discounted - data.cost_price) / discounted) * 100.0
            return PriceRecommendation(
                item_code=data.item_code,
                current_price=data.current_selling_price,
                recommended_price=round(discounted, 2),
                margin_at_recommended=round(margin, 1),
                action="Discount Clearance",
                rationale=f"Slow stock rotation ({data.inventory_holding_days} days in warehouse). Liquidation markdown advised.",
            )

        # 2. Competitor benchmark adjustment
        if data.competitor_market_price:
            comp_price = data.competitor_market_price
            if comp_price < data.current_selling_price and comp_price >= min_acceptable_price:
                # Price match slightly below competitor
                matched = round(comp_price - 1.0, 2)
                margin = ((matched - data.cost_price) / matched) * 100.0
                return PriceRecommendation(
                    item_code=data.item_code,
                    current_price=data.current_selling_price,
                    recommended_price=matched,
                    margin_at_recommended=round(margin, 1),
                    action="Match Competitor",
                    rationale=f"Competitor pricing ₹{comp_price} is lower. Undercutting to win buy-box while retaining {margin:.1f}% margin.",
                )
            elif comp_price > (data.current_selling_price * 1.10):
                # Opportunity to increase margin!
                new_price = round(data.current_selling_price * 1.08, 2)
                margin = ((new_price - data.cost_price) / new_price) * 100.0
                return PriceRecommendation(
                    item_code=data.item_code,
                    current_price=data.current_selling_price,
                    recommended_price=new_price,
                    margin_at_recommended=round(margin, 1),
                    action="Increase Price",
                    rationale=f"Market price is higher (₹{comp_price}). Increasing price captures higher margin without losing demand.",
                )

        # 3. Maintain current price
        curr_margin = ((data.current_selling_price - data.cost_price) / data.current_selling_price) * 100.0
        return PriceRecommendation(
            item_code=data.item_code,
            current_price=data.current_selling_price,
            recommended_price=data.current_selling_price,
            margin_at_recommended=round(curr_margin, 1),
            action="Maintain Price",
            rationale="Current price provides optimal margin and aligns with velocity.",
        )
