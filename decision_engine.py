def get_risk_level(probability):
    """Classifies model probability into a risk tier."""
    if probability < 0.30: return "LOW"
    if probability < 0.60: return "MEDIUM"
    if probability < 0.85: return "HIGH"
    return "CRITICAL"

def get_recommended_action(category):
    """Maps root cause category to recommended action."""
    mapping = {
        'CPU Spike': 'Scale CPU / restart affected workload',
        'Memory Leak': 'Restart affected service / reclaim memory',
        'Disk Exhaustion': 'Clean temporary data / expand storage',
        'Network Degradation': 'Check/restart network service / reroute where applicable',
        'Combined Failure': 'Controlled recovery sequence + alert',
        'Unknown / Mixed': 'Alert operator and avoid unsafe autonomous action'
    }
    return mapping.get(category, 'Alert operator and avoid unsafe autonomous action')

def generate_explanation(probability, category, attributions):
    """Generates a human-readable explanation from the XAI inputs."""
    risk = get_risk_level(probability)
    
    # Filter to top 3 positive contributors
    top_positives = [a for a in attributions if a['direction'] == 'positive'][:3]
    
    if not top_positives:
        return (f"The model detected a {risk} failure risk (score: {probability:.2f}). "
                f"However, no strong positive indicators were identified, suggesting normal variance.")
    
    feat_strs = []
    for f in top_positives:
        feat_strs.append(f"{f['human_readable_name']} ({f['raw_value']:.2f})")
        
    explanation = (f"The model detected a {risk} failure risk (model score: {probability:.2f}). "
                   f"Evidence supports a likely root cause of: {category.upper()}. "
                   f"The most influential indicators are: {', '.join(feat_strs)}.")
                   
    return explanation
