from graph import get_paths_from_routes, trucks_from_file, knapsack
paths = get_paths_from_routes(2)
truck=trucks_from_file(0)
total_profit, used_paths, used_trucks, remaining_budget=knapsack(truck, paths, 100000000)
#print(total_profit, used_paths, used_trucks, remaining_budget)