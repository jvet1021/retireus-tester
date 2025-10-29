// RetireUS Red Flag Tester - Main App JavaScript

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('quizForm');
    const resultsContainer = document.getElementById('resultsContainer');
    const pensionCheckbox = document.querySelector('input[name="q8_work_benefits"][value="pension"]');
    const q8bBlock = document.getElementById('q8b_block');

    // Handle conditional pension income question
    pensionCheckbox.addEventListener('change', function() {
        if (this.checked) {
            q8bBlock.style.display = 'block';
            q8bBlock.classList.add('active');
        } else {
            q8bBlock.style.display = 'none';
            q8bBlock.classList.remove('active');
            document.querySelector('input[name="q8b_pension_income"]').value = 0;
        }
    });

    // Handle form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const responses = {};

        // Process multi-select checkboxes
        const multiSelectFields = ['q2_concerns', 'q8_work_benefits', 'q11_account_types'];
        multiSelectFields.forEach(field => {
            responses[field] = formData.getAll(field);
        });

        // Process other fields
        const allFields = [
            'q4_retirement_age', 'q8b_pension_income', 'q9_investment_style',
            'q10_annual_savings', 'q12_total_savings',
            'timed_q4_on_pace', 'timed_q5_investments_appropriate',
            'timed_q6_rmd_planning', 'timed_q7_market_crash', 'timed_q8_financial_plan'
        ];
        
        allFields.forEach(field => {
            const value = formData.get(field);
            if (value) {
                responses[field] = value;
            }
        });

        // Send to API
        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(responses)
            });

            const result = await response.json();
            
            if (response.ok) {
                displayResults(result);
            } else {
                alert('Error: ' + (result.error || 'Unknown error'));
            }
        } catch (error) {
            alert('Network error: ' + error.message);
        }
    });
});

function displayResults(result) {
    const resultsContainer = document.getElementById('resultsContainer');
    
    // Update summary cards
    document.getElementById('totalFlags').textContent = result.summary.total_flags;
    document.getElementById('basicFlags').textContent = result.summary.basic_count;
    document.getElementById('taxFlags').textContent = result.summary.tax_count;
    document.getElementById('wealthFlags').textContent = result.summary.wealth_count;

    // Display scores (NEW!)
    displayScores(result.scores);

    // Display recommendation (UPDATED - only highest tier)
    const recommendationsDiv = document.getElementById('recommendations');
    recommendationsDiv.innerHTML = '';
    
    if (result.recommended_plan) {
        recommendationsDiv.innerHTML = '<h3 style="margin-bottom: 15px;">💡 Recommended Plan</h3>';
        
        const tierDiv = document.createElement('div');
        tierDiv.className = `recommendation-tier ${getTierClass(result.recommended_plan.tier)}`;
        tierDiv.innerHTML = `
            <h3>✓ ${result.recommended_plan.tier}</h3>
            <p class="recommendation-count">Based on ${result.recommended_plan.flag_count} red flag(s) detected</p>
        `;
        recommendationsDiv.appendChild(tierDiv);
    }

    // Display red flags by tier
    const redFlagsDiv = document.getElementById('redFlagsList');
    redFlagsDiv.innerHTML = '';
    
    if (result.red_flags.length > 0) {
        redFlagsDiv.innerHTML = '<h3 style="margin-top: 20px; margin-bottom: 15px;">🚩 Detected Red Flags</h3>';
        
        // Group by tier
        const flagsByTier = {
            'Basic Planning': [],
            'Tax Mastery': [],
            'Wealth Mastery': []
        };
        
        result.red_flags.forEach(flag => {
            if (flagsByTier[flag.tier]) {
                flagsByTier[flag.tier].push(flag);
            }
        });

        // Display each tier
        for (const [tier, flags] of Object.entries(flagsByTier)) {
            if (flags.length > 0) {
                const tierSection = document.createElement('div');
                tierSection.className = 'tier-section';
                
                const tierHeader = document.createElement('div');
                tierHeader.className = `tier-header ${getTierClass(tier)}`;
                tierHeader.textContent = `${tier} (${flags.length} ${flags.length === 1 ? 'flag' : 'flags'})`;
                tierSection.appendChild(tierHeader);

                flags.forEach(flag => {
                    const flagItem = document.createElement('div');
                    flagItem.className = `red-flag-item ${getTierClass(tier)}`;
                    flagItem.innerHTML = `
                        <div class="red-flag-name">
                            <span class="red-flag-id">${flag.id}</span>
                            ${flag.name}
                        </div>
                        <div class="red-flag-description">${flag.description}</div>
                    `;
                    tierSection.appendChild(flagItem);
                });

                redFlagsDiv.appendChild(tierSection);
            }
        }
    }

    // Show results container
    resultsContainer.style.display = 'block';
    
    // Scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth' });
}

function displayScores(scores) {
    // Create scores section if it doesn't exist
    let scoresSection = document.getElementById('scoresSection');
    if (!scoresSection) {
        scoresSection = document.createElement('div');
        scoresSection.id = 'scoresSection';
        scoresSection.innerHTML = '<h3 style="margin: 30px 0 20px 0;">📊 Your Scores</h3>';
        
        // Insert after summary cards
        const summaryCards = document.querySelector('.summary-cards');
        summaryCards.parentNode.insertBefore(scoresSection, summaryCards.nextSibling);
    }
    
    scoresSection.innerHTML = `
        <h3 style="margin: 30px 0 20px 0;">📊 Your Scores</h3>
        <div class="score-cards">
            <div class="score-card">
                <h4>Pacing Score</h4>
                <div class="score-value ${getScoreClass(scores.pacing.status)}">
                    ${scores.pacing.result}
                </div>
                <p class="score-description">Based on your savings trajectory</p>
            </div>
            <div class="score-card">
                <h4>Tax Planning Score</h4>
                <div class="score-value ${getScoreClass(scores.tax_planning.status)}">
                    ${scores.tax_planning.result}
                </div>
                <p class="score-description">Projected tax burden in retirement</p>
            </div>
            <div class="score-card">
                <h4>Risk of Failure Score</h4>
                <div class="score-value ${getScoreClass(scores.risk_of_failure.status)}">
                    ${scores.risk_of_failure.result}
                </div>
                <p class="score-description">Overall retirement readiness</p>
            </div>
        </div>
    `;
}

function getScoreClass(status) {
    const statusMap = {
        'on_track': 'on-track',
        'at_risk': 'at-risk',
        'off_track': 'off-track'
    };
    return statusMap[status] || 'at-risk';
}

function getTierClass(tierName) {
    const tierMap = {
        'Basic Planning': 'basic',
        'Tax Mastery': 'tax',
        'Wealth Mastery': 'wealth'
    };
    return tierMap[tierName] || 'basic';
}

