# This is the "What If" in the name of the project.

from .rules import calculate_utilities
import numpy as np

def get_ranked_ballots(utilities):
    return np.argsort(-utilities, axis=1) # converts raw utility scores into ranked preference ballots

def run_borda_count(voters, candidates, candidate_names, noise=0.05):
    # Borda Count:
    # Voters rank all candidates, points awarded based on rank
    utilities = calculate_utilities(voters, candidates, noise_level=noise)
    rankings = get_ranked_ballots(utilities)

    n_voters, n_candidates = rankings.shape
    scors = np.zeros(n_candidates)

    print("\nBorda Count Election")
    for rank in range(n_candidates):
        points_awarded = n_candidates - 1 - rank
        candidates_at_rank = rankings[:, rank]
        counts = np.bincount(candidates_at_rank, minlength=n_candidates)
        scores += counts * points_awarded
    
    results = sorted(zip(candidate_names, scores), key=lambda x: x[1], reverse=True)

    for name, score in results:
        print(f"{name}: {int(score):,} points.")
    
    print(f"Result: {results[0][0]} wins the Borda Count.")
    return results[0][0]

## TODO: SV, AV, others... I'm too tired rn.