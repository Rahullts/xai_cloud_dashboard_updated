import numpy as np

def get_feature_attributions(model, scaler, feature_names, raw_feature_dict):
    """
    Calculates local feature attributions for a Logistic Regression model.
    Attribution = scaled_feature_value * coefficient
    """
    # 1. Extract raw values in correct order
    raw_vals = np.array([[raw_feature_dict[f] for f in feature_names]])
    
    # 2. Scale values
    scaled_vals = scaler.transform(raw_vals)[0]
    
    # 3. Get coefficients
    coefs = model.coef_[0]
    
    # 4. Calculate attributions
    attributions = []
    for i, name in enumerate(feature_names):
        contrib = float(scaled_vals[i] * coefs[i])
        
        # Determine human readable name
        parts = name.split('_')
        metric = parts[0].capitalize() if parts[0] != 'net' else "Network " + parts[2].capitalize()
        if 'current' in name:
            hr_name = f"{metric} Current"
        elif 'mean' in name:
            hr_name = f"{metric} {parts[-1]}-step average"
        elif 'delta' in name:
            hr_name = f"{metric} {parts[-1]}-step delta"
        elif 'slope' in name:
            hr_name = f"{metric} {parts[-1]}-step trend"
        elif 'std' in name:
            hr_name = f"{metric} {parts[-1]}-step variability"
        else:
            hr_name = name
            
        attributions.append({
            "feature": name,
            "human_readable_name": hr_name,
            "raw_value": float(raw_vals[0][i]),
            "scaled_value": float(scaled_vals[i]),
            "coefficient": float(coefs[i]),
            "contribution": contrib,
            "abs_contribution": abs(contrib),
            "direction": "positive" if contrib > 0 else "negative"
        })
        
    # 5. Sort by absolute contribution and assign rank
    attributions.sort(key=lambda x: x["abs_contribution"], reverse=True)
    for i, attr in enumerate(attributions):
        attr["rank"] = i + 1
        
    return attributions
