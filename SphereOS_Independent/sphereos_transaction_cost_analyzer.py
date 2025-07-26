"""
SphereOS Transaction Cost Analyzer
Analyzes transaction costs and profitability of opportunities
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum


class TransactionCostType(Enum):
    DISTANCE = "distance"
    TIME = "time"
    COMPLEXITY = "complexity"
    COORDINATION = "coordination"
    LEGAL = "legal"
    TECHNICAL = "technical"


class ProfitabilityStatus(Enum):
    PROFITABLE = "profitable"
    BREAKEVEN = "breakeven"
    UNPROFITABLE = "unprofitable"
    UNCERTAIN = "uncertain"


class FrictionFactor(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ProfitabilityAnalysis:
    opportunity_id: str
    total_cost: float
    total_value: float
    net_profit: float
    profitability_status: ProfitabilityStatus
    cost_breakdown: Dict[str, float]
    friction_factors: List[FrictionFactor]
    recommendations: List[str]
    confidence_score: float
    created_at: str


class TransactionCostAnalyzer:
    """Analyzes transaction costs and profitability"""
    
    def __init__(self):
        self.cost_models = {
            TransactionCostType.DISTANCE: self._calculate_distance_cost,
            TransactionCostType.TIME: self._calculate_time_cost,
            TransactionCostType.COMPLEXITY: self._calculate_complexity_cost,
            TransactionCostType.COORDINATION: self._calculate_coordination_cost,
            TransactionCostType.LEGAL: self._calculate_legal_cost,
            TransactionCostType.TECHNICAL: self._calculate_technical_cost,
        }
    
    async def analyze_transaction_cost(self, opportunity_id: str, distance_km: float = 0,
                                     participants: int = 2, complexity_score: float = 1.0,
                                     risk_factors: str = None) -> ProfitabilityAnalysis:
        """Analyze transaction cost for an opportunity"""
        
        # Calculate costs
        distance_cost = self._calculate_distance_cost(distance_km)
        time_cost = self._calculate_time_cost(participants, complexity_score)
        complexity_cost = self._calculate_complexity_cost(complexity_score)
        coordination_cost = self._calculate_coordination_cost(participants)
        legal_cost = self._calculate_legal_cost(risk_factors)
        technical_cost = self._calculate_technical_cost(complexity_score)
        
        total_cost = distance_cost + time_cost + complexity_cost + coordination_cost + legal_cost + technical_cost
        
        # Estimate value (simplified)
        total_value = self._estimate_opportunity_value(opportunity_id, participants, complexity_score)
        
        net_profit = total_value - total_cost
        
        # Determine profitability status
        if net_profit > 0:
            status = ProfitabilityStatus.PROFITABLE
        elif net_profit == 0:
            status = ProfitabilityStatus.BREAKEVEN
        else:
            status = ProfitabilityStatus.UNPROFITABLE
        
        # Identify friction factors
        friction_factors = self._identify_friction_factors(distance_km, participants, complexity_score, risk_factors)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(total_cost, total_value, friction_factors)
        
        return ProfitabilityAnalysis(
            opportunity_id=opportunity_id,
            total_cost=total_cost,
            total_value=total_value,
            net_profit=net_profit,
            profitability_status=status,
            cost_breakdown={
                "distance": distance_cost,
                "time": time_cost,
                "complexity": complexity_cost,
                "coordination": coordination_cost,
                "legal": legal_cost,
                "technical": technical_cost
            },
            friction_factors=friction_factors,
            recommendations=recommendations,
            confidence_score=0.8,
            created_at=datetime.now().isoformat()
        )
    
    def _calculate_distance_cost(self, distance_km: float) -> float:
        """Calculate cost based on distance"""
        # Base cost per km
        cost_per_km = 50.0
        return distance_km * cost_per_km
    
    def _calculate_time_cost(self, participants: int, complexity_score: float) -> float:
        """Calculate time-related costs"""
        # Base hourly rate
        hourly_rate = 100.0
        # Estimated hours per participant
        hours_per_participant = 2.0 * complexity_score
        return participants * hours_per_participant * hourly_rate
    
    def _calculate_complexity_cost(self, complexity_score: float) -> float:
        """Calculate complexity-related costs"""
        base_complexity_cost = 500.0
        return base_complexity_cost * complexity_score
    
    def _calculate_coordination_cost(self, participants: int) -> float:
        """Calculate coordination costs"""
        # Coordination cost increases exponentially with participants
        base_coordination_cost = 200.0
        return base_coordination_cost * (participants ** 1.5)
    
    def _calculate_legal_cost(self, risk_factors: str) -> float:
        """Calculate legal/risk-related costs"""
        if not risk_factors:
            return 100.0
        
        risk_levels = {
            "low": 100.0,
            "medium": 500.0,
            "high": 1000.0,
            "critical": 2000.0
        }
        
        return risk_levels.get(risk_factors.lower(), 100.0)
    
    def _calculate_technical_cost(self, complexity_score: float) -> float:
        """Calculate technical implementation costs"""
        base_technical_cost = 300.0
        return base_technical_cost * complexity_score
    
    def _estimate_opportunity_value(self, opportunity_id: str, participants: int, complexity_score: float) -> float:
        """Estimate the value of an opportunity"""
        # Base value per participant
        base_value_per_participant = 1000.0
        # Complexity multiplier
        complexity_multiplier = 1.0 + (complexity_score - 1.0) * 0.5
        
        return participants * base_value_per_participant * complexity_multiplier
    
    def _identify_friction_factors(self, distance_km: float, participants: int, 
                                 complexity_score: float, risk_factors: str) -> List[FrictionFactor]:
        """Identify friction factors affecting the transaction"""
        factors = []
        
        if distance_km > 100:
            factors.append(FrictionFactor.HIGH)
        elif distance_km > 50:
            factors.append(FrictionFactor.MEDIUM)
        else:
            factors.append(FrictionFactor.LOW)
        
        if participants > 10:
            factors.append(FrictionFactor.CRITICAL)
        elif participants > 5:
            factors.append(FrictionFactor.HIGH)
        elif participants > 2:
            factors.append(FrictionFactor.MEDIUM)
        else:
            factors.append(FrictionFactor.LOW)
        
        if complexity_score > 3.0:
            factors.append(FrictionFactor.CRITICAL)
        elif complexity_score > 2.0:
            factors.append(FrictionFactor.HIGH)
        elif complexity_score > 1.5:
            factors.append(FrictionFactor.MEDIUM)
        else:
            factors.append(FrictionFactor.LOW)
        
        if risk_factors and risk_factors.lower() in ["high", "critical"]:
            factors.append(FrictionFactor.CRITICAL)
        
        return factors
    
    def _generate_recommendations(self, total_cost: float, total_value: float, 
                                friction_factors: List[FrictionFactor]) -> List[str]:
        """Generate recommendations based on analysis"""
        recommendations = []
        
        if total_cost > total_value:
            recommendations.append("Consider reducing transaction complexity")
            recommendations.append("Explore virtual collaboration options")
            recommendations.append("Break down into smaller transactions")
        
        if FrictionFactor.CRITICAL in friction_factors:
            recommendations.append("High friction detected - consider alternative approaches")
        
        if FrictionFactor.HIGH in friction_factors:
            recommendations.append("Moderate friction - optimize coordination processes")
        
        if total_value > total_cost * 2:
            recommendations.append("High value opportunity - proceed with confidence")
        
        return recommendations
    
    async def analyze_friction_impact(self, opportunity_id: str, friction_types: str = None) -> Dict:
        """Analyze the impact of specific friction factors"""
        friction_analysis = {
            "opportunity_id": opportunity_id,
            "friction_impact": {},
            "mitigation_strategies": {},
            "created_at": datetime.now().isoformat()
        }
        
        if friction_types:
            for friction_type in friction_types.split(","):
                friction_type = friction_type.strip()
                impact = self._calculate_friction_impact(friction_type)
                mitigation = self._get_mitigation_strategies(friction_type)
                
                friction_analysis["friction_impact"][friction_type] = impact
                friction_analysis["mitigation_strategies"][friction_type] = mitigation
        
        return friction_analysis
    
    def _calculate_friction_impact(self, friction_type: str) -> Dict:
        """Calculate impact of specific friction type"""
        impacts = {
            "distance": {"cost_increase": 0.3, "time_increase": 0.5, "complexity_increase": 0.2},
            "coordination": {"cost_increase": 0.4, "time_increase": 0.6, "complexity_increase": 0.3},
            "complexity": {"cost_increase": 0.5, "time_increase": 0.4, "complexity_increase": 0.8},
            "legal": {"cost_increase": 0.6, "time_increase": 0.3, "complexity_increase": 0.4},
            "technical": {"cost_increase": 0.4, "time_increase": 0.5, "complexity_increase": 0.6}
        }
        
        return impacts.get(friction_type.lower(), {"cost_increase": 0.2, "time_increase": 0.2, "complexity_increase": 0.2})
    
    def _get_mitigation_strategies(self, friction_type: str) -> List[str]:
        """Get mitigation strategies for friction type"""
        strategies = {
            "distance": [
                "Use virtual collaboration tools",
                "Schedule meetings during overlapping hours",
                "Consider hybrid in-person/virtual approach"
            ],
            "coordination": [
                "Appoint a dedicated coordinator",
                "Use project management tools",
                "Establish clear communication protocols"
            ],
            "complexity": [
                "Break down into smaller components",
                "Use standardized templates",
                "Engage subject matter experts"
            ],
            "legal": [
                "Consult legal experts early",
                "Use standard contracts where possible",
                "Document all agreements clearly"
            ],
            "technical": [
                "Use proven technologies",
                "Engage technical experts",
                "Plan for adequate testing time"
            ]
        }
        
        return strategies.get(friction_type.lower(), ["Standard risk mitigation practices"])
    
    async def breakeven_analysis(self, opportunity_id: str, cost_scenarios: str = None) -> Dict:
        """Perform breakeven analysis"""
        scenarios = cost_scenarios.split(",") if cost_scenarios else ["baseline"]
        
        breakeven_results = {
            "opportunity_id": opportunity_id,
            "scenarios": {},
            "recommendations": [],
            "created_at": datetime.now().isoformat()
        }
        
        for scenario in scenarios:
            scenario = scenario.strip()
            
            # Adjust costs based on scenario
            cost_multiplier = self._get_scenario_multiplier(scenario)
            
            # Calculate breakeven point
            base_costs = 1000.0  # Simplified base cost
            adjusted_costs = base_costs * cost_multiplier
            breakeven_value = adjusted_costs
            
            breakeven_results["scenarios"][scenario] = {
                "cost_multiplier": cost_multiplier,
                "adjusted_costs": adjusted_costs,
                "breakeven_value": breakeven_value,
                "risk_level": self._get_risk_level(cost_multiplier)
            }
        
        # Generate recommendations
        breakeven_results["recommendations"] = self._generate_breakeven_recommendations(breakeven_results["scenarios"])
        
        return breakeven_results
    
    def _get_scenario_multiplier(self, scenario: str) -> float:
        """Get cost multiplier for scenario"""
        multipliers = {
            "baseline": 1.0,
            "optimistic": 0.7,
            "pessimistic": 1.5,
            "worst_case": 2.0
        }
        return multipliers.get(scenario.lower(), 1.0)
    
    def _get_risk_level(self, cost_multiplier: float) -> str:
        """Get risk level based on cost multiplier"""
        if cost_multiplier <= 0.8:
            return "low"
        elif cost_multiplier <= 1.2:
            return "medium"
        elif cost_multiplier <= 1.5:
            return "high"
        else:
            return "critical"
    
    def _generate_breakeven_recommendations(self, scenarios: Dict) -> List[str]:
        """Generate recommendations based on breakeven analysis"""
        recommendations = []
        
        baseline = scenarios.get("baseline", {})
        worst_case = scenarios.get("worst_case", {})
        
        if worst_case and baseline:
            if worst_case["breakeven_value"] > baseline["breakeven_value"] * 1.5:
                recommendations.append("High cost variability - consider risk mitigation strategies")
            
            if worst_case["risk_level"] == "critical":
                recommendations.append("Critical risk scenario - ensure adequate contingency planning")
        
        return recommendations 