import numpy as np
from collections import defaultdict

# Define the Bayesian Network
cpt = {
    'Weather': {'Sunny': 0.6, 'Rainy': 0.4},  # P(Weather)
    'Time': {'Morning': 0.5, 'Evening': 0.5},  # P(Time)
    'Traffic': {
        ('Sunny', 'Morning'): {'Light': 0.8, 'Heavy': 0.2},
        ('Sunny', 'Evening'): {'Light': 0.6, 'Heavy': 0.4},
        ('Rainy', 'Morning'): {'Light': 0.3, 'Heavy': 0.7},
        ('Rainy', 'Evening'): {'Light': 0.4, 'Heavy': 0.6},
    }
}

def sample_from_distribution(distribution):
    return np.random.choice(list(distribution.keys()), p=list(distribution.values()))

def monte_carlo_simulation(cpt, target, evidence, num_samples=10000):
    counts = defaultdict(int)
    valid_samples = 0

    for _ in range(num_samples):
        sample = {}
        sample['Weather'] = sample_from_distribution(cpt['Weather'])
        sample['Time'] = sample_from_distribution(cpt['Time'])
        sample['Traffic'] = sample_from_distribution(cpt['Traffic'][(sample['Weather'], sample['Time'])])

        is_valid = all(sample[node] == value for node, value in evidence.items())
        if is_valid:
            valid_samples += 1
            counts[sample[target]] += 1

    probabilities = {state: count / valid_samples for state, count in counts.items()}
    return probabilities, valid_samples

evidence = {'Weather': 'Rainy'}  
target = 'Traffic'             

probabilities, valid_samples = monte_carlo_simulation(cpt, target, evidence)

print(f"Estimated probabilities for {target} given {evidence}: {probabilities}")
print(f"Number of valid samples: {valid_samples}")
