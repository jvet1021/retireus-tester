"""
RetireUS Checkpoint Quiz - Test Scenarios for QA
=================================================

These test cases cover all red flag combinations and edge cases.
Interns should run these scenarios in dev/production to validate the logic.

TEST INSTRUCTIONS:
1. Copy the response dictionary for each test case
2. Paste into the red_flag_detector.py analyzer
3. Compare the detected red flags with the EXPECTED RESULTS
4. Mark PASS/FAIL in your test tracking sheet
"""

from red_flag_detector import analyze_quiz_responses, ServiceTier

# ============================================================================
# SECTION 1: BASIC PLANNING RED FLAGS (Individual Tests)
# ============================================================================

def test_basic_rf1_running_out_of_money():
    """
    TEST: Basic RF1 - Haven't Calculated Retirement Goal (Trigger: running out of money concern)
    EXPECTED: Basic RF1 triggered
    EXPECTED RECOMMENDATION: Basic Planning
    """
    print("\n" + "="*80)
    print("TEST: Basic RF1 - Running Out of Money Concern")
    print("="*80)
    
    responses = {
        'q2_concerns': ['running_out_of_money'],
        'q4_retirement_age': 65,
        'q9_investment_style': 'b',
        'q10_annual_savings': 15000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 300000,
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: basic_rf1 triggered")
    print("✅ EXPECTED: Basic Planning recommended")


def test_basic_rf2_investment_uncertainty():
    """
    TEST: Basic RF2 - Investment Needs Are Unknown
    EXPECTED: Basic RF2 triggered
    EXPECTED RECOMMENDATION: Basic Planning
    """
    print("\n" + "="*80)
    print("TEST: Basic RF2 - Investment Needs Unknown")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 65,
        'q9_investment_style': 'b',
        'q10_annual_savings': 15000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 300000,
        'timed_q5_investments_appropriate': 'should_reevaluate',
        'timed_q8_financial_plan': 'dont_have_one',
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: basic_rf2 triggered")
    print("✅ EXPECTED: Basic Planning recommended")


def test_basic_rf3_market_volatility():
    """
    TEST: Basic RF3 - Investments May Be Out Of Alignment
    EXPECTED: Basic RF3 triggered
    EXPECTED RECOMMENDATION: Basic Planning
    """
    print("\n" + "="*80)
    print("TEST: Basic RF3 - Market Volatility Concern")
    print("="*80)
    
    responses = {
        'q2_concerns': ['market_volatility'],
        'q4_retirement_age': 65,
        'q9_investment_style': 'b',
        'q10_annual_savings': 15000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 300000,
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: basic_rf3 triggered")
    print("✅ EXPECTED: Basic Planning recommended")


def test_basic_rf4_high_market_risk():
    """
    TEST: Basic RF4 - Market Risk Is HIGH
    EXPECTED: Basic RF4 triggered
    EXPECTED RECOMMENDATION: Basic Planning
    """
    print("\n" + "="*80)
    print("TEST: Basic RF4 - High Market Risk (Casino Investor)")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 65,
        'q9_investment_style': 'a',  # Casino everyday
        'q10_annual_savings': 15000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 300000,
        'timed_q7_market_crash': 'concerned_stressed',
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: basic_rf4 triggered")
    print("✅ EXPECTED: Basic Planning recommended")


def test_basic_rf5_inflation_risk():
    """
    TEST: Basic RF5 - Inflation Risk Is HIGH
    EXPECTED: Basic RF5 triggered
    EXPECTED RECOMMENDATION: Basic Planning
    """
    print("\n" + "="*80)
    print("TEST: Basic RF5 - High Inflation Risk (Conservative Investor)")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 65,
        'q9_investment_style': 'd',  # Safe investments
        'q10_annual_savings': 15000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 300000,
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: basic_rf5 triggered")
    print("✅ EXPECTED: Basic Planning recommended")


def test_basic_rf6_old_employer_plan():
    """
    TEST: Basic RF6 - Old Employer Plan Limiting Strategy
    EXPECTED: Basic RF6 triggered
    EXPECTED RECOMMENDATION: Basic Planning
    """
    print("\n" + "="*80)
    print("TEST: Basic RF6 - Old Employer Plan")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 65,
        'q9_investment_style': 'b',
        'q10_annual_savings': 15000,
        'q11_account_types': ['old_employer_plan'],
        'q12_total_savings': 300000,
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: basic_rf6 triggered")
    print("✅ EXPECTED: Basic Planning recommended")


def test_basic_rf7_limited_savings():
    """
    TEST: Basic RF7 - Limited Compounding Savings
    EXPECTED: Basic RF7 triggered
    EXPECTED RECOMMENDATION: Basic Planning
    """
    print("\n" + "="*80)
    print("TEST: Basic RF7 - Limited Annual Savings")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 65,
        'q9_investment_style': 'b',
        'q10_annual_savings': 5000,  # Low savings
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 300000,
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: basic_rf7 triggered")
    print("✅ EXPECTED: Basic Planning recommended")


# ============================================================================
# SECTION 2: TAX MASTERY RED FLAGS (Individual Tests)
# ============================================================================

def test_tax_rf1_early_retirement():
    """
    TEST: Tax RF1 - You May Face Tax Penalties
    EXPECTED: Tax RF1 triggered
    NOTE: Need 2+ tax flags for Tax Mastery recommendation
    """
    print("\n" + "="*80)
    print("TEST: Tax RF1 - Early Retirement Penalty Risk")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 55,  # Early retirement
        'q9_investment_style': 'b',
        'q10_annual_savings': 15000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 300000,
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: tax_rf1 triggered")
    print("❌ EXPECTED: Tax Mastery NOT recommended (need 2+ tax flags)")


def test_tax_rf2_rmd_concerns():
    """
    TEST: Tax RF2 - RMDs Need To Be Evaluated
    EXPECTED: Tax RF2 triggered
    """
    print("\n" + "="*80)
    print("TEST: Tax RF2 - RMD Planning Needed")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 70,  # Late retirement
        'q9_investment_style': 'b',
        'q10_annual_savings': 15000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 300000,
        'timed_q6_rmd_planning': 'no_unclear',
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: tax_rf2 triggered")
    print("❌ EXPECTED: Tax Mastery NOT recommended (need 2+ tax flags)")


def test_tax_rf3_no_tax_diversification():
    """
    TEST: Tax RF3 - Limited Tax Diversification
    EXPECTED: Tax RF3 triggered
    """
    print("\n" + "="*80)
    print("TEST: Tax RF3 - Limited Tax Diversification")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 65,
        'q9_investment_style': 'b',
        'q10_annual_savings': 15000,
        'q11_account_types': ['old_employer_plan'],
        'q12_total_savings': 300000,
        'q_current_progress': 'only_employer_account',
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: tax_rf3 triggered")
    print("❌ EXPECTED: Tax Mastery NOT recommended (need 2+ tax flags)")


def test_tax_rf4_no_tax_sheltered_growth():
    """
    TEST: Tax RF4 - No Tax-Sheltered Growth
    EXPECTED: Tax RF4 triggered
    """
    print("\n" + "="*80)
    print("TEST: Tax RF4 - No Roth or Whole Life")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 65,
        'q9_investment_style': 'b',
        'q10_annual_savings': 15000,
        'q11_account_types': ['old_employer_plan'],  # No Roth or Whole Life
        'q12_total_savings': 300000,
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: tax_rf4 triggered")
    print("❌ EXPECTED: Tax Mastery NOT recommended (need 2+ tax flags)")


def test_tax_rf5_tax_liability_unknown():
    """
    TEST: Tax RF5 - Retirement Tax Liability Unknown
    EXPECTED: Tax RF5 triggered
    """
    print("\n" + "="*80)
    print("TEST: Tax RF5 - Tax Liability Unknown")
    print("="*80)
    
    responses = {
        'q2_concerns': ['paying_too_much_taxes'],
        'q4_retirement_age': 65,
        'q9_investment_style': 'b',
        'q10_annual_savings': 15000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 300000,
        'timed_q6_rmd_planning': 'no_unclear',
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: tax_rf5 triggered")
    print("❌ EXPECTED: Tax Mastery NOT recommended (need 2+ tax flags)")


# ============================================================================
# SECTION 3: WEALTH MASTERY RED FLAGS (Individual Tests)
# ============================================================================

def test_wealth_rf1_estate_planning():
    """
    TEST: Wealth RF1 - Possible Estate Planning Risks
    EXPECTED: Wealth RF1 triggered
    EXPECTED RECOMMENDATION: Wealth Mastery
    """
    print("\n" + "="*80)
    print("TEST: Wealth RF1 - High Net Worth Estate Planning")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 65,
        'q9_investment_style': 'b',
        'q10_annual_savings': 50000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 2500000,  # High net worth
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: wealth_rf1 triggered")
    print("✅ EXPECTED: Wealth Mastery recommended")


def test_wealth_rf2_executive_compensation():
    """
    TEST: Wealth RF2 - Benefits With Unique Tax Implications
    EXPECTED: Wealth RF2 triggered
    EXPECTED RECOMMENDATION: Wealth Mastery
    """
    print("\n" + "="*80)
    print("TEST: Wealth RF2 - Executive Compensation")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 65,
        'q8_work_benefits': ['deferred_compensation', 'stock_options'],
        'q9_investment_style': 'b',
        'q10_annual_savings': 50000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 800000,
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: wealth_rf2 triggered")
    print("✅ EXPECTED: Wealth Mastery recommended")


def test_wealth_rf3_stock_concentration():
    """
    TEST: Wealth RF3 - Single Equity Risk Exposure High
    EXPECTED: Wealth RF3 triggered
    EXPECTED RECOMMENDATION: Wealth Mastery
    """
    print("\n" + "="*80)
    print("TEST: Wealth RF3 - Stock Options Concentration Risk")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 65,
        'q8_work_benefits': ['stock_options'],
        'q9_investment_style': 'b',
        'q10_annual_savings': 30000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 600000,
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: wealth_rf3 triggered")
    print("✅ EXPECTED: Wealth Mastery recommended")


# ============================================================================
# SECTION 4: MULTI-TIER SCENARIOS (Complex Cases)
# ============================================================================

def test_scenario_young_professional():
    """
    TEST SCENARIO: Young professional, just starting out
    EXPECTED: Multiple Basic Planning flags, Tax RF1
    EXPECTED RECOMMENDATION: Basic Planning only (need 2+ tax flags)
    """
    print("\n" + "="*80)
    print("SCENARIO: Young Professional Starting Career")
    print("="*80)
    
    responses = {
        'q2_concerns': ['running_out_of_money', 'not_being_on_pace'],
        'q4_retirement_age': 55,  # Early retirement
        'q9_investment_style': 'a',  # Risky
        'q10_annual_savings': 3000,  # Low savings
        'q11_account_types': [],  # No accounts
        'q12_total_savings': 10000,  # Just starting
        'timed_q4_on_pace': 'not_sure',
        'timed_q5_investments_appropriate': 'should_reevaluate',
        'timed_q7_market_crash': 'concerned_stressed',
        'timed_q8_financial_plan': 'dont_have_one',
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: Multiple basic_rf flags (1, 2, 3, 4, 7)")
    print("✅ EXPECTED: tax_rf1, tax_rf4")
    print("✅ EXPECTED: Basic Planning recommended")
    print("❌ EXPECTED: Tax Mastery NOT recommended (need 2+ tax flags)")


def test_scenario_high_earner_approaching_retirement():
    """
    TEST SCENARIO: High earner with executive comp, approaching retirement
    EXPECTED: Tax Mastery + Wealth Mastery recommendations
    """
    print("\n" + "="*80)
    print("SCENARIO: High Earner Approaching Retirement")
    print("="*80)
    
    responses = {
        'q2_concerns': ['paying_too_much_taxes'],
        'q4_retirement_age': 68,  # Late retirement
        'q8_work_benefits': ['pension', 'deferred_compensation', 'stock_options'],
        'q8b_pension_income': 80000,
        'q9_investment_style': 'b',
        'q10_annual_savings': 50000,
        'q11_account_types': ['old_employer_plan'],  # No Roth/Whole Life
        'q12_total_savings': 2500000,  # High net worth
        'q_current_progress': 'multiple_retirement_accounts',
        'timed_q6_rmd_planning': 'no_unclear',
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: basic_rf6")
    print("✅ EXPECTED: tax_rf2, tax_rf4, tax_rf5 (3 tax flags)")
    print("✅ EXPECTED: wealth_rf1, wealth_rf2, wealth_rf3 (3 wealth flags)")
    print("✅ EXPECTED: Basic Planning, Tax Mastery, AND Wealth Mastery recommended")


def test_scenario_conservative_mid_career():
    """
    TEST SCENARIO: Mid-career conservative investor
    EXPECTED: Basic Planning for inflation risk
    """
    print("\n" + "="*80)
    print("SCENARIO: Conservative Mid-Career Investor")
    print("="*80)
    
    responses = {
        'q2_concerns': ['market_volatility'],
        'q4_retirement_age': 62,
        'q9_investment_style': 'd',  # Safe investments
        'q10_annual_savings': 18000,
        'q11_account_types': ['roth_accounts', 'whole_life'],
        'q12_total_savings': 600000,
        'timed_q8_financial_plan': 'very_clear',
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: basic_rf3, basic_rf5")
    print("✅ EXPECTED: Basic Planning recommended")
    print("❌ EXPECTED: No Tax Mastery (no tax flags)")
    print("❌ EXPECTED: No Wealth Mastery (no wealth flags)")


def test_scenario_optimal_planner():
    """
    TEST SCENARIO: Well-planned individual with good diversification
    EXPECTED: Minimal or no red flags
    """
    print("\n" + "="*80)
    print("SCENARIO: Optimal Retirement Planner")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 65,
        'q9_investment_style': 'b',  # Moderate
        'q10_annual_savings': 25000,
        'q11_account_types': ['roth_accounts', 'whole_life'],
        'q12_total_savings': 1200000,
        'timed_q4_on_pace': 'calculated_target',
        'timed_q5_investments_appropriate': 'risk_return_target',
        'timed_q6_rmd_planning': 'yes_long_term_plan',
        'timed_q8_financial_plan': 'very_clear',
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: No red flags OR minimal flags")
    print("❌ EXPECTED: Possibly no recommendations")


def test_scenario_tax_mastery_threshold():
    """
    TEST SCENARIO: Edge case - exactly 2 tax flags (threshold for recommendation)
    EXPECTED: Tax Mastery recommended
    """
    print("\n" + "="*80)
    print("SCENARIO: Tax Mastery Threshold Test (Exactly 2 Tax Flags)")
    print("="*80)
    
    responses = {
        'q2_concerns': ['paying_too_much_taxes'],
        'q4_retirement_age': 57,  # Early retirement (tax_rf1)
        'q9_investment_style': 'b',
        'q10_annual_savings': 20000,
        'q11_account_types': ['old_employer_plan'],  # No Roth/Whole Life (tax_rf4)
        'q12_total_savings': 800000,
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: tax_rf1, tax_rf4 (exactly 2 tax flags)")
    print("✅ EXPECTED: Tax Mastery recommended (threshold met)")


def test_scenario_single_tax_flag():
    """
    TEST SCENARIO: Edge case - only 1 tax flag (below threshold)
    EXPECTED: Tax Mastery NOT recommended
    """
    print("\n" + "="*80)
    print("SCENARIO: Single Tax Flag (Below Threshold)")
    print("="*80)
    
    responses = {
        'q2_concerns': [],
        'q4_retirement_age': 57,  # Early retirement (tax_rf1 only)
        'q9_investment_style': 'b',
        'q10_annual_savings': 20000,
        'q11_account_types': ['roth_accounts', 'whole_life'],  # Has tax-sheltered
        'q12_total_savings': 800000,
    }
    
    analyze_quiz_responses(responses)
    
    print("\n✅ EXPECTED: tax_rf1 (only 1 tax flag)")
    print("❌ EXPECTED: Tax Mastery NOT recommended (need 2+)")


# ============================================================================
# SECTION 5: EDGE CASES & BOUNDARY TESTS
# ============================================================================

def test_edge_case_age_boundaries():
    """
    TEST: Age boundary conditions
    - Age 58: No tax_rf1 (need < 59)
    - Age 59: No tax_rf1
    - Age 67: No tax_rf2 (need > 67)
    - Age 68: Yes tax_rf2
    """
    print("\n" + "="*80)
    print("EDGE CASE: Age Boundaries for Tax RFs")
    print("="*80)
    
    print("\n--- Testing Age 58 (just below early withdrawal threshold) ---")
    responses_58 = {
        'q4_retirement_age': 58,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 500000,
    }
    analyze_quiz_responses(responses_58)
    print("✅ EXPECTED: tax_rf1 triggered (< 59)")
    
    print("\n--- Testing Age 59 (at threshold) ---")
    responses_59 = {
        'q4_retirement_age': 59,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 500000,
    }
    analyze_quiz_responses(responses_59)
    print("✅ EXPECTED: NO tax_rf1 (>= 59)")
    
    print("\n--- Testing Age 67 (at RMD threshold) ---")
    responses_67 = {
        'q4_retirement_age': 67,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 500000,
    }
    analyze_quiz_responses(responses_67)
    print("✅ EXPECTED: NO tax_rf2 (need > 67)")
    
    print("\n--- Testing Age 68 (above RMD threshold) ---")
    responses_68 = {
        'q4_retirement_age': 68,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 500000,
    }
    analyze_quiz_responses(responses_68)
    print("✅ EXPECTED: tax_rf2 triggered (> 67)")


def test_edge_case_savings_boundaries():
    """
    TEST: Savings amount boundaries
    - $10,000: Yes basic_rf7 (threshold)
    - $10,001: No basic_rf7
    - $2,000,000: No wealth_rf1 (threshold)
    - $2,000,001: Yes wealth_rf1
    """
    print("\n" + "="*80)
    print("EDGE CASE: Savings Boundaries")
    print("="*80)
    
    print("\n--- Testing $10,000 annual savings (at threshold) ---")
    responses_10k = {
        'q4_retirement_age': 65,
        'q10_annual_savings': 10000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 500000,
    }
    analyze_quiz_responses(responses_10k)
    print("✅ EXPECTED: basic_rf7 triggered (<= 10k)")
    
    print("\n--- Testing $10,001 annual savings (just above threshold) ---")
    responses_10k_plus = {
        'q4_retirement_age': 65,
        'q10_annual_savings': 10001,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 500000,
    }
    analyze_quiz_responses(responses_10k_plus)
    print("✅ EXPECTED: NO basic_rf7 (> 10k)")
    
    print("\n--- Testing $2,000,000 total savings (at threshold) ---")
    responses_2m = {
        'q4_retirement_age': 65,
        'q10_annual_savings': 20000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 2000000,
    }
    analyze_quiz_responses(responses_2m)
    print("✅ EXPECTED: NO wealth_rf1 (need > 2M)")
    
    print("\n--- Testing $2,000,001 total savings (just above threshold) ---")
    responses_2m_plus = {
        'q4_retirement_age': 65,
        'q10_annual_savings': 20000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 2000001,
    }
    analyze_quiz_responses(responses_2m_plus)
    print("✅ EXPECTED: wealth_rf1 triggered (> 2M)")


def test_edge_case_pension_combinations():
    """
    TEST: Pension-related tax RF2 combinations
    Testing various pension + account status combinations
    """
    print("\n" + "="*80)
    print("EDGE CASE: Pension Income Combinations")
    print("="*80)
    
    print("\n--- Pension $74,999 (below threshold) ---")
    responses_pension_low = {
        'q4_retirement_age': 65,
        'q8_work_benefits': ['pension'],
        'q8b_pension_income': 74999,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 500000,
    }
    analyze_quiz_responses(responses_pension_low)
    print("✅ EXPECTED: NO tax_rf2 from pension amount (< 75k)")
    
    print("\n--- Pension $75,000 (at threshold) ---")
    responses_pension_threshold = {
        'q4_retirement_age': 65,
        'q8_work_benefits': ['pension'],
        'q8b_pension_income': 75000,
        'q11_account_types': ['roth_accounts'],
        'q12_total_savings': 500000,
    }
    analyze_quiz_responses(responses_pension_threshold)
    print("✅ EXPECTED: tax_rf2 triggered (>= 75k)")


# ============================================================================
# SECTION 6: RUN ALL TESTS
# ============================================================================

def run_all_basic_tests():
    """Run all individual Basic Planning RF tests"""
    print("\n\n" + "#"*80)
    print("# SECTION 1: BASIC PLANNING RED FLAGS")
    print("#"*80)
    
    test_basic_rf1_running_out_of_money()
    test_basic_rf2_investment_uncertainty()
    test_basic_rf3_market_volatility()
    test_basic_rf4_high_market_risk()
    test_basic_rf5_inflation_risk()
    test_basic_rf6_old_employer_plan()
    test_basic_rf7_limited_savings()


def run_all_tax_tests():
    """Run all individual Tax Mastery RF tests"""
    print("\n\n" + "#"*80)
    print("# SECTION 2: TAX MASTERY RED FLAGS")
    print("#"*80)
    
    test_tax_rf1_early_retirement()
    test_tax_rf2_rmd_concerns()
    test_tax_rf3_no_tax_diversification()
    test_tax_rf4_no_tax_sheltered_growth()
    test_tax_rf5_tax_liability_unknown()


def run_all_wealth_tests():
    """Run all individual Wealth Mastery RF tests"""
    print("\n\n" + "#"*80)
    print("# SECTION 3: WEALTH MASTERY RED FLAGS")
    print("#"*80)
    
    test_wealth_rf1_estate_planning()
    test_wealth_rf2_executive_compensation()
    test_wealth_rf3_stock_concentration()


def run_all_scenario_tests():
    """Run all multi-tier scenario tests"""
    print("\n\n" + "#"*80)
    print("# SECTION 4: MULTI-TIER SCENARIOS")
    print("#"*80)
    
    test_scenario_young_professional()
    test_scenario_high_earner_approaching_retirement()
    test_scenario_conservative_mid_career()
    test_scenario_optimal_planner()
    test_scenario_tax_mastery_threshold()
    test_scenario_single_tax_flag()


def run_all_edge_case_tests():
    """Run all edge case and boundary tests"""
    print("\n\n" + "#"*80)
    print("# SECTION 5: EDGE CASES & BOUNDARY TESTS")
    print("#"*80)
    
    test_edge_case_age_boundaries()
    test_edge_case_savings_boundaries()
    test_edge_case_pension_combinations()


def run_full_test_suite():
    """Run the complete test suite"""
    print("\n" + "="*80)
    print("RETIREUS CHECKPOINT QUIZ - FULL TEST SUITE")
    print("="*80)
    print("\nRunning comprehensive red flag detection tests...")
    print("Interns: Compare actual results with EXPECTED results for each test.\n")
    
    run_all_basic_tests()
    run_all_tax_tests()
    run_all_wealth_tests()
    run_all_scenario_tests()
    run_all_edge_case_tests()
    
    print("\n\n" + "="*80)
    print("TEST SUITE COMPLETE")
    print("="*80)
    print("\nInstructions for QA team:")
    print("1. Mark each test as PASS/FAIL based on expected vs actual results")
    print("2. Document any discrepancies in your test tracking sheet")
    print("3. Report all failures to the development team")
    print("4. Re-run failed tests after fixes are deployed")
    print("\n")


if __name__ == "__main__":
    # Run the full test suite
    run_full_test_suite()
