import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.electorate import generate_pancasila_voters_bimodal, generate_candidates
from models.rules import run_indonesian_election
from models.alternatives import run_borda_count, run_instant_runoff, run_supplementary_vote

def run_scenario():
    print("="*50)
    print(" SCENARIO 2: JOKOWI ERA (Bimodal Polarization)")
    print("="*50)
    
    voters = generate_pancasila_voters_bimodal(n_voters=100000, polarization_dist=0.25, seed=2014)
    
    candidate_dict = {
        "Jokowi (Secular-leaning/Populist)": [0.25, -0.25],
        "Prabowo (Religious-leaning/Establishment)": [-0.25, 0.25]
    }
    candidate_names, candidates = generate_candidates(candidate_dict)
    
    print("\n[ SIMULATION 1: Standard UUD 1945 (Two-Round System) ]")
    run_indonesian_election(voters, candidates, candidate_names, noise=0.05)
    
    print("\n[ SIMULATION 2: Borda Count ]")
    run_borda_count(voters, candidates, candidate_names, noise=0.05)
    
    print("\n[ SIMULATION 3: Alternative Vote (AV/IRV) ]")
    run_instant_runoff(voters, candidates, candidate_names, noise=0.05)
    
    print("\n[ SIMULATION 4: Supplementary Vote (SV) ]")
    run_supplementary_vote(voters, candidates, candidate_names, noise=0.05)

if __name__ == "__main__":
    run_scenario()