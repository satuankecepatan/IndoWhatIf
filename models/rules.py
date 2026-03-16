import numpy as np

def calculate_utilities(voters, candidates, noise_level=0.0):
    # Calculate the Eucledian distance between every voter and every candidate.
    # Voters: (N, 2); Candidates: (C, 2)
    # The resulting distance matrix is going to be (N, C)

    diff = voters[:, np.newaxis, :] - candidates[np.newaxis, :, :]
    distances = np.linalg.norm(diff, axis=2)

    utilities = -distances # the closer the better

    if noise_level > 0:
        noise = np.random.normal(scale=noise_level, size=utilities.shape)
        utilities += noise
    
    return utilities

def simulate_round(utilities):
    n_voters = utilities.shape[0]
    votes = np.argmax(utilities, axis=1) # each voter picks the candidate with highest utility
    vote_counts = np.bincount(votes, minlength=utilities.shape[1])
    vote_percentages = (vote_counts / n_voters) * 100
    return vote_counts, vote_percentages

def check_constitutional_threshold(vote_percentages):
    # Indonesian constitutional requires someone to get >0% of the national vote to win in a single round.
    # The rule requiring >20% of votes in over half the provinces is abstracted here
    top_candidate_idx = np.argmax(vote_percentages)
    if vote_percentages[top_candidate_idx] > 50.0:
        return top_candidate_idx
    return None

def run_indonesian_election(voters, candidates, candidate_names, noise=0.05):
    """
    Master wrapper function for the whole election process.
    """
    utilities = calculate_utilities(voters, candidates, noise_level=noise)

    print("Round 1")
    r1_counts, r1_pcts = simulate_round(utilities)
    
    r1_results = sorted(
        zip(candidate_names, r1_pcts, range(len(candidate_names))),
        key=lambda x: x[1],
        reverse=True
    )

    for name, pct, idx in r1_results:
        print(f"{name}: {pct:.2f}%")
    
    winner_idx = check_constitutional_threshold(r1_pcts) # check for winner

    if winner_idx is not None:
        winner_name = candidate_names[winner_idx]
        print(f"\nResult: {winner_name} wins outright in Round 1.")
        return {"winner": winner_name, "rounds": 1, "r1_results": r1_results}
    print("\nNo candidate reached 50%+1.")

    print("Round 2.")

    top_two_indices = [r1_results[0][2], r1_results[1][2]]
    top_two_names = [r1_results[0][0], r1_results[1][0]]

    r2_utilities = utilities[:, top_two_indices]
    r2_counts, r2_pcts = simulate_round(r2_utilities)

    r2_results = sorted(
        zip(top_two_names, r2_pcts),
        key=lambda x: x[1],
        reverse=True
    )

    for name, pct in r2_results:
        print(f"{name}: {pct:.2f}%")
    
    winner_name = r2_results[0][0]
    print(f"\nResult: {winner_name} wins the Runoff in Round 2.")

    return {"winner": winner_name, "rounds": 2, "r1_results": r1_results, "r2_results": r2_results}