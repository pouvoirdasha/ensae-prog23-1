from graph import get_paths_from_routes, trucks_from_file, knapsack
paths = get_paths_from_routes(1)
truck=trucks_from_file(0)
print(truck)
total_profit, used_paths, used_trucks, remaining_budget=knapsack(truck, paths, 10000000)
print(total_profit, used_paths, used_trucks, remaining_budget)