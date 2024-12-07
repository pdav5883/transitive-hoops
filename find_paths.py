import networkx as nx
import argparse
from datetime import datetime
from typing import List, Dict

def load_graph(filename: str) -> nx.DiGraph:
    """Load the graph from GEXF file"""
    return nx.read_gexf(filename)

def format_path(G: nx.DiGraph, path: List[str]) -> str:
    """Format a path as a readable string with game details"""
    result = []
    for i in range(len(path) - 1):
        team1, team2 = path[i], path[i+1]
        edge_data = G[team1][team2]
        result.append(
            f"{team1} beat {team2} by {edge_data['weight']} on {edge_data['date']}"
        )
    return " → ".join(result)

def find_and_group_paths(G: nx.DiGraph, team1: str, team2: str, cutoff: int) -> Dict[int, List[List[str]]]:
    """Find all paths between teams and group them by length"""
    # Verify teams exist in graph
    if team1 not in G or team2 not in G:
        raise ValueError("One or both teams not found in graph")
    
    # Get all paths up to cutoff length
    paths = list(nx.all_simple_paths(G, team1, team2, cutoff=cutoff))
    
    # Group paths by length
    grouped_paths = {}
    for path in paths:
        path_length = len(path) - 1  # Number of edges in path
        if path_length not in grouped_paths:
            grouped_paths[path_length] = []
        grouped_paths[path_length].append(path)
    
    return grouped_paths

def main():
    parser = argparse.ArgumentParser(description='Find paths between two teams')
    parser.add_argument('team1', help='First team name')
    parser.add_argument('team2', help='Second team name')
    parser.add_argument('--cutoff', type=int, default=4, 
                       help='Maximum path length (default: 4)')
    parser.add_argument('--graph', default='basketball_graph.gexf',
                       help='Path to graph file (default: basketball_graph.gexf)')
    
    args = parser.parse_args()
    
    # Load the graph
    G = load_graph(args.graph)
    
    try:
        grouped_paths = find_and_group_paths(G, args.team1, args.team2, args.cutoff)
        
        if not grouped_paths:
            print(f"No paths found from {args.team1} to {args.team2} "
                  f"within {args.cutoff} steps")
            return
        
        # Print paths grouped by length
        total_paths = sum(len(paths) for paths in grouped_paths.values())
        print(f"\nFound {total_paths} paths from {args.team1} to {args.team2}")
        print(f"Maximum path length: {args.cutoff}\n")
        
        for length in sorted(grouped_paths.keys()):
            paths = grouped_paths[length]
            print(f"\nPaths of length {length} ({len(paths)} paths):")
            print("-" * 40)
            for path in paths:
                print(format_path(G, path))
                print()
                
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 