import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.electorate import generate_pancasila_voters_centrist, generate_candidates
from models.rules import run_indonesian_election
from models.alternatives import run_borda_count, run_instant_runoff, run_supplementary_vote

def run_scenario():
    print("="*50)
    print(" SCENARIO 3: POST-JOKOWI ERA (Coalition Consolidation)")
    print("="*50)
    
    voters = generate_pancasila_voters_centrist(n_voters=100000, seed=2024)
    
    candidate_dict = {
        "Prabowo-Gibran (Center/Incumbent Establishment)": [0.0, 0.15],
        "Anies-Muhaimin (Religious/Change)": [-0.25, -0.1],
        "Ganjar-Mahfud (Secular/Grassroots)": [0.2, -0.1]
    }
    candidate_names, candidates = generate_candidates(candidate_dict)
    
    noise_level = 0.04 # to simulate the heavy structural machinery (bansos, coalition size) solidifies voting blocks, making them less random.
    
    print("\n[ SIMULATION 1: Standard UUD 1945 (Two-Round System) ]")
    run_indonesian_election(voters, candidates, candidate_names, noise=noise_level)
    
    print("\n[ SIMULATION 2: Borda Count ]")
    run_borda_count(voters, candidates, candidate_names, noise=noise_level)
    
    print("\n[ SIMULATION 3: Alternative Vote (AV/IRV) ]")
    run_instant_runoff(voters, candidates, candidate_names, noise=noise_level)
    
    print("\n[ SIMULATION 4: Supplementary Vote (SV) ]")
    run_supplementary_vote(voters, candidates, candidate_names, noise=noise_level)

if __name__ == "__main__":
    run_scenario()