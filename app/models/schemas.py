from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Optional, List, Dict, Any

@dataclass
class BuyerRequirements:
    product: str = "Women's fashion footwear"
    destination: str = "Ghana"
    audience: str = "Young women"
    styles_min: int = 8
    styles_max: int = 12
    order_quantity: int = 100
    target_unit_price: Optional[float] = None
    material: str = "PU"
    shipping_method: str = "sea freight (estimate)"
    priority: str = "low_moq_balanced_risk"
    missing_critical: List[str] = None
    assumptions: List[str] = None
    def __post_init__(self):
        self.missing_critical = self.missing_critical or []
        self.assumptions = self.assumptions or []
    def to_dict(self) -> Dict[str, Any]: return asdict(self)

@dataclass
class DecisionState:
    required: bool
    reason: str
    options: List[Dict[str, Any]]
    recommended_supplier_id: Optional[str] = None

@dataclass
class ProcurementResult:
    requirements: Dict[str, Any]
    candidates: List[Dict[str, Any]]
    shortlist: List[Dict[str, Any]]
    decision: Dict[str, Any]
    metrics: Dict[str, Any]
