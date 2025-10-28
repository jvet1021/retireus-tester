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

    // Display recommendations
    const recommendationsDiv = document.getElementById('recommendations');
    recommendationsDiv.innerHTML = '';
    
    if (Object.keys(result.recommendations).length > 0) {
        recommendationsDiv.innerHTML = '<h3 style="margin-bottom: 15px;">💡 Recommended Services</h3>';
        
        for (const [tier, flags] of Object.entries(result.recommendations)) {
            const tierClass = tier.toLowerCase().replace(' ', '-');
            const tierDiv = document.createElement('div');
            tierDiv.className = `recommendation-tier ${getTierClass(tier)}`;
            tierDiv.innerHTML = `
                <h3>✓ ${tier}</h3>
                <p class="recommendation-count">Triggered by ${flags.length} red flag(s)</p>
            `;
            recommendationsDiv.appendChild(tierDiv);
        }
    } else {
        recommendationsDiv.innerHTML = `
            <div class="recommendation-tier" style="border-left-color: #10B981;">
                <h3>✅ No Recommendations Triggered</h3>
                <p>User appears to be on track for retirement.</p>
            </div>
        `;
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

function getTierClass(tierName) {
    const tierMap = {
        'Basic Planning': 'basic',
        'Tax Mastery': 'tax',
        'Wealth Mastery': 'wealth'
    };
    return tierMap[tierName] || 'basic';
}