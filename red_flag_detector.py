"""
RetireUS Checkpoint Quiz - Red Flag Detection Algorithm
--------------------------------------------------------
Paste in quiz responses and get back the red flags that should trigger.
"""

from typing import Dict, List, Set
from dataclasses import dataclass
from enum import Enum


class ServiceTier(Enum):
    BASIC_PLANNING = "Basic Planning"
    TAX_MASTERY = "Tax Mastery"
    WEALTH_MASTERY = "Wealth Mastery"


@dataclass
class RedFlag:
    """Represents a detected red flag"""
    id: str
    name: str
    tier: ServiceTier
    description: str


class RedFlagDetector:
    """
    Detects red flags based on quiz responses.
    
    Usage:
        detector = RedFlagDetector()
        responses = {
            'q2_concerns': ['running_out_of_money', 'not_being_on_pace'],
            'q4_retirement_age': 55,
            'q9_investment_style': 'a',
            # ... etc
        }
        red_flags = detector.detect(responses)
        recommendations = detector.get_recommendations(red_flags)
    """
    
    def __init__(self):
        self.red_flags_found: Set[str] = set()
    
    def detect(self, responses: Dict) -> List[RedFlag]:
        """
        Main detection method. Takes quiz responses and returns triggered red flags.
        
        Args:
            responses: Dictionary of quiz responses
            
        Returns:
            List of RedFlag objects that were triggered
        """
        self.red_flags_found = set()
        detected = []
        
        # BASIC PLANNING RED FLAGS
        detected.extend(self._check_basic_rf1(responses))
        detected.extend(self._check_basic_rf2(responses))
        detected.extend(self._check_basic_rf3(responses))
        detected.extend(self._check_basic_rf4(responses))
        detected.extend(self._check_basic_rf5(responses))
        detected.extend(self._check_basic_rf6(responses))
        detected.extend(self._check_basic_rf7(responses))
        
        # TAX MASTERY RED FLAGS
        detected.extend(self._check_tax_rf1(responses))
        detected.extend(self._check_tax_rf2(responses))
        detected.extend(self._check_tax_rf3(responses))
        detected.extend(self._check_tax_rf4(responses))
        detected.extend(self._check_tax_rf5(responses))
        
        # WEALTH MASTERY RED FLAGS
        detected.extend(self._check_wealth_rf1(responses))
        detected.extend(self._check_wealth_rf2(responses))
        detected.extend(self._check_wealth_rf3(responses))
        
        return detected
    
    # ==================== BASIC PLANNING RED FLAGS ====================
    
    def _check_basic_rf1(self, r: Dict) -> List[RedFlag]:
        """Basic RF1: Haven't Calculated Retirement Goal"""
        conditions = [
            'running_out_of_money' in r.get('q2_concerns', []),
            'not_being_on_pace' in r.get('q2_concerns', []),
            r.get('q_total_savings_needed') == 'no_idea',
            r.get('q_annual_cost') == 'no_idea',
            r.get('timed_q4_on_pace') == 'not_sure',
        ]
        
        if any(conditions):
            rf = RedFlag(
                id='basic_rf1',
                name='Haven\'t Calculated Retirement Goal',
                tier=ServiceTier.BASIC_PLANNING,
                description='User lacks clarity on retirement savings target and timeline'
            )
            self.red_flags_found.add('basic_rf1')
            return [rf]
        return []
    
    def _check_basic_rf2(self, r: Dict) -> List[RedFlag]:
        """Basic RF2: Investment Needs Are Unknown"""
        conditions = [
            'not_being_on_pace' in r.get('q2_concerns', []),
            r.get('timed_q4_on_pace') == 'not_sure',
            r.get('timed_q5_investments_appropriate') == 'should_reevaluate',
            r.get('q_current_progress') == 'savings_not_set_for_retirement',
            r.get('q_current_progress') == 'havent_started_saving',
            r.get('timed_q8_financial_plan') == 'dont_have_one',
        ]
        
        if any(conditions):
            rf = RedFlag(
                id='basic_rf2',
                name='Investment Needs Are Unknown',
                tier=ServiceTier.BASIC_PLANNING,
                description='User is uncertain about investment strategy and retirement readiness'
            )
            self.red_flags_found.add('basic_rf2')
            return [rf]
        return []
    
    def _check_basic_rf3(self, r: Dict) -> List[RedFlag]:
        """Basic RF3: Investments May Be Out Of Alignment"""
        conditions = [
            r.get('q_market_volatility_concern') == 'not_sure_risk_exposure',
            r.get('timed_q8_financial_plan') == 'dont_have_one',
            'market_volatility' in r.get('q2_concerns', []),
            r.get('timed_q_portfolio_crash_loss') == 'no_idea',
        ]
        
        if any(conditions):
            rf = RedFlag(
                id='basic_rf3',
                name='Investments May Be Out Of Alignment',
                tier=ServiceTier.BASIC_PLANNING,
                description='Portfolio may not match risk tolerance or retirement timeline'
            )
            self.red_flags_found.add('basic_rf3')
            return [rf]
        return []
    
    def _check_basic_rf4(self, r: Dict) -> List[RedFlag]:
        """Basic RF4: Market Risk Is HIGH"""
        conditions = [
            r.get('q9_investment_style') == 'a',  # casino everyday
            r.get('timed_q7_market_crash') == 'concerned_stressed',
        ]
        
        if any(conditions):
            rf = RedFlag(
                id='basic_rf4',
                name='Market Risk Is HIGH',
                tier=ServiceTier.BASIC_PLANNING,
                description='User has high exposure to market volatility or risky investment behavior'
            )
            self.red_flags_found.add('basic_rf4')
            return [rf]
        return []
    
    def _check_basic_rf5(self, r: Dict) -> List[RedFlag]:
        """Basic RF5: Inflation Risk Is HIGH"""
        investment_style = r.get('q9_investment_style')
        
        if investment_style in ['c', 'd']:  # income-focused or safe investments
            rf = RedFlag(
                id='basic_rf5',
                name='Inflation Risk Is HIGH',
                tier=ServiceTier.BASIC_PLANNING,
                description='Conservative investment strategy may not keep pace with inflation'
            )
            self.red_flags_found.add('basic_rf5')
            return [rf]
        return []
    
    def _check_basic_rf6(self, r: Dict) -> List[RedFlag]:
        """Basic RF6: Old Employer Plan Limiting Strategy"""
        benefits = r.get('q11_account_types', [])
        
        if 'old_employer_plan' in benefits:
            rf = RedFlag(
                id='basic_rf6',
                name='Old Employer Plan Limiting Strategy',
                tier=ServiceTier.BASIC_PLANNING,
                description='Old employer retirement plans may have limited investment options or high fees'
            )
            self.red_flags_found.add('basic_rf6')
            return [rf]
        return []
    
    def _check_basic_rf7(self, r: Dict) -> List[RedFlag]:
        """Basic RF7: Limited Compounding Savings"""
        annual_savings = r.get('q10_annual_savings', 0)
        
        if annual_savings <= 10000:
            rf = RedFlag(
                id='basic_rf7',
                name='Limited Compounding Savings',
                tier=ServiceTier.BASIC_PLANNING,
                description='Low annual savings rate may not be sufficient for retirement goals'
            )
            self.red_flags_found.add('basic_rf7')
            return [rf]
        return []
    
    # ==================== TAX MASTERY RED FLAGS ====================
    
    def _check_tax_rf1(self, r: Dict) -> List[RedFlag]:
        """Tax RF1: You May Face Tax Penalties"""
        retirement_age = r.get('q4_retirement_age', 65)
        
        if retirement_age < 59:
            rf = RedFlag(
                id='tax_rf1',
                name='You May Face Tax Penalties',
                tier=ServiceTier.TAX_MASTERY,
                description='Early retirement may trigger penalty taxes on retirement account withdrawals'
            )
            self.red_flags_found.add('tax_rf1')
            return [rf]
        return []
    
    def _check_tax_rf2(self, r: Dict) -> List[RedFlag]:
        """Tax RF2: RMDs Need To Be Evaluated"""
        retirement_age = r.get('q4_retirement_age', 65)
        pension_income = r.get('q8b_pension_income', 0)
        has_pension = 'pension' in r.get('q8_work_benefits', [])
        current_progress = r.get('q_current_progress', '')
        
        conditions = [
            retirement_age > 67,
            r.get('q_tax_concern') == 'not_much_tax_free_savings',
            r.get('timed_q6_rmd_planning') == 'no_unclear',
            (has_pension and current_progress == 'only_employer_account'),
            (has_pension and current_progress == 'multiple_retirement_accounts'),
            pension_income >= 75000,
        ]
        
        if any(conditions):
            rf = RedFlag(
                id='tax_rf2',
                name='RMDs Need To Be Evaluated',
                tier=ServiceTier.TAX_MASTERY,
                description='Required Minimum Distributions may create unexpected tax burden'
            )
            self.red_flags_found.add('tax_rf2')
            return [rf]
        return []
    
    def _check_tax_rf3(self, r: Dict) -> List[RedFlag]:
        """Tax RF3: Limited Tax Diversification"""
        conditions = [
            r.get('q_tax_concern') == 'lot_in_pretax_accounts',
            r.get('q_tax_concern') == 'not_much_tax_free_savings',
            r.get('q_current_progress') == 'only_employer_account',
        ]
        
        if any(conditions):
            rf = RedFlag(
                id='tax_rf3',
                name='Limited Tax Diversification',
                tier=ServiceTier.TAX_MASTERY,
                description='Retirement savings may be concentrated in single tax treatment category'
            )
            self.red_flags_found.add('tax_rf3')
            return [rf]
        return []
    
    def _check_tax_rf4(self, r: Dict) -> List[RedFlag]:
        """Tax RF4: No Tax-Sheltered Growth"""
        account_types = r.get('q11_account_types', [])
        
        has_roth = 'roth_accounts' in account_types
        has_whole_life = 'whole_life' in account_types
        
        if not has_roth and not has_whole_life:
            rf = RedFlag(
                id='tax_rf4',
                name='No Tax-Sheltered Growth',
                tier=ServiceTier.TAX_MASTERY,
                description='Missing tax-free growth opportunities like Roth accounts or life insurance'
            )
            self.red_flags_found.add('tax_rf4')
            return [rf]
        return []
    
    def _check_tax_rf5(self, r: Dict) -> List[RedFlag]:
        """Tax RF5: Retirement Tax Liability Unknown"""
        conditions = [
            'paying_too_much_taxes' in r.get('q2_concerns', []),
            r.get('timed_q6_rmd_planning') == 'no_unclear',
        ]
        
        if any(conditions):
            rf = RedFlag(
                id='tax_rf5',
                name='Retirement Tax Liability Unknown',
                tier=ServiceTier.TAX_MASTERY,
                description='User lacks understanding of future tax obligations in retirement'
            )
            self.red_flags_found.add('tax_rf5')
            return [rf]
        return []
    
    # ==================== WEALTH MASTERY RED FLAGS ====================
    
    def _check_wealth_rf1(self, r: Dict) -> List[RedFlag]:
        """Wealth RF1: Possible Estate Planning Risks"""
        total_savings = r.get('q12_total_savings', 0)
        
        if total_savings > 2000000:
            rf = RedFlag(
                id='wealth_rf1',
                name='Possible Estate Planning Risks',
                tier=ServiceTier.WEALTH_MASTERY,
                description='High net worth may require estate tax planning and wealth transfer strategies'
            )
            self.red_flags_found.add('wealth_rf1')
            return [rf]
        return []
    
    def _check_wealth_rf2(self, r: Dict) -> List[RedFlag]:
        """Wealth RF2: Benefits With Unique Tax Implications"""
        benefits = r.get('q8_work_benefits', [])
        
        if 'deferred_compensation' in benefits or 'stock_options' in benefits:
            rf = RedFlag(
                id='wealth_rf2',
                name='Benefits With Unique Tax Implications',
                tier=ServiceTier.WEALTH_MASTERY,
                description='Executive compensation requires specialized tax and timing strategies'
            )
            self.red_flags_found.add('wealth_rf2')
            return [rf]
        return []
    
    def _check_wealth_rf3(self, r: Dict) -> List[RedFlag]:
        """Wealth RF3: Single Equity Risk Exposure High"""
        benefits = r.get('q8_work_benefits', [])
        
        if 'stock_options' in benefits:
            rf = RedFlag(
                id='wealth_rf3',
                name='Single Equity Risk Exposure High',
                tier=ServiceTier.WEALTH_MASTERY,
                description='Concentrated stock positions create significant portfolio risk'
            )
            self.red_flags_found.add('wealth_rf3')
            return [rf]
        return []
    
    # ==================== RECOMMENDATION ENGINE ====================
    
    def get_recommendations(self, red_flags: List[RedFlag]) -> Dict[ServiceTier, List[RedFlag]]:
        """
        Determine which service tiers to recommend based on red flags.
        
        Rules:
        - Basic Planning: Recommend if ANY basic red flags present
        - Tax Mastery: Recommend if 2+ tax red flags present
        - Wealth Mastery: Recommend if 1+ wealth red flags present
        
        Returns:
            Dictionary mapping ServiceTier to list of red flags in that tier
        """
        basic_flags = [rf for rf in red_flags if rf.tier == ServiceTier.BASIC_PLANNING]
        tax_flags = [rf for rf in red_flags if rf.tier == ServiceTier.TAX_MASTERY]
        wealth_flags = [rf for rf in red_flags if rf.tier == ServiceTier.WEALTH_MASTERY]
        
        recommendations = {}
        
        # Basic Planning: ANY red flags
        if len(basic_flags) > 0:
            recommendations[ServiceTier.BASIC_PLANNING] = basic_flags
        
        # Tax Mastery: 2+ red flags
        if len(tax_flags) >= 2:
            recommendations[ServiceTier.TAX_MASTERY] = tax_flags
        
        # Wealth Mastery: 1+ red flags
        if len(wealth_flags) >= 1:
            recommendations[ServiceTier.WEALTH_MASTERY] = wealth_flags
        
        return recommendations
    
    def print_results(self, red_flags: List[RedFlag], recommendations: Dict[ServiceTier, List[RedFlag]]):
        """Pretty print the detection results"""
        print("\n" + "="*80)
        print("RED FLAG DETECTION RESULTS")
        print("="*80)
        
        if not red_flags:
            print("\n✅ No red flags detected! User appears to be on track.")
            return
        
        print(f"\n📊 TOTAL RED FLAGS DETECTED: {len(red_flags)}")
        
        # Group by tier
        by_tier = {}
        for rf in red_flags:
            if rf.tier not in by_tier:
                by_tier[rf.tier] = []
            by_tier[rf.tier].append(rf)
        
        # Print each tier
        for tier in [ServiceTier.BASIC_PLANNING, ServiceTier.TAX_MASTERY, ServiceTier.WEALTH_MASTERY]:
            if tier in by_tier:
                print(f"\n{'─'*80}")
                print(f"🚩 {tier.value.upper()} ({len(by_tier[tier])} flags)")
                print(f"{'─'*80}")
                for rf in by_tier[tier]:
                    print(f"\n  • {rf.id.upper()}: {rf.name}")
                    print(f"    └─ {rf.description}")
        
        # Print recommendations
        print(f"\n{'='*80}")
        print("💡 RECOMMENDED SERVICES")
        print(f"{'='*80}")
        
        if not recommendations:
            print("\n  No service recommendations triggered.")
        else:
            for tier, flags in recommendations.items():
                print(f"\n  ✓ {tier.value}")
                print(f"    Triggered by {len(flags)} red flag(s)")
        
        print("\n" + "="*80 + "\n")


# ==================== HELPER FUNCTION ====================

def analyze_quiz_responses(responses: Dict) -> None:
    """
    Main function to analyze quiz responses.
    
    Args:
        responses: Dictionary of quiz responses (see format below)
    """
    detector = RedFlagDetector()
    red_flags = detector.detect(responses)
    recommendations = detector.get_recommendations(red_flags)
    detector.print_results(red_flags, recommendations)
    
    return red_flags, recommendations


# ==================== EXAMPLE USAGE ====================

if __name__ == "__main__":
    print("\n" + "="*80)
    print("RETIREUS RED FLAG DETECTOR - TEST EXAMPLES")
    print("="*80)
    
    # Example 1: User with multiple basic planning issues
    print("\n\n📋 EXAMPLE 1: Young professional, hasn't started planning")
    print("-" * 80)
    
    example1 = {
        'q2_concerns': ['running_out_of_money', 'not_being_on_pace'],
        'q4_retirement_age': 55,  # Early retirement
        'q9_investment_style': 'a',  # Risky investing
        'q10_annual_savings': 5000,  # Low savings
        'q11_account_types': ['old_employer_plan'],
        'q12_total_savings': 50000,
        'timed_q4_on_pace': 'not_sure',
        'timed_q7_market_crash': 'concerned_stressed',
        'timed_q8_financial_plan': 'dont_have_one',
    }
    
    analyze_quiz_responses(example1)
    
    # Example 2: High earner with tax concerns
    print("\n\n📋 EXAMPLE 2: High earner approaching retirement, tax issues")
    print("-" * 80)
    
    example2 = {
        'q2_concerns': ['paying_too_much_taxes'],
        'q4_retirement_age': 68,  # Late retirement
        'q8_work_benefits': ['pension', 'deferred_compensation', 'stock_options'],
        'q8b_pension_income': 80000,  # High pension
        'q9_investment_style': 'b',
        'q10_annual_savings': 30000,
        'q11_account_types': ['old_employer_plan'],  # No Roth or Whole Life
        'q12_total_savings': 2500000,  # High net worth
        'q_current_progress': 'multiple_retirement_accounts',
        'timed_q6_rmd_planning': 'no_unclear',
    }
    
    analyze_quiz_responses(example2)
    
    # Example 3: Conservative investor with inflation risk
    print("\n\n📋 EXAMPLE 3: Conservative investor, inflation concerns")
    print("-" * 80)
    
    example3 = {
        'q2_concerns': ['market_volatility'],
        'q4_retirement_age': 62,
        'q9_investment_style': 'd',  # Safe investments
        'q10_annual_savings': 15000,
        'q11_account_types': ['roth_accounts', 'whole_life'],
        'q12_total_savings': 500000,
        'timed_q5_investments_appropriate': 'should_reevaluate',
        'timed_q8_financial_plan': 'very_clear',
    }
    
    analyze_quiz_responses(example3)
