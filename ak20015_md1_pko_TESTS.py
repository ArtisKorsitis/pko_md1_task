# Test cases for solving VRP (Vehicle routing problem) using SA (Simulated annealing) algorithm

import time
from ak20015_md1_pko import simulated_annealing

# Function to return non-random customer locations for each test case
def get_test_case_locations(num_customers):
    predefined_locations = {
        1: [(0, 0), (10, 20)],
        2: [(0, 0), (10, 20), (20, 30)],
        5: [(0, 0), (10, 20), (20, 30), (30, 40), (40, 50), (50, 60)],
        10: [(0, 0), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 45), (45, 50), (50, 55)],
        30: [(0, 0), (2, 3), (5, 10), (7, 15), (8, 20), (10, 25), (13, 30), (15, 35), (18, 40), (20, 45), (22, 50), 
             (25, 55), (28, 60), (30, 65), (33, 70), (35, 75), (37, 80), (40, 85), (43, 90), (45, 95), (48, 100), 
             (50, 105), (53, 110), (55, 115), (57, 120), (60, 125), (63, 130), (65, 135), (67, 140), (70, 145), (73, 150)],
        50: [(0, 0), (1, 5), (2, 9), (3, 12), (6, 15), (7, 18), (8, 22), (10, 25), (13, 30), (15, 32), (17, 35), (20, 40),
             (23, 42), (25, 45), (27, 50), (30, 55), (32, 58), (35, 60), (37, 65), (40, 70), (42, 75), (45, 80), (47, 85),
             (50, 90), (55, 95), (60, 100), (63, 105), (65, 110), (67, 115), (70, 120), (73, 125), (75, 130), (77, 135),
             (80, 140), (83, 145), (85, 150), (87, 155), (90, 160), (92, 165), (94, 170), (97, 175), (100, 180), (102, 185),
             (105, 190), (108, 195), (110, 200), (115, 205), (120, 210), (140, 230), (170, 260), (190, 280)]
    }
    
    return predefined_locations.get(num_customers, [(0, 0)])

# Test case specifications: (number of vehicles, number of customers)
test_case_specs = [
    # Special cases
    (0, 0),    # 0 vehicles    0 customers
    (1, 0),    # 1 vehicle     0 customers
    (0, 1),    # 0 vehicles    1 customer
    (1, 1),    # 1 vehicle     1 customer

    # Case when more vehicles than customers
    # Expected: Best Cost: 44.72 => same as (1, 1), meaning: only one vehicle is used
    (4, 1),    # 4 vehicles    1 customer

    # Normal cases
    (1, 5),    # 1 vehicle     5 customers
    (2, 5),    # 2 vehicles    5 customers
    (3, 5),    # 3 vehicles    5 customers
    (1, 10),   # 1 vehicle     10 customers
    (2, 10),   # 2 vehicles    10 customers
    (3, 10),   # 3 vehicles    10 customers
    (1, 30),   # 1 vehicle     30 customers
    (2, 30),   # 2 vehicles    30 customers
    (3, 30),   # 3 vehicles    30 customers
    (1, 50),   # 1 vehicle     50 customers
    (2, 50),   # 2 vehicles    50 customers
    (3, 50)    # 3 vehicles    50 customers
]

# Function to print the location tree
def print_location_tree(locations):
    print("Location Tree:")
    # Depot is always at (0, 0)
    print("Depot: (0, 0)")
    for i, location in enumerate(locations[1:], start=1):
        print(f"Customer {i}: {location}")
    print()

# Function to run test cases and record execution time and quality of solution
def run_test_cases(test_case_specs, initial_temp, cooling_rate, num_iterations):
    results = []
    for i, (num_vehicles, num_customers) in enumerate(test_case_specs):
        print(f"Running Test Case {i+1}: {num_vehicles} vehicle(s), {num_customers} customer(s)")
        
        # Get predefined locations
        locations = get_test_case_locations(num_customers)
        
        # Print location tree before running the test
        print_location_tree(locations)
        
        # Record start time
        start_time = time.time()
        
        # Run Simulated Annealing
        best_solution, best_cost = simulated_annealing(locations, num_vehicles, initial_temp, cooling_rate, num_iterations)
        
        # Record end time
        end_time = time.time()
        
        # Calculate execution time in seconds
        execution_time = end_time - start_time
        
        results.append({
            "Test Case": i + 1,
            "Num Vehicles": num_vehicles,
            "Num Customers": num_customers,
            "Best Solution": best_solution,
            "Best Cost": best_cost,
            "Execution Time (s)": f"{execution_time:.2f}"
        })
        
        print(f"Test Case {i+1} completed. Best Cost: {best_cost}")
        print(f"Execution Time: {execution_time:.2f} seconds\n")
        print(f"Best Solution: {best_solution}\n")
    
    return results

# Parameters for the Simulated Annealing algorithm
initial_temp = 1000
cooling_rate = 0.995
num_iterations = 10000

# Run the test cases
run_test_cases(test_case_specs, initial_temp, cooling_rate, num_iterations)
