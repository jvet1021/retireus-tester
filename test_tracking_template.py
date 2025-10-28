"""
RetireUS Red Flag Analyzer - PASTE YOUR DATA HERE
==================================================

USAGE:
1. Get quiz responses from your database/API
2. Paste them into the test_responses dictionary below
3. Run this file: python analyze_user_responses.py
4. Get instant red flag analysis

"""

from red_flag_detector import analyze_quiz_responses

# ============================================================================
# PASTE YOUR QUIZ RESPONSES HERE
# ============================================================================

test_responses = {
    # Question 2: What concerns you about your ability to retire? (multi-select)
    # Options: 'running_out_of_money', 'not_being_on_pace', 'market_volatility', 'paying_too_much_taxes'
    'q2_concerns': ['running_out_of_money', 'not_being_on_pace'],
    
    # Question 4: At what age do you want to retire? (number)
    'q4_retirement_age': 65,
    
    # Question 8: Do you receive any of the following work benefits? (multi-select)
    # Options: 'pension', 'deferred_compensation', 'stock_options', 'none'
    'q8_work_benefits': [],
    
    # Question 8b (CONDITIONAL): What is your estimated pension income? (number)
    # Only appears if 'pension' selected in q8
    'q8b_pension_income': 0,
    
    # Question 9: How would you describe your investment style? (single choice)
    # Options: 'a' (casino), 'b' (moderate), 'c' (income), 'd' (safe)
    'q9_investment_style': 'b',
    
    # Question 10: How much are you saving each year for retirement? (number)
    'q10_annual_savings': 15000,
    
    # Question 11: Do you have any of the following? (multi-select)
    # Options: 'roth_accounts', 'whole_life', 'annuity_contracts', 'old_employer_plan', 'none'
    'q11_account_types': ['roth_accounts'],
    
    # Question 12: Roughly how much do you have in total investment savings? (number)
    'q12_total_savings': 500000,
    
    # TIMED QUESTIONS (rapid fire section)
    # Timed Q4: How do you know if you are on pace?
    # Options: 'calculated_target', 'not_sure'
    'timed_q4_on_pace': 'not_sure',
    
    # Timed Q5: How do you know if investments are appropriate?
    # Options: 'risk_return_target', 'should_reevaluate'
    'timed_q5_investments_appropriate': 'should_reevaluate',
    
    # Timed Q6: Have you done any RMD planning?
    # Options: 'yes_long_term_plan', 'no_unclear'
    'timed_q6_rmd_planning': 'no_unclear',
    
    # Timed Q7: If market crashed, how would you be impacted?
    # Options: 'wouldnt_bother_me', 'concerned_stressed'
    'timed_q7_market_crash': 'concerned_stressed',
    
    # Timed Q8: How do you feel about your overall financial plan?
    # Options: 'very_clear', 'dont_have_one'
    'timed_q8_financial_plan': 'dont_have_one',
    
    # MISSING QUESTIONS (from logic doc, not in current flow)
    # Uncomment and use these if you have them in your quiz:
    
    # 'q_total_savings_needed': 'no_idea',  # How much do you need total?
    # 'q_annual_cost': 'no_idea',  # How much will retirement cost per year?
    # 'q_current_progress': 'havent_started_saving',  # Describe your current progress
    # 'q_market_volatility_concern': 'not_sure_risk_exposure',  # Why concerned about volatility?
    # 'q_tax_concern': 'not_much_tax_free_savings',  # What are you concerned about regarding taxes?
    # 'timed_q_portfolio_crash_loss': 'no_idea',  # What would portfolio lose in crash?
}

# ============================================================================
# RUN THE ANALYSIS
# ============================================================================

if __name__ == "__main__":
    print("\n")
    print("="*80)
    print("ANALYZING USER QUIZ RESPONSES")
    print("="*80)
    print("\nProcessing responses...\n")
    
    red_flags, recommendations = analyze_quiz_responses(test_responses)
    
    # Additional summary
    print("\n" + "="*80)
    print("SUMMARY FOR PRODUCT/SALES TEAM")
    print("="*80)
    
    if recommendations:
        print("\n🎯 RECOMMENDED UPSELLS:")
        for tier, flags in recommendations.items():
            print(f"\n   • {tier.value}")
            print(f"     → {len(flags)} pain point(s) identified")
            print(f"     → Red flags: {', '.join([rf.id for rf in flags])}")
    else:
        print("\n✅ User appears well-prepared. Consider:")
        print("   • Periodic check-in service")
        print("   • Advanced optimization review")
    
    print("\n" + "="*80 + "\n")


# ============================================================================
# COMMON EXAMPLES FOR QUICK COPY-PASTE
# ============================================================================

"""
EXAMPLE 1: Young person just starting out
------------------------------------------
{
    'q2_concerns': ['running_out_of_money', 'not_being_on_pace'],
    'q4_retirement_age': 55,
    'q9_investment_style': 'a',
    'q10_annual_savings': 3000,
    'q11_account_types': [],
    'q12_total_savings': 10000,
    'timed_q4_on_pace': 'not_sure',
    'timed_q7_market_crash': 'concerned_stressed',
    'timed_q8_financial_plan': 'dont_have_one',
}

EXAMPLE 2: High net worth executive
------------------------------------
{
    'q2_concerns': ['paying_too_much_taxes'],
    'q4_retirement_age': 68,
    'q8_work_benefits': ['pension', 'deferred_compensation', 'stock_options'],
    'q8b_pension_income': 80000,
    'q9_investment_style': 'b',
    'q10_annual_savings': 50000,
    'q11_account_types': ['old_employer_plan'],
    'q12_total_savings': 2500000,
    'timed_q6_rmd_planning': 'no_unclear',
}

EXAMPLE 3: Conservative mid-career
-----------------------------------
{
    'q2_concerns': ['market_volatility'],
    'q4_retirement_age': 62,
    'q9_investment_style': 'd',
    'q10_annual_savings': 18000,
    'q11_account_types': ['roth_accounts', 'whole_life'],
    'q12_total_savings': 600000,
    'timed_q8_financial_plan': 'very_clear',
}

EXAMPLE 4: Edge case - exactly 2 tax flags (threshold)
-------------------------------------------------------
{
    'q2_concerns': ['paying_too_much_taxes'],
    'q4_retirement_age': 57,
    'q9_investment_style': 'b',
    'q10_annual_savings': 20000,
    'q11_account_types': ['old_employer_plan'],
    'q12_total_savings': 800000,
}

EXAMPLE 5: Zero red flags (optimal planner)
--------------------------------------------
{
    'q2_concerns': [],
    'q4_retirement_age': 65,
    'q9_investment_style': 'b',
    'q10_annual_savings': 25000,
    'q11_account_types': ['roth_accounts', 'whole_life'],
    'q12_total_savings': 1200000,
    'timed_q4_on_pace': 'calculated_target',
    'timed_q5_investments_appropriate': 'risk_return_target',
    'timed_q6_rmd_planning': 'yes_long_term_plan',
    'timed_q8_financial_plan': 'very_clear',
}
"""
