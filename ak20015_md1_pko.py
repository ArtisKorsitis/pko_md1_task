# Code to solve VRP (Vehicle routing problem) using SA (Simulated annealing) algorithm

import random
import math

# Function to calculate distance between two points
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Function to calculate total route cost (distance)
def total_route_distance(routes, locations):
    total_distance = 0
    for route in routes:
        # Only calculate distance for non-empty routes
        if route:
            # Depot to first customer
            total_distance += distance(locations[0], locations[route[0]])
            for i in range(len(route) - 1):
                total_distance += distance(locations[route[i]], locations[route[i + 1]])
            # Last customer back to depot
            total_distance += distance(locations[route[-1]], locations[0])
    return total_distance

# Function to generate the initial solution (assign customers to vehicles)
def generate_initial_solution(num_vehicles, num_customers):
    # Customers indexed from 1
    customers = list(range(1, num_customers + 1))
    random.shuffle(customers)
    routes = [[] for _ in range(num_vehicles)]

    # Only assign customers to as many vehicles as needed
    for i, customer in enumerate(customers):
        routes[i % min(num_vehicles, num_customers)].append(customer)
    return routes

# Function to perturb the solution by shuffling or swapping customers
def perturb_solution(routes):
    new_routes = [route[:] for route in routes]
    
    # Case for 1 vehicle
    if len(new_routes) == 1:
        # Shuffle customers within the single route
        random.shuffle(new_routes[0])
    else:
        # Ignore empty routes
        non_empty_routes = [i for i, route in enumerate(new_routes) if route]
        if len(non_empty_routes) > 1:
            route1, route2 = random.sample(non_empty_routes, 2)
            customer1 = random.choice(new_routes[route1])
            customer2 = random.choice(new_routes[route2])
            new_routes[route1].remove(customer1)
            new_routes[route2].remove(customer2)
            new_routes[route1].append(customer2)
            new_routes[route2].append(customer1)
    return new_routes

# Simulated Annealing algorithm with special case handling
def simulated_annealing(locations, num_vehicles, initial_temp, cooling_rate, num_iterations):
    num_customers = len(locations) - 1  # Depot is not counted as a customer

    # Special case: No vehicles and no customers
    if num_vehicles == 0 and num_customers == 0:
        print("No vehicles and no customers. Nothing to optimize.")
        return [], 0

    # Special case: 1 vehicle and 0 customers
    if num_vehicles == 1 and num_customers == 0:
        print("1 vehicle but no customers to serve.")
        return [[]], 0

    # Special case: No vehicles but some customers
    if num_vehicles == 0 and num_customers > 0:
        print(f"{num_customers} customer(s), but no vehicles available. No solution possible.")
        return [], float('inf')

    # Special case: 1 vehicle and 1 customer (trivial case)
    if num_vehicles == 1 and num_customers == 1:
        print("1 vehicle and 1 customer. Trivial solution.")
        return [[1]], format(2 * distance(locations[0], locations[1]), ".2f")

    # Regular case: Proceed with the Simulated Annealing algorithm
    current_solution = generate_initial_solution(num_vehicles, num_customers)
    current_cost = total_route_distance(current_solution, locations)
    best_solution = current_solution
    best_cost = current_cost
    temperature = initial_temp

    for _ in range(num_iterations):
        new_solution = perturb_solution(current_solution)
        new_cost = total_route_distance(new_solution, locations)
        delta_cost = new_cost - current_cost

        if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / temperature):
            current_solution = new_solution
            current_cost = new_cost

        if current_cost < best_cost:
            best_solution = current_solution
            best_cost = current_cost

        temperature *= cooling_rate

    return best_solution, format(best_cost, ".2f")
