"""
RetireUS Red Flag Tester - Web Application
===========================================
A web interface for testing the red flag detection logic.
"""

from flask import Flask, render_template, request, jsonify
import json
from red_flag_detector import RedFlagDetector, ServiceTier
from scoring import calculate_pacing_score, calculate_tax_planning_score, calculate_risk_of_failure_score

app = Flask(__name__)

# Initialize detector
detector = RedFlagDetector()

@app.route('/')
def index():
    """Main page with quiz interface"""
    return render_template('index.html')

@app.route('/scenarios')
def scenarios():
    """Scenario testing page"""
    return render_template('scenarios.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Analyze quiz responses and return red flags + scores"""
    try:
        responses = request.json
        
        # Convert responses to proper format
        formatted_responses = format_responses(responses)
        
        # Detect red flags
        red_flags = detector.detect(formatted_responses)
        recommendations = detector.get_recommendations(red_flags)
        
        # Calculate scores (NEW!)
        pacing = calculate_pacing_score(formatted_responses)
        tax_planning = calculate_tax_planning_score(formatted_responses)
        risk_of_failure = calculate_risk_of_failure_score(
            formatted_responses, 
            red_flags, 
            pacing['score']
        )
        
        # Get the recommended plan (highest tier only)
        recommended_plan = None
        if recommendations:
            highest_tier = list(recommendations.keys())[0]  # Only one tier in dict now
            flag_count = len(recommendations[highest_tier])
            recommended_plan = {
                'tier': highest_tier.value,
                'flag_count': flag_count
            }
        else:
            # Failsafe
            recommended_plan = {
                'tier': 'Basic Planning',
                'flag_count': 0
            }
        
        # Format response
        result = {
            'red_flags': [
                {
                    'id': rf.id,
                    'name': rf.name,
                    'tier': rf.tier.value,
                    'description': rf.description
                }
                for rf in red_flags
            ],
            'recommended_plan': recommended_plan,
            'scores': {
                'pacing': pacing,
                'tax_planning': tax_planning,
                'risk_of_failure': risk_of_failure
            },
            'summary': {
                'total_flags': len(red_flags),
                'basic_count': sum(1 for rf in red_flags if rf.tier == ServiceTier.BASIC_PLANNING),
                'tax_count': sum(1 for rf in red_flags if rf.tier == ServiceTier.TAX_MASTERY),
                'wealth_count': sum(1 for rf in red_flags if rf.tier == ServiceTier.WEALTH_MASTERY),
            }
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/scenarios/list', methods=['GET'])
def list_scenarios():
    """Get list of all test scenarios"""
    scenarios = [
        {
            'id': 'young_professional',
            'name': 'Young Professional - Just Starting Out',
            'description': 'Multiple basic planning issues, early retirement penalty',
            'expected_flags': 7,
            'expected_tiers': ['Basic Planning', 'Tax Mastery']
        },
        {
            'id': 'high_earner',
            'name': 'High Earner Approaching Retirement',
            'description': 'Executive compensation, high net worth, tax complexity',
            'expected_flags': 7,
            'expected_tiers': ['Basic Planning', 'Tax Mastery', 'Wealth Mastery']
        },
        {
            'id': 'conservative',
            'name': 'Conservative Mid-Career Investor',
            'description': 'Risk-averse with inflation concerns',
            'expected_flags': 2,
            'expected_tiers': ['Basic Planning']
        },
        {
            'id': 'optimal',
            'name': 'Optimal Retirement Planner',
            'description': 'Well-prepared with minimal issues',
            'expected_flags': 0,
            'expected_tiers': []
        },
        {
            'id': 'tax_threshold',
            'name': 'Tax Mastery Threshold Test',
            'description': 'Exactly 2 tax flags (edge case)',
            'expected_flags': 2,
            'expected_tiers': ['Tax Mastery']
        },
        {
            'id': 'age_58',
            'name': 'Age 58 Boundary Test',
            'description': 'Early retirement penalty boundary',
            'expected_flags': 1,
            'expected_tiers': []
        },
        {
            'id': 'age_68',
            'name': 'Age 68 Boundary Test',
            'description': 'RMD planning boundary',
            'expected_flags': 1,
            'expected_tiers': []
        },
        {
            'id': 'savings_10k',
            'name': 'Annual Savings $10k Boundary',
            'description': 'Limited savings boundary test',
            'expected_flags': 1,
            'expected_tiers': ['Basic Planning']
        },
        {
            'id': 'wealth_2m',
            'name': 'Total Savings $2M+ Boundary',
            'description': 'Estate planning threshold test',
            'expected_flags': 1,
            'expected_tiers': ['Wealth Mastery']
        }
    ]
    
    return jsonify(scenarios)

@app.route('/api/scenarios/<scenario_id>', methods=['GET'])
def get_scenario(scenario_id):
    """Get specific scenario data"""
    scenarios_data = {
        'young_professional': {
            'q2_concerns': ['running_out_of_money', 'not_being_on_pace'],
            'q4_retirement_age': 55,
            'q8_work_benefits': [],
            'q9_investment_style': 'a',
            'q10_annual_savings': 3000,
            'q11_account_types': [],
            'q12_total_savings': 10000,
            'timed_q4_on_pace': 'not_sure',
            'timed_q5_investments_appropriate': 'should_reevaluate',
            'timed_q7_market_crash': 'concerned_stressed',
            'timed_q8_financial_plan': 'dont_have_one',
        },
        'high_earner': {
            'q2_concerns': ['paying_too_much_taxes'],
            'q4_retirement_age': 68,
            'q8_work_benefits': ['pension', 'deferred_compensation', 'stock_options'],
            'q8b_pension_income': 80000,
            'q9_investment_style': 'b',
            'q10_annual_savings': 50000,
            'q11_account_types': ['old_employer_plan'],
            'q12_total_savings': 2500000,
            'q_current_progress': 'multiple_retirement_accounts',
            'timed_q6_rmd_planning': 'no_unclear',
        },
        'conservative': {
            'q2_concerns': ['market_volatility'],
            'q4_retirement_age': 62,
            'q8_work_benefits': [],
            'q9_investment_style': 'd',
            'q10_annual_savings': 18000,
            'q11_account_types': ['roth_accounts', 'whole_life'],
            'q12_total_savings': 600000,
            'timed_q8_financial_plan': 'very_clear',
        },
        'optimal': {
            'q2_concerns': [],
            'q4_retirement_age': 65,
            'q8_work_benefits': [],
            'q9_investment_style': 'b',
            'q10_annual_savings': 25000,
            'q11_account_types': ['roth_accounts', 'whole_life'],
            'q12_total_savings': 1200000,
            'timed_q4_on_pace': 'calculated_target',
            'timed_q5_investments_appropriate': 'risk_return_target',
            'timed_q6_rmd_planning': 'yes_long_term_plan',
            'timed_q8_financial_plan': 'very_clear',
        },
        'tax_threshold': {
            'q2_concerns': ['paying_too_much_taxes'],
            'q4_retirement_age': 57,
            'q8_work_benefits': [],
            'q9_investment_style': 'b',
            'q10_annual_savings': 20000,
            'q11_account_types': ['old_employer_plan'],
            'q12_total_savings': 800000,
        },
        'age_58': {
            'q2_concerns': [],
            'q4_retirement_age': 58,
            'q8_work_benefits': [],
            'q9_investment_style': 'b',
            'q10_annual_savings': 20000,
            'q11_account_types': ['roth_accounts'],
            'q12_total_savings': 500000,
        },
        'age_68': {
            'q2_concerns': [],
            'q4_retirement_age': 68,
            'q8_work_benefits': [],
            'q9_investment_style': 'b',
            'q10_annual_savings': 20000,
            'q11_account_types': ['roth_accounts'],
            'q12_total_savings': 500000,
        },
        'savings_10k': {
            'q2_concerns': [],
            'q4_retirement_age': 65,
            'q8_work_benefits': [],
            'q9_investment_style': 'b',
            'q10_annual_savings': 10000,
            'q11_account_types': ['roth_accounts'],
            'q12_total_savings': 500000,
        },
        'wealth_2m': {
            'q2_concerns': [],
            'q4_retirement_age': 65,
            'q8_work_benefits': [],
            'q9_investment_style': 'b',
            'q10_annual_savings': 50000,
            'q11_account_types': ['roth_accounts'],
            'q12_total_savings': 2500000,
        }
    }
    
    if scenario_id in scenarios_data:
        return jsonify(scenarios_data[scenario_id])
    else:
        return jsonify({'error': 'Scenario not found'}), 404

def format_responses(raw_responses):
    """Format responses from web form to detector format"""
    formatted = {}
    
    # Handle multi-select fields (arrays)
    multi_select_fields = ['q2_concerns', 'q8_work_benefits', 'q11_account_types']
    for field in multi_select_fields:
        if field in raw_responses:
            formatted[field] = raw_responses[field] if isinstance(raw_responses[field], list) else []
    
    # Handle numeric fields (ADDED q7_annual_retirement_cost)
    numeric_fields = ['q4_retirement_age', 'q7_annual_retirement_cost', 'q8b_pension_income', 
                      'q10_annual_savings', 'q12_total_savings']
    for field in numeric_fields:
        if field in raw_responses and raw_responses[field]:
            try:
                formatted[field] = int(raw_responses[field])
            except (ValueError, TypeError):
                formatted[field] = 0
    
    # Handle single-select fields
    single_select_fields = [
        'q9_investment_style', 
        'timed_q1_value_more', 
        'timed_q2_upset_more',
        'timed_q3_saving_enough',
        'timed_q4_on_pace',
        'timed_q5_investments_appropriate',
        'timed_q6_rmd_planning',
        'timed_q7_market_crash',
        'timed_q8_financial_plan',
        'q_current_progress',
        'q_tax_concern',
        'q_market_volatility_concern'
    ]
    for field in single_select_fields:
        if field in raw_responses:
            formatted[field] = raw_responses[field]
    
    return formatted

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)