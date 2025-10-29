"""
RetireUS Scoring Logic
======================
Calculates Pacing, Tax Planning, and Risk of Failure scores
"""

import math

def calculate_pacing_score(responses):
    """
    Calculate Pacing Score using FV formula
    Returns: dict with score, result text, and status
    """
    # Get inputs
    q4_retirement_age = responses.get('q4_retirement_age', 65)
    q7_annual_cost = responses.get('q7_annual_retirement_cost', 100000)
    q8_has_pension = 'pension' in responses.get('q8_work_benefits', [])
    q8b_pension_income = responses.get('q8b_pension_income', 0) if q8_has_pension else 0
    q9_investment_style = responses.get('q9_investment_style', 'b')
    q10_annual_savings = responses.get('q10_annual_savings', 15000)
    q12_total_savings = responses.get('q12_total_savings', 500000)
    
    # Current age (estimate as 40 if not provided)
    current_age = 40  # You might want to add this as a quiz question
    number_of_periods = q4_retirement_age - current_age
    
    # Investment style to rates mapping
    rate_map = {
        'd': [0.025, 0.03, 0.035, 0.04],  # Safe investments
        'c': [0.04, 0.045, 0.05, 0.055],   # Income investments
        'b': [0.055, 0.06, 0.065, 0.07],   # Moderate
        'a': [0.075, 0.08, 0.085, 0.09]    # Casino/aggressive
    }
    
    rates = rate_map.get(q9_investment_style, rate_map['b'])
    
    # Calculate FV Target
    fv_target = future_value(0.025, number_of_periods, -q10_annual_savings, 
                             -(q7_annual_cost - q8b_pension_income), 0) / 0.045
    
    # Run FV calculation 4 times with different rates
    less_than_target_count = 0
    for rate in rates:
        fv = future_value(rate, number_of_periods, -q10_annual_savings, -q12_total_savings, 0)
        if fv < fv_target:
            less_than_target_count += 1
    
    # Determine result
    if less_than_target_count == 0:
        result = "Likely On Track"
        status = "on_track"
        score = 0
    elif less_than_target_count == 1:
        result = "At Risk"
        status = "at_risk"
        score = 3
    else:  # 2 or more
        result = "Likely Off Track"
        status = "off_track"
        score = 6
    
    return {
        'score': score,
        'result': result,
        'status': status,
        'details': {
            'calculations_below_target': less_than_target_count,
            'fv_target': round(fv_target, 2)
        }
    }


def calculate_tax_planning_score(responses):
    """
    Calculate Tax Planning Score using baseline scoring
    Returns: dict with score, result text, and status
    """
    score = 0  # Baseline starts at 0
    
    # Get inputs
    q4_retirement_age = responses.get('q4_retirement_age', 65)
    q7_annual_cost = responses.get('q7_annual_retirement_cost', 100000)
    q8_work_benefits = responses.get('q8_work_benefits', [])
    q10_annual_savings = responses.get('q10_annual_savings', 15000)
    q12_total_savings = responses.get('q12_total_savings', 500000)
    timed_q6_rmd = responses.get('timed_q6_rmd_planning', '')
    
    current_age = 40
    timeline = q4_retirement_age - current_age
    
    # Individual rules
    if timed_q6_rmd == 'yes_long_term_plan':
        score += 1
    elif timed_q6_rmd == 'no_unclear':
        score -= 1
    
    if q10_annual_savings < 20000:
        score += 1
    elif q10_annual_savings >= 30000:
        score -= 1
    
    # Combination rules
    if timeline > 10 and q12_total_savings >= 1000000:
        score -= 1
    
    if timeline > 20 and q10_annual_savings >= 30000:
        score -= 1
    
    if q4_retirement_age > 65 and q12_total_savings >= 1000000:
        score -= 1
    
    if q12_total_savings >= 1000000 and q7_annual_cost == 50000:
        score -= 1
    
    if q12_total_savings >= 1000000 and 'pension' in q8_work_benefits:
        score -= 1
    
    if q12_total_savings >= 1000000 and 'deferred_compensation' in q8_work_benefits:
        score -= 1
    
    if q12_total_savings < 350000 and q7_annual_cost >= 150000:
        score += 2
    
    if q12_total_savings < 200000 and timeline < 5:
        score += 2
    
    # Determine result
    if score <= 0:
        result = "Heavy Projected Tax Burden"
        status = "off_track"
    elif score == 0:
        result = "Average Tax Burden"
        status = "at_risk"
    else:  # > 0
        result = "Low Tax Burden"
        status = "on_track"
    
    return {
        'score': score,
        'result': result,
        'status': status
    }


def calculate_risk_of_failure_score(responses, red_flags, pacing_score):
    """
    Calculate Risk of Failure Score using weighted formula
    Returns: dict with score, result text, and status
    """
    # Pacing component (50% weight)
    pacing_weighted = pacing_score * 0.5
    
    # Timeline component (25% weight)
    q4_retirement_age = responses.get('q4_retirement_age', 65)
    current_age = 40
    timeline = q4_retirement_age - current_age
    
    if timeline <= 5:
        timeline_score = 3
    elif timeline <= 10:
        timeline_score = 2
    elif timeline <= 15:
        timeline_score = 0
    else:  # 15+
        timeline_score = -2
    
    timeline_weighted = timeline_score * 0.25
    
    # Red Flags component (25% weight)
    red_flag_scores = {
        'basic_rf1': 3,
        'basic_rf3': 4,
        'basic_rf4': 4,
        'basic_rf5': 2,
        'tax_rf1': 2,
        'wealth_rf3': 3
    }
    
    red_flag_total = 0
    for flag in red_flags:
        flag_id = flag.id.lower()
        if flag_id in red_flag_scores:
            red_flag_total += red_flag_scores[flag_id]
    
    red_flags_weighted = red_flag_total * 0.25
    
    # Total score
    total_score = pacing_weighted + timeline_weighted + red_flags_weighted
    
    # Determine result
    if total_score < 2:
        result = "On Track"
        status = "on_track"
    elif total_score <= 4:
        result = "At Risk"
        status = "at_risk"
    else:  # > 4
        result = "Likely Off Pace"
        status = "off_track"
    
    return {
        'score': round(total_score, 2),
        'result': result,
        'status': status,
        'components': {
            'pacing': pacing_weighted,
            'timeline': timeline_weighted,
            'red_flags': red_flags_weighted
        }
    }


def future_value(rate, nper, pmt, pv, type=0):
    """
    Calculate Future Value (Excel FV function equivalent)
    """
    if rate == 0:
        return -(pv + pmt * nper)
    
    fv = -pv * math.pow(1 + rate, nper)
    fv -= pmt * (1 + rate * type) * (math.pow(1 + rate, nper) - 1) / rate
    
    return fv