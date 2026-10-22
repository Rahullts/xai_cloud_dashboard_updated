def get_feature_group(feature_name):
    """Maps a temporal feature to its primary resource group."""
    if feature_name.startswith('cpu_'): return 'CPU'
    if feature_name.startswith('memory_'): return 'Memory'
    if feature_name.startswith('disk_'): return 'Disk'
    if feature_name.startswith('net_'): return 'Network'
    return 'Unknown'

def determine_root_cause(attributions):
    """
    Aggregates positive feature attributions by resource group to determine 
    the most likely root cause category.
    """
    scores = {'CPU': 0.0, 'Memory': 0.0, 'Disk': 0.0, 'Network': 0.0}
    
    # We only aggregate POSITIVE contributions because those are the ones 
    # driving the prediction towards 1 (Failure)
    for attr in attributions:
        grp = get_feature_group(attr['feature'])
        if grp in scores and attr['contribution'] > 0:
            scores[grp] += attr['contribution']
            
    total = sum(scores.values())
    if total <= 0:
        return "Unknown / Mixed", {k: 0.0 for k in scores}
        
    # Normalize scores
    norm_scores = {k: v / total for k, v in scores.items()}
    
    # Sort groups by score
    sorted_groups = sorted(norm_scores.items(), key=lambda x: -x[1])
    top_group, top_score = sorted_groups[0]
    second_group, second_score = sorted_groups[1]
    
    # Decision Logic
    # If the top group dominates (> 50% and safely above second group)
    if top_score > 0.45 and (top_score - second_score) > 0.15:
        mapping = {
            'CPU': 'CPU Spike',
            'Memory': 'Memory Leak',
            'Disk': 'Disk Exhaustion',
            'Network': 'Network Degradation'
        }
        category = mapping[top_group]
    elif top_score > 0.3 and second_score > 0.25:
        category = 'Combined Failure'
    else:
        category = 'Unknown / Mixed'
        
    return category, norm_scores
