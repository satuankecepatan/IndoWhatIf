import sys
import time
from eras.pre_jokowi import run_scenario as run_pre_jokowi
from eras.jokowi_era import run_scenario as run_jokowi_era
from eras.post_jokowi import run_scenario as run_post_jokowi

def print_header():
    print("==========================================================")
    print(" ELECTION SIMULATOR 3000: INDONESIA 'WHAT IF' EDITION")
    print(" Analyzing the Pancasila Spatial Model")
    print("==========================================================")
    print("Select an era to simulate under different electoral rules:\n")
    print("  [1] Pre-Jokowi (2004/2009) - The Fragmented Center")
    print("  [2] Jokowi Era (2014/2019) - Bimodal Polarization")
    print("  [3] Post-Jokowi (2024+)    - Coalition Consolidation")
    print("  [4] Run All Eras Sequentially")
    print("  [5] Exit")
    print("==========================================================")

def main():
    while True:
        print_header()
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice == '1':
            print("\nInitializing Pre-Jokowi Simulation...")
            time.sleep(1)
            run_pre_jokowi()
            input("\nPress Enter to return to the main menu...")
            
        elif choice == '2':
            print("\nInitializing Jokowi Era Simulation...")
            time.sleep(1)
            run_jokowi_era()
            input("\nPress Enter to return to the main menu...")
            
        elif choice == '3':
            print("\nInitializing Post-Jokowi Simulation...")
            time.sleep(1)
            run_post_jokowi()
            input("\nPress Enter to return to the main menu...")
            
        elif choice == '4':
            print("\nRunning Full Historical Suite...")
            time.sleep(1)
            run_pre_jokowi()
            print("\n" + "*"*50 + "\n")
            time.sleep(1)
            run_jokowi_era()
            print("\n" + "*"*50 + "\n")
            time.sleep(1)
            run_post_jokowi()
            input("\nPress Enter to return to the main menu...")
            
        elif choice == '5':
            print("\nExiting Election Simulator. Terima kasih!")
            sys.exit(0)
            
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")
            time.sleep(1)
            
        # Clear screen hack for cross-platform (optional, just prints newlines)
        print("\n" * 2)

if __name__ == "__main__":
    main()