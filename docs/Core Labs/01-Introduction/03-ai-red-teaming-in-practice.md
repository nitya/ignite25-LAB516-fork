# 03 - AI Red Teaming in Practice

**Duration:** 5 minutes  
**Type:** Conceptual Reading

## The NIST Framework for AI Risk Management

Microsoft follows the NIST AI Risk Management Framework, which provides a structured approach to AI safety:

### 1. 🏛️ Govern
**Establish policies and procedures** for responsible AI development
- Create AI governance committees
- Define acceptable use policies
- Establish accountability frameworks

### 2. 🗺️ Map
**Identify relevant risks and define your use case**
- Catalog potential AI risks specific to your domain
- Document intended use cases and limitations
- Map regulatory and compliance requirements

### 3. 📏 Measure
**Evaluate risks at scale** ← *This is where AI Red Teaming shines*
- Automated safety assessments
- Quantitative risk measurement
- Continuous monitoring and evaluation

### 4. 🛡️ Manage
**Mitigate risks in production and monitor with incident response plans**
- Implement safety controls and filters
- Deploy monitoring systems
- Maintain incident response procedures

## Where AI Red Teaming Fits

The AI Red Teaming Agent primarily supports the **Measure** phase by enabling:

### Automated Scale Testing
- **Challenge**: Manual red teaming is time and resource intensive
- **Solution**: Automated scans can test hundreds of attack scenarios rapidly
- **Benefit**: Scale safety testing to match the pace of AI development

### Consistent Evaluation
- **Challenge**: Human red teamers may have varying expertise and coverage
- **Solution**: Standardized attack objectives and evaluation criteria
- **Benefit**: Reproducible and comparable results across teams and time

### Early Detection
- **Challenge**: Safety issues discovered late in development are costly to fix
- **Solution**: Integrate red teaming into CI/CD pipelines
- **Benefit**: "Shift left" approach catches issues early

## Implementation Strategies

### 1. Development Integration

#### Continuous Integration Pipeline
```yaml
# Example CI/CD integration
ai_safety_check:
  runs-on: ubuntu-latest
  steps:
    - name: Checkout code
    - name: Setup Python
    - name: Install dependencies
    - name: Run AI Red Teaming Scan
      run: python run_red_team_scan.py
    - name: Evaluate results
      run: python evaluate_asr_results.py
```

#### Pre-deployment Gates
- **Threshold-based approval**: ASR below 5% required for production
- **Manual review triggers**: Flagged issues require human expert review
- **Compliance verification**: Automated compliance report generation

### 2. Operational Monitoring

#### Production Monitoring
- **Runtime detection**: Monitor live interactions for safety violations
- **Feedback loops**: User reports trigger additional testing
- **Model drift detection**: Regular re-testing as models are updated

#### Incident Response
- **Rapid assessment**: Quick red teaming scans for new attack vectors
- **Impact analysis**: Evaluate scope of potential safety issues
- **Remediation testing**: Verify fixes address identified issues

## Best Practices for Implementation

### 1. Start Small, Scale Gradually

#### Phase 1: Pilot (Weeks 1-2)
- Choose one model or application for initial testing
- Run basic scans with default risk categories
- Establish baseline ASR measurements

#### Phase 2: Expand (Weeks 3-6)
- Add custom attack objectives for your domain
- Integrate with development workflows
- Train team on result interpretation

#### Phase 3: Mature (Months 2-6)
- Implement automated CI/CD integration
- Establish organizational policies and thresholds
- Create incident response procedures

### 2. Combine Automated and Manual Testing

#### Automated Testing Strengths
- **Coverage**: Test many scenarios rapidly
- **Consistency**: Standardized evaluation criteria
- **Scalability**: Keep pace with development velocity

#### Manual Testing Strengths
- **Creativity**: Novel attack vectors and edge cases
- **Context**: Domain-specific expertise and insights
- **Judgment**: Nuanced evaluation of borderline cases

#### Recommended Approach
```
Automated Scan → Flag High-Risk Issues → Human Expert Review → Iterate
```

### 3. Establish Clear Metrics and Thresholds

#### Key Performance Indicators (KPIs)
- **Attack Success Rate (ASR)**: Primary safety metric
- **Coverage**: Percentage of risk categories tested
- **Frequency**: How often testing is performed
- **Time to Resolution**: Speed of fixing identified issues

#### Sample Thresholds
- **Green**: ASR < 2% across all categories
- **Yellow**: ASR 2-5% requires review and justification
- **Red**: ASR > 5% blocks deployment pending fixes

### 4. Document and Learn

#### Testing Documentation
- **Test Plans**: What scenarios are being tested and why
- **Results Archive**: Historical ASR trends and patterns
- **Mitigation Log**: How identified issues were addressed

#### Knowledge Sharing
- **Team Training**: Regular sessions on AI safety testing
- **Cross-team Collaboration**: Share learnings across projects
- **External Engagement**: Contribute to industry best practices

## Common Implementation Challenges

### Challenge 1: False Positives
**Problem**: Safety evaluators flag benign content as harmful
**Solutions**:
- Fine-tune evaluation thresholds
- Implement human-in-the-loop review for borderline cases
- Create domain-specific evaluation criteria

### Challenge 2: Attack Strategy Evolution
**Problem**: Attackers develop new techniques faster than detection
**Solutions**:
- Regular updates to attack objective datasets
- Community sharing of new attack patterns
- Adaptive evaluation criteria that evolve over time

### Challenge 3: Context Sensitivity
**Problem**: Same content may be harmful in one context but acceptable in another
**Solutions**:
- Context-aware evaluation frameworks
- Use case specific testing scenarios
- Stakeholder involvement in defining acceptable content

## Success Metrics

### Short-term (0-3 months)
- ✅ Baseline ASR measurements established
- ✅ Team trained on red teaming concepts
- ✅ Basic automated scans operational

### Medium-term (3-12 months)
- ✅ CI/CD integration functional
- ✅ Custom attack objectives developed
- ✅ Incident response procedures tested

### Long-term (12+ months)
- ✅ Organization-wide safety culture established
- ✅ Industry benchmarking and comparison
- ✅ Continuous improvement process mature

---

## Preparation Check

Before moving to hands-on modules, ensure you understand:

- ✅ The four risk categories and their importance
- ✅ Different attack strategy complexity levels
- ✅ How ASR is calculated and used
- ✅ The role of automation in scaling safety testing
- ✅ Best practices for combining automated and manual testing

---

## Module 1 Summary

You've now completed the foundational knowledge for AI red teaming:

1. **Understood** the difference between traditional and AI red teaming
2. **Learned** about the four primary risk categories
3. **Explored** attack strategies and their complexity levels
4. **Discovered** how to implement red teaming in practice

**Next**: Ready to get hands-on? Let's set up your local environment and run your first AI red teaming scan!

---

**Navigation:** [Previous](./02-risk-categories-attack-strategies.md) | [Module Home](./README.md) | **Next:** [Module 2: Local Red Teaming](../02-local-red-teaming/README.md)