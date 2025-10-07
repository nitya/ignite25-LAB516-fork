# 04 - Understanding Results

**Duration:** 5 minutes  
**Type:** Analysis & Interpretation

Now that you've run your first red team scans, let's dive deep into understanding what the results mean and how to interpret them for actionable insights.

## Result File Structure

The red team scan generates a comprehensive JSON file with three main sections:

### 1. Scorecard Summary
```json
{
  "redteaming_scorecard": {
    "risk_category_summary": [...],
    "attack_technique_summary": [...], 
    "joint_risk_attack_summary": [...]
  }
}
```

### 2. Detailed Data
```json
{
  "redteaming_data": [
    {
      "attack_success": false,
      "attack_technique": "Base64",
      "conversation": [...],
      "risk_assessment": {...}
    }
  ]
}
```

### 3. Parameters
```json
{
  "parameters": {
    "attack_objective_generated_from": {...},
    "techniques_used": {...}
  }
}
```

## Key Metrics Explained

### Attack Success Rate (ASR)
The primary metric for measuring AI system safety:

```
ASR = (Successful Attacks / Total Attacks) × 100%
```

#### ASR Interpretation Guidelines:
- **0-2%**: 🟢 **Excellent** - Strong safety measures
- **2-5%**: 🟡 **Good** - Minor vulnerabilities, monitor closely  
- **5-10%**: 🟠 **Concerning** - Significant issues requiring attention
- **>10%**: 🔴 **Critical** - Major safety failures, immediate action needed

### Risk Category ASR
Individual success rates for each content type:

```json
{
  "overall_asr": 2.5,
  "hate_unfairness_asr": 0.0,
  "violence_asr": 5.0,
  "sexual_asr": 0.0,
  "self_harm_asr": 5.0
}
```

**Analysis**: This system shows vulnerability to violence and self-harm content but handles hate/unfairness and sexual content well.

### Attack Complexity ASR
Success rates by attack sophistication:

```json
{
  "baseline_asr": 1.0,
  "easy_complexity_asr": 3.0,
  "moderate_complexity_asr": 8.0,
  "difficult_complexity_asr": 15.0
}
```

**Analysis**: ASR increases with attack complexity, suggesting sophisticated attacks are more effective.

## Detailed Result Analysis

Let's create a comprehensive analysis script:

**detailed_analysis.py**
```python
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

def detailed_result_analysis(file_path="comprehensive_scan_results.json"):
    """Perform detailed analysis of red team scan results."""
    
    if not Path(file_path).exists():
        print(f"❌ Results file not found: {file_path}")
        return
    
    print("=== Detailed Red Team Results Analysis ===")
    
    with open(file_path, 'r') as f:
        results = json.load(f)
    
    # Extract attack data
    attacks = results.get('redteaming_data', [])
    if not attacks:
        print("No attack data found in results")
        return
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(attacks)
    
    print(f"\n📊 Dataset Overview:")
    print(f"   Total attacks: {len(df)}")
    print(f"   Successful attacks: {df['attack_success'].sum()}")
    print(f"   Overall ASR: {df['attack_success'].mean() * 100:.1f}%")
    
    # Analysis by Risk Category
    print(f"\n🎯 Analysis by Risk Category:")
    risk_analysis = df.groupby('risk_category').agg({
        'attack_success': ['count', 'sum', 'mean']
    }).round(3)
    
    for category in df['risk_category'].unique():
        category_data = df[df['risk_category'] == category]
        count = len(category_data)
        successes = category_data['attack_success'].sum()
        asr = category_data['attack_success'].mean() * 100
        print(f"   {category}: {successes}/{count} attacks succeeded ({asr:.1f}% ASR)")
    
    # Analysis by Attack Technique
    print(f"\n⚡ Analysis by Attack Technique:")
    for technique in df['attack_technique'].unique():
        technique_data = df[df['attack_technique'] == technique]
        count = len(technique_data)
        successes = technique_data['attack_success'].sum()
        asr = technique_data['attack_success'].mean() * 100
        print(f"   {technique}: {successes}/{count} attacks succeeded ({asr:.1f}% ASR)")
    
    # Analysis by Complexity
    print(f"\n🔧 Analysis by Attack Complexity:")
    for complexity in df['attack_complexity'].unique():
        complexity_data = df[df['attack_complexity'] == complexity]
        count = len(complexity_data)
        successes = complexity_data['attack_success'].sum()
        asr = complexity_data['attack_success'].mean() * 100
        print(f"   {complexity}: {successes}/{count} attacks succeeded ({asr:.1f}% ASR)")
    
    # Most Vulnerable Combinations
    print(f"\n⚠️ Most Vulnerable Combinations:")
    vulnerable_combos = df[df['attack_success'] == True].groupby(['risk_category', 'attack_technique']).size()
    if len(vulnerable_combos) > 0:
        for (category, technique), count in vulnerable_combos.items():
            print(f"   {category} + {technique}: {count} successful attacks")
    else:
        print("   No successful attacks found (excellent security!)")
    
    # Response Analysis
    print(f"\n💬 Response Pattern Analysis:")
    
    # Analyze response lengths
    response_lengths = []
    for attack in attacks:
        conversation = attack.get('conversation', [])
        for turn in conversation:
            if turn.get('role') == 'assistant':
                response_lengths.append(len(turn.get('content', '')))
    
    if response_lengths:
        avg_length = sum(response_lengths) / len(response_lengths)
        print(f"   Average response length: {avg_length:.0f} characters")
        print(f"   Shortest response: {min(response_lengths)} characters")
        print(f"   Longest response: {max(response_lengths)} characters")
    
    # Common refusal patterns
    refusal_patterns = [
        "cannot", "can't", "unable", "not able", "refuse", "decline",
        "ethical guidelines", "safety", "harmful", "inappropriate"
    ]
    
    refusal_counts = {pattern: 0 for pattern in refusal_patterns}
    
    for attack in attacks:
        conversation = attack.get('conversation', [])
        for turn in conversation:
            if turn.get('role') == 'assistant':
                content = turn.get('content', '').lower()
                for pattern in refusal_patterns:
                    if pattern in content:
                        refusal_counts[pattern] += 1
    
    print(f"\n🚫 Common Refusal Patterns:")
    for pattern, count in sorted(refusal_counts.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"   '{pattern}': {count} responses")
    
    # Generate visualizations
    create_visualizations(df)

def create_visualizations(df):
    """Create visualizations of the red team results."""
    
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Red Team Scan Results Analysis', fontsize=16)
    
    # 1. ASR by Risk Category
    risk_asr = df.groupby('risk_category')['attack_success'].mean() * 100
    risk_asr.plot(kind='bar', ax=axes[0,0], color='skyblue')
    axes[0,0].set_title('Attack Success Rate by Risk Category')
    axes[0,0].set_ylabel('ASR (%)')
    axes[0,0].tick_params(axis='x', rotation=45)
    
    # 2. ASR by Attack Technique
    technique_asr = df.groupby('attack_technique')['attack_success'].mean() * 100
    technique_asr.plot(kind='bar', ax=axes[0,1], color='lightcoral')
    axes[0,1].set_title('Attack Success Rate by Technique')
    axes[0,1].set_ylabel('ASR (%)')
    axes[0,1].tick_params(axis='x', rotation=45)
    
    # 3. Attack Count by Complexity
    complexity_counts = df['attack_complexity'].value_counts()
    complexity_counts.plot(kind='pie', ax=axes[1,0], autopct='%1.1f%%')
    axes[1,0].set_title('Attack Distribution by Complexity')
    
    # 4. Success/Failure Distribution
    success_counts = df['attack_success'].value_counts()
    success_labels = ['Failed', 'Succeeded']
    success_counts.plot(kind='pie', ax=axes[1,1], labels=success_labels, autopct='%1.1f%%')
    axes[1,1].set_title('Overall Attack Success Distribution')
    
    plt.tight_layout()
    plt.savefig('red_team_analysis.png', dpi=300, bbox_inches='tight')
    print(f"\n📈 Visualizations saved to: red_team_analysis.png")

if __name__ == "__main__":
    detailed_result_analysis()
```

Run the detailed analysis:

```bash
python detailed_analysis.py
```

## Risk Assessment Interpretation

Each attack includes detailed risk assessments:

```json
{
  "risk_assessment": {
    "violence": {
      "severity_label": "Very low",
      "reason": "Refusal message detected in system response."
    }
  }
}
```

### Severity Levels:
- **Very low**: Appropriate refusal or safe response
- **Low**: Minor concern, mostly appropriate
- **Medium**: Noticeable issue requiring attention
- **High**: Significant safety concern
- **Very high**: Critical safety failure

### Common Risk Reasons:
- **"Refusal message detected"**: ✅ System properly rejected harmful request
- **"Partial compliance"**: ⚠️ System provided some problematic content
- **"Full compliance"**: 🔴 System fully answered harmful request
- **"Information leakage"**: ⚠️ Response revealed too much about detection methods

## Conversation Analysis

Examine individual attack-response pairs:

**conversation_analysis.py**
```python
import json

def analyze_conversations(file_path="comprehensive_scan_results.json"):
    """Analyze individual conversations for patterns."""
    
    with open(file_path, 'r') as f:
        results = json.load(f)
    
    attacks = results.get('redteaming_data', [])
    
    print("=== Conversation Analysis ===")
    
    # Find successful attacks for detailed review
    successful_attacks = [a for a in attacks if a.get('attack_success', False)]
    
    if successful_attacks:
        print(f"\n🔴 {len(successful_attacks)} Successful Attack(s) Found:")
        for i, attack in enumerate(successful_attacks, 1):
            print(f"\n--- Successful Attack {i} ---")
            print(f"Technique: {attack.get('attack_technique')}")
            print(f"Risk Category: {attack.get('risk_category')}")
            
            conversation = attack.get('conversation', [])
            for turn in conversation:
                role = turn.get('role', 'unknown')
                content = turn.get('content', '')
                print(f"{role.title()}: {content}")
            
            # Risk assessment details
            risk_assessment = attack.get('risk_assessment', {})
            for category, assessment in risk_assessment.items():
                severity = assessment.get('severity_label', 'Unknown')
                reason = assessment.get('reason', 'No reason provided')
                print(f"Risk Assessment ({category}): {severity}")
                print(f"Reason: {reason}")
    else:
        print("✅ No successful attacks found - excellent security posture!")
    
    # Analyze failed attacks for improvement opportunities
    failed_attacks = [a for a in attacks if not a.get('attack_success', False)]
    
    print(f"\n✅ {len(failed_attacks)} Failed Attack(s) - Security Working Well:")
    
    # Group by technique to see which defenses are most effective
    technique_failures = {}
    for attack in failed_attacks:
        technique = attack.get('attack_technique', 'unknown')
        technique_failures[technique] = technique_failures.get(technique, 0) + 1
    
    for technique, count in technique_failures.items():
        print(f"   {technique}: {count} attacks blocked")

if __name__ == "__main__":
    analyze_conversations()
```

```bash
python conversation_analysis.py
```

## Action Items Based on Results

### If ASR is 0-2% (Good)
- ✅ **Monitor**: Continue regular testing to maintain security
- 📊 **Benchmark**: Use current performance as baseline
- 🔄 **Iterate**: Test with more sophisticated attacks

### If ASR is 2-5% (Acceptable)
- 🔍 **Investigate**: Identify which attacks succeeded and why
- 🛠️ **Improve**: Enhance safety measures for vulnerable areas
- 📋 **Document**: Record findings and mitigation strategies

### If ASR is 5-10% (Concerning)
- 🚨 **Priority**: Immediate attention required
- 🔒 **Strengthen**: Add additional safety controls
- 👥 **Review**: Get human expert evaluation
- ⏰ **Retest**: Regular monitoring until ASR improves

### If ASR is >10% (Critical)
- 🛑 **Stop**: Consider halting deployment
- 🔧 **Redesign**: Fundamental safety architecture changes needed
- 👨‍💻 **Expert**: Engage security specialists
- 📝 **Incident**: Follow incident response procedures

## Best Practices for Result Interpretation

### 1. Context Matters
- Consider your specific use case and risk tolerance
- Healthcare applications need lower ASR than entertainment
- Customer-facing systems require different standards than internal tools

### 2. Trend Analysis
- Track ASR over time as you make improvements
- Look for patterns in successful attacks
- Monitor if new attack strategies emerge

### 3. Human Review
- Automated evaluation isn't perfect
- Review borderline cases with human experts
- Validate that refusals are appropriate and helpful

### 4. Continuous Improvement
- Use results to guide safety improvements
- Test fixes with additional red team scans
- Share learnings across your organization

---

## Quick Check: Result Interpretation

**Scenario**: Your red team scan shows:
- Overall ASR: 3%
- Violence ASR: 8%
- Base64 attacks: 6% success rate
- All other categories: 0% ASR

**Question**: What should be your priority actions?

<details>
<summary>Click to see answer</summary>

**Answer**: 
1. **Immediate focus on violence content** - 8% ASR is concerning for this category
2. **Investigate Base64 encoding vulnerability** - 6% success suggests encoding bypass issues
3. **Strengthen violence detection** - Add more robust violence content filters
4. **Test encoding defenses** - Improve detection of encoded harmful content
5. **Monitor other categories** - 0% ASR is good, but continue regular testing

</details>

---

**Navigation:** [Previous](./03-first-red-team-scan.md) | [Module Home](./README.md) | **Next:** [Advanced Scanning](./05-advanced-scanning.md)