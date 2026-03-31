import pandas as pd

# ==============================
# CONSTANTS
# ==============================
DOMAINS = ["GOLEK", "RIASEC", "LearningStyle", "Verbal", "Strength", "Technical", "WorkValues"]

WEIGHTS = {
    "GOLEK": 0.18,
    "RIASEC": 0.14,
    "LearningStyle": 0.14,
    "Verbal": 0.14,
    "Strength": 0.18,
    "Technical": 0.12,
    "WorkValues": 0.10
}

# ==============================
# FEATURE PREPARATION
# ==============================
def prepare_features(scores_df):
    """
    Converts dataframe into ordered feature list
    Expected columns: section, normalized
    """
    try:
        s = scores_df.set_index("section")["normalized"]
    except Exception as e:
        raise ValueError(f"Invalid input dataframe format: {e}")

    # Ensure correct order
    features = [float(s.get(domain, 0)) for domain in DOMAINS]
    return features

# ==============================
# TVET INDEX CALCULATION
# ==============================
def compute_tvet_index(features):
    """
    Computes weighted TVET index and returns label
    """
    if len(features) != len(DOMAINS):
        raise ValueError("Feature length mismatch with domains")

    index = sum(features[i] * WEIGHTS[DOMAINS[i]] for i in range(len(DOMAINS)))

    # Convert to percentage scale (optional, safer)
    index = round(index, 2)

    if index >= 75:
        label = "Strong Preference"
    elif index >= 55:
        label = "Moderate Preference"
    else:
        label = "Low Preference"

    return index, label