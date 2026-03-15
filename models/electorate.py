# This is Pancasila mathematized.
# Pancasila is highly constrained.
# It'll be reflected on the code, watch.

import numpy as np

def generate_pancasila_voters_centrist(n_voters=100000, seed=67): # hehe
    """
    This is going to simulate two eras.
    1. Pre-Jokowi
    2. Post-Jokowi
    Why Jokowi? We need a baseline.
    Before Jokowi our elections are volatile.
    Jokowi seems like a good baseline for this simulation.
    """
    if seed is not None:
        np.random.seed(seed)
    
    voters = np.random.normal(loc=[0.0, 0.0], scale=[0.15, 0.15], size=(n_voters, 2)) # the scale being this small means a tight cluster
    voters = np.clip(voters, -0.45, 0.45) # hard boundary to keep the voters moderate
    # you can't even have communism here
    # thus this simulates "fringe ideologies are forbidden"
    return voters

def generate_pancasila_voters_bimodal(n_voters=100000, polarization_dist=0.25, seed=67):
    """
    The reason why Jokowi is a good baseline is that in his two terms,
    there's only two "camps" that are competing.
    1. Prabowo
    2. Jokowi
    """
    if seed is not None:
        np.random.seed(seed)
    
    n_camp1 = n_voters // 2
    n_camp2 - n_voters - n_camp1

    # camp1 is the Prabowo base
    camp1 = np.random.normal(
        loc=[-polarization_dist, -polarization_dist],
        scale=[0.12, 0.12],
        size=(n_camp1, 2)
    )

    # and camp2 is the Jokowi base
    camp2 = np.random.normal(
        loc=[polarization_dist, polarization_dist],
        scale=[0.12, 0.12],
        size=(n_camp2, 2)
    )

    voters = np.vstack((camp1, camp2))
    np.random.shuffle(voters)
    voters = np.clip(voters, -0.6, 0.6)
    return voters

def generate_candidates(coordinates_dict):
    """
    Helper function to format candidate locations.
    """
    names = list(coordinates_dict.keys())
    coords = np.array(list(coordinates_dict.values()))
    return names, coords