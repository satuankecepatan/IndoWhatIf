import sys
import os
import time
import matplotlib.pyplot as plt
import seaborn as sns

from eras.pre_jokowi import run_scenario as run_pre_jokowi
from eras.jokowi_era import run_scenario as run_jokowi_era
from eras.post_jokowi import run_scenario as run_post_jokowi

from models.electorate import generate_pancasila_voters_centrist, generate_pancasila_voters_bimodal, generate_candidates

# --- DUAL LOGGER CLASS ---
class DualLogger:
    """
    Intercepts standard output to print to the terminal AND save to a log file simultaneously.
    """
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.log = open(filepath, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()
        
    def close(self):
        self.log.close()

# --- SPATIAL PLOTTING LOGIC ---
def plot_spatial_model(title, voters, candidates, candidate_names, filepath):
    """
    Generates a 2D scatter plot of the Pancasila spatial model and saves it.
    """
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 8))
    
    # Plot voters (using low alpha so dense clusters look darker)
    plt.scatter(voters[:, 0], voters[:, 1], alpha=0.05, color='royalblue', s=15, label='Electorate Density')
    
    # Plot candidates
    colors = sns.color_palette("husl", len(candidate_names))
    for i, (name, coord) in enumerate(zip(candidate_names, candidates)):
        plt.scatter(coord[0], coord[1], color=colors[i], s=250, marker='*', edgecolor='black', zorder=5)
        # Add labels slightly offset
        short_name = name.split(" ")[0] # Just grab the first word for cleaner plotting
        plt.text(coord[0] + 0.02, coord[1] + 0.02, short_name, fontsize=11, fontweight='bold', zorder=6)
        
    # Formatting the axes to represent Pancasila ideology
    plt.title(f"{title} - Spatial Distribution", fontsize=16, pad=15)
    plt.xlabel("← Nationalist-Religious      |      Nationalist-Secular →", fontsize=12, fontweight='bold')
    plt.ylabel("← Populist/Grassroots      |      Establishment/Technocrat →", fontsize=12, fontweight='bold')
    
    # Set rigid limits to show how tightly clustered Pancasila politics is
    plt.xlim(-1.0, 1.0)
    plt.ylim(-1.0, 1.0)
    
    plt.axhline(0, color='black', linewidth=1, linestyle='--', alpha=0.5)
    plt.axvline(0, color='black', linewidth=1, linestyle='--', alpha=0.5)
    
    # Save the plot
    plt.savefig(filepath, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"📊 Plot saved successfully to: {filepath}")

# --- MENU AND EXECUTION LOGIC ---
def ensure_directories():
    os.makedirs('outputs/logs', exist_ok=True)
    os.makedirs('outputs/plots', exist_ok=True)

def print_header():
    print("==========================================================")
    print(" ELECTION SIMULATOR 3000: INDONESIA 'WHAT IF' EDITION")
    print(" Analyzing the Pancasila Spatial Model")
    print("==========================================================")
    print("Select an era to simulate under different electoral rules:\n")
    print("  [1] Pre-Jokowi (2004/2009) - The Fragmented Center")
    print("  [2] Jokowi Era (2014/2019) - Bimodal Polarization")
    print("  [3] Post-Jokowi (2024+)    - Coalition Consolidation")
    print("  [4] Exit")
    print("==========================================================")

def execute_scenario(scenario_func, log_filename, plot_title, plot_filename, generation_logic):
    """
    Wraps the scenario execution with our logger and plotter.
    """
    log_path = os.path.join('outputs', 'logs', log_filename)
    plot_path = os.path.join('outputs', 'plots', plot_filename)
    
    original_stdout = sys.stdout
    logger = DualLogger(log_path)
    sys.stdout = logger
    
    try:
        # 1. Run the terminal simulation (which now dual-logs to the file)
        scenario_func()
    finally:
        # Always restore standard output even if simulation fails
        sys.stdout = original_stdout
        logger.close()
        
    print(f"\n📝 Simulation log saved to: {log_path}")
    
    # 2. Generate the plot
    print("Generating spatial plot visualization...")
    voters, candidates, candidate_names = generation_logic()
    plot_spatial_model(plot_title, voters, candidates, candidate_names, plot_path)

def main():
    ensure_directories()
    
    while True:
        print_header()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            def pre_jokowi_data():
                # Recreate just 5,000 voters for a cleaner visual plot, using exact same seed
                v = generate_pancasila_voters_centrist(n_voters=5000, seed=2004)
                c_dict = {
                    "SBY": [0.0, 0.05], "Megawati": [0.2, 0.2], 
                    "Wiranto": [0.1, -0.1], "Amien Rais": [-0.2, 0.1], 
                    "Hamzah Haz": [-0.3, -0.1]
                }
                names, coords = generate_candidates(c_dict)
                return v, coords, names
                
            execute_scenario(run_pre_jokowi, 'pre_jokowi_log.txt', 'Pre-Jokowi Era (2004/2009)', 'pre_jokowi_map.png', pre_jokowi_data)
            input("\nPress Enter to return to the main menu...")
            
        elif choice == '2':
            def jokowi_era_data():
                v = generate_pancasila_voters_bimodal(n_voters=5000, polarization_dist=0.25, seed=2014)
                c_dict = {
                    "Jokowi": [0.25, -0.25], "Prabowo": [-0.25, 0.25]
                }
                names, coords = generate_candidates(c_dict)
                return v, coords, names
                
            execute_scenario(run_jokowi_era, 'jokowi_era_log.txt', 'Jokowi Era (2014/2019)', 'jokowi_era_map.png', jokowi_era_data)
            input("\nPress Enter to return to the main menu...")
            
        elif choice == '3':
            def post_jokowi_data():
                v = generate_pancasila_voters_centrist(n_voters=5000, seed=2024)
                c_dict = {
                    "Prabowo-Gibran": [0.0, 0.15], "Anies-Muhaimin": [-0.25, -0.1], 
                    "Ganjar-Mahfud": [0.2, -0.1]
                }
                names, coords = generate_candidates(c_dict)
                return v, coords, names
                
            execute_scenario(run_post_jokowi, 'post_jokowi_log.txt', 'Post-Jokowi Era (2024+)', 'post_jokowi_map.png', post_jokowi_data)
            input("\nPress Enter to return to the main menu...")
            
        elif choice == '4':
            print("\nExiting Election Simulator. Terima kasih!")
            sys.exit(0)
            
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")
            time.sleep(1)
            
        print("\n" * 2)

if __name__ == "__main__":
    main()