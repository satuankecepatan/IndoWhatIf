import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.electorate import generate_pancasila_voters_centrist, generate_candidates
from models.rules import run_indonesian_election
from models.alternatives import run_borda_count, run_instant_runoff, run_supplementary_vote

def run_scenario():
    print("="*50)
    print(" SCENARIO 1: PRE-JOKOWI ERA (The Fragmented Center)")
    print("="*50)
    
    voters = generate_pancasila_voters_centrist(n_voters=100000, seed=2004)
    
    candidate_dict = {
        "SBY (Center/Technocrat)": [0.0, 0.05],
        "Megawati (Secular/Establishment)": [0.2, 0.2],
        "Wiranto (Secular/Military)": [0.1, -0.1],
        "Amien Rais (Religious/Reformist)": [-0.2, 0.1],
        "Hamzah Haz (Religious/Grassroots)": [-0.3, -0.1]
    }
    candidate_names, candidates = generate_candidates(candidate_dict)
    
    print("\n[ SIMULATION 1: Standard UUD 1945 (Two-Round System) ]")
    run_indonesian_election(voters, candidates, candidate_names, noise=0.08)
    
    print("\n[ SIMULATION 2: Borda Count ]")
    run_borda_count(voters, candidates, candidate_names, noise=0.08)
    
    print("\n[ SIMULATION 3: Alternative Vote (AV/IRV) ]")
    run_instant_runoff(voters, candidates, candidate_names, noise=0.08)
    
    print("\n[ SIMULATION 4: Supplementary Vote (SV) ]")
    run_supplementary_vote(voters, candidates, candidate_names, noise=0.08)

if __name__ == "__main__":
    run_scenario()