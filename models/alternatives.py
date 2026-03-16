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

def run_instant_runoff(voters, candidates, candidate_names, noise=0.05): # AV
    utilities = calculate_utilities(voters, candidates, noise_level=noise)
    rankings = get_ranked_ballots(utilities)

    n_voters, n_candidates = rankings.shape
    active_candidates = set(range(n_candidates))

    print("\nInstant Runoff Election (AV)")
    
    round_num = 1
    while len(active_candidates) > 1:
        print(f"Round {round_num}:")
        # First preference for each voter
        active_mask = np.isin(rankings, list(active_candidates))
        first_active_indices = np.argmax(active_mask, axis=1)
        current_votes = rankings[np.arange(n_voters), first_active_indices]

        counts = np.bincount(current_votes, minlength=n_candidates)
        pcts = (counts / n_voters) * 100

        standings = [(candidate_names[i], pcts[i], i) for i in active_candidates]
        standings.sort(key=lambda x: x[1], reverse=True)

        for name, pct, _ in standings:
            print(f"  {name}: {pct:.2f}%")
        
        top_pct = standings[0][1]
        top_name = standings[0][0]

        if top_pct > 50:
            print(f"Result: {top_name} wins with {top_pct:.2f}%")
            return top_name
        
        lowest_id = standings[-1][2]
        lowest_name = standings[-1][0]
        print(f"  -> Eliminating {lowest_name}. Transferring votes...\n")
        active_candidates.remove(lowest_id)

        round_num += 1
    
    winner_idx = list(active_candidates)[0] # for when there's only one candidate left
    print(f"Result {candidate_names[winner_idx]} wins.")
    return candidate_names[winner_idx]

def run_supplementary_vote(voters, candidates, candidate_names, noise=0.05): # SV
    utilities = calculate_utilities(voters, candidates, noise_level=noise)
    rankings = get_ranked_ballots(utilities)

    n_voters, n_candidates = rankings.shape

    print("\nSupplementary Vote Election.")
    print("Round 1: First Preferences.")

    first_choices = rankings[:, 0]
    r1_counts = np.bincount(first_choices, minlength=n_candidates)
    r1_pcts = (r1_counts / n_voters) * 100

    r1_results = sorted(zip(
        candidate_names,
        r1_pcts,
        range(n_candidates)),
        key=lambda x: x[1],
        reverse=True
    )

    for name, pct, _ in r1_results:
        print(f"  {name}: {pct:.2f}%")
    
    if r1_results[0][1] > 50:
        print(f"Result: {r1_results[0][0]} wins.")
        return r1_results[0][0]

    print("\nNo candidate reached 50%, eliminating all but Top 2...")
    top_two_ids = {r1_results[0][2], r1_results[1][2]}
    eliminated_mask = ~np.isin(first_choices, list(top_two_ids))
    second_choices = rankings[eliminated_mask, 1]
    valid_transfers = second_choices[np.isin(second_choices, list(top_two_ids))]
    transfer_counts = np.bincount(valid_transfers, minlength=n_candidates)

    print("\nRound 2: First Preferences + Valid Second Preferences.")
    final_counts = np.zeros(n_candidates)
    for c_id in top_two_ids:
        final_counts[c_id] = r1_counts[c_id] + transfer_counts[c_id]
    
    total_valid_votes = np.sum(final_counts)
    final_pcts = (final_counts / total_valid_votes) * 100

    r2_results = sorted(zip(
        candidate_names,
        final_pcts,
        range(n_candidates)),
        key=lambda x: x[1],
        reverse=True
    )

    for name, pct, _ in r2_results:
        print(f"  {name}: {pct:.2f}%")
    
    print(f"Result: {r2_results[0][0]} wins the Supplementary Vote.")
    return r2_results[0][0]