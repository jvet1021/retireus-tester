// RetireUS Red Flag Tester - Scenarios JavaScript

let currentScenario = null;
let currentScenarioData = null;

document.addEventListener('DOMContentLoaded', function() {
    loadScenarios();
});

async function loadScenarios() {
    try {
        const response = await fetch('/api/scenarios/list');
        const scenarios = await response.json();
        
        const grid = document.getElementById('scenariosGrid');
        grid.innerHTML = '';
        
        scenarios.forEach(scenario => {
            const card = document.createElement('div');
            card.className = 'scenario-card';
            card.onclick = () => showScenario(scenario.id);
            
            card.innerHTML = `
                <h3>${scenario.name}</h3>
                <p>${scenario.description}</p>
                <div class="scenario-meta">
                    <span class="badge badge-flags">${scenario.expected_flags} flags</span>
                    ${scenario.expected_tiers.map(tier => 
                        `<span class="badge badge-tier">${tier}</span>`
                    ).join('')}
                </div>
            `;
            
            grid.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading scenarios:', error);
        alert('Failed to load scenarios');
    }
}

async function showScenario(scenarioId) {
    try {
        // Get scenario list for metadata
        const listResponse = await fetch('/api/scenarios/list');
        const scenarios = await listResponse.json();
        const scenarioMeta = scenarios.find(s => s.id === scenarioId);
        
        // Get scenario data
        const dataResponse = await fetch(`/api/scenarios/${scenarioId}`);
        const scenarioData = await dataResponse.json();
        
        currentScenario = scenarioMeta;
        currentScenarioData = scenarioData;
        
        // Update modal
        document.getElementById('modalTitle').textContent = scenarioMeta.name;
        document.getElementById('modalDescription').textContent = scenarioMeta.description;
        document.getElementById('modalResponses').textContent = JSON.stringify(scenarioData, null, 2);
        document.getElementById('expectedFlags').textContent = scenarioMeta.expected_flags;
        
        const tiersDiv = document.getElementById('expectedTiers');
        tiersDiv.innerHTML = scenarioMeta.expected_tiers.length > 0
            ? scenarioMeta.expected_tiers.map(tier => `<span class="badge badge-tier">${tier}</span>`).join('')
            : '<span class="badge" style="background: #E5E7EB; color: #6B7280;">None</span>';
        
        // Hide previous results
        document.getElementById('scenarioResults').style.display = 'none';
        
        // Show modal
        document.getElementById('scenarioModal').style.display = 'flex';
    } catch (error) {
        console.error('Error loading scenario:', error);
        alert('Failed to load scenario');
    }
}

function closeModal() {
    document.getElementById('scenarioModal').style.display = 'none';
    currentScenario = null;
    currentScenarioData = null;
}

async function runScenario() {
    if (!currentScenarioData) return;
    
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentScenarioData)
        });

        const result = await response.json();
        
        if (response.ok) {
            displayScenarioResults(result);
        } else {
            alert('Error: ' + (result.error || 'Unknown error'));
        }
    } catch (error) {
        alert('Network error: ' + error.message);
    }
}

function displayScenarioResults(result) {
    const resultsDiv = document.getElementById('scenarioResults');
    
    // Update comparison
    document.getElementById('comparisonExpectedFlags').textContent = currentScenario.expected_flags;
    document.getElementById('comparisonActualFlags').textContent = result.summary.total_flags;
    
    // Determine if test passed
    const expectedTiersSet = new Set(currentScenario.expected_tiers);
    const actualTiersSet = new Set(Object.keys(result.recommendations));
    
    const tiersMatch = setsEqual(expectedTiersSet, actualTiersSet);
    const flagsMatch = currentScenario.expected_flags === result.summary.total_flags;
    
    const testPassed = tiersMatch; // Primary check is tiers, flags can vary slightly
    
    const statusDiv = document.getElementById('testStatus');
    if (testPassed) {
        statusDiv.className = 'test-status pass';
        statusDiv.innerHTML = '✅ TEST PASSED - Results match expected outcome';
    } else {
        statusDiv.className = 'test-status fail';
        statusDiv.innerHTML = `
            ❌ TEST FAILED - Results differ from expected<br>
            <small>Expected tiers: ${Array.from(expectedTiersSet).join(', ') || 'None'}</small><br>
            <small>Actual tiers: ${Array.from(actualTiersSet).join(', ') || 'None'}</small>
        `;
    }
    
    // Update summary cards
    document.getElementById('modalTotalFlags').textContent = result.summary.total_flags;
    document.getElementById('modalBasicFlags').textContent = result.summary.basic_count;
    document.getElementById('modalTaxFlags').textContent = result.summary.tax_count;
    document.getElementById('modalWealthFlags').textContent = result.summary.wealth_count;

    // Display recommendations
    const recommendationsDiv = document.getElementById('modalRecommendations');
    recommendationsDiv.innerHTML = '';
    
    if (Object.keys(result.recommendations).length > 0) {
        recommendationsDiv.innerHTML = '<h4 style="margin-bottom: 15px;">💡 Recommended Services</h4>';
        
        for (const [tier, flags] of Object.entries(result.recommendations)) {
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
                <h4>✅ No Recommendations Triggered</h4>
                <p>User appears to be on track.</p>
            </div>
        `;
    }

    // Display red flags
    const redFlagsDiv = document.getElementById('modalRedFlags');
    redFlagsDiv.innerHTML = '';
    
    if (result.red_flags.length > 0) {
        redFlagsDiv.innerHTML = '<h4 style="margin-top: 20px; margin-bottom: 15px;">🚩 Detected Red Flags</h4>';
        
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
                tierHeader.textContent = `${tier} (${flags.length})`;
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

    // Show results
    resultsDiv.style.display = 'block';
}

function getTierClass(tierName) {
    const tierMap = {
        'Basic Planning': 'basic',
        'Tax Mastery': 'tax',
        'Wealth Mastery': 'wealth'
    };
    return tierMap[tierName] || 'basic';
}

function setsEqual(set1, set2) {
    if (set1.size !== set2.size) return false;
    for (const item of set1) {
        if (!set2.has(item)) return false;
    }
    return true;
}

// Close modal on outside click
document.addEventListener('click', function(e) {
    const modal = document.getElementById('scenarioModal');
    if (e.target === modal) {
        closeModal();
    }
});