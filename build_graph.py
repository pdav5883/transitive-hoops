import json
import networkx as nx
from typing import Dict, List
from collections import defaultdict
def load_games(filename: str) -> List[Dict]:
    """Load games from JSON file"""
    with open(filename, 'r') as f:
        return json.load(f)

def build_game_graph(games: List[Dict]) -> nx.DiGraph:
    """
    Build a directed graph where:
    - Nodes are teams
    - Edges point from winner to loser
    - Edge weights are the total point differential
    - Edge N property tracks number of wins
    - Edge date property records when game was last played
    """
    G = nx.DiGraph()
    
    for game in games:
        home_score = game['score_home']
        away_score = game['score_away']
        home_team = game['home_team']
        away_team = game['away_team']
        game_date = game['date']
        
        # Skip games with no scores (not played yet or cancelled)
        if not home_score or not away_score:
            continue
        else:
            home_score = float(home_score)
            away_score = float(away_score)
            
        # Determine winner and loser
        if home_score > away_score:
            winner = home_team
            loser = away_team
            margin = home_score - away_score
        else:
            winner = away_team
            loser = home_team
            margin = away_score - home_score
        
        # If edge already exists, update properties
        if G.has_edge(winner, loser):
            G[winner][loser]['weight'] += margin  # Add to total margin
            G[winner][loser]['N'] += 1  # Increment number of wins
            G[winner][loser]['date'] = game_date  # Update to most recent date
        else:
            # Add new edge with initial properties
            G.add_edge(winner, loser, weight=margin, N=1, date=game_date)
    
    return G

def print_graph_stats(G: nx.DiGraph):
    """Print basic statistics about the graph"""
    # Count total number of games (sum of all edges)
    total_games = sum(e['N'] for _, _, e in G.edges(data=True))
    
    print(f"Number of teams (nodes): {G.number_of_nodes()}")
    print(f"Number of games (edges): {total_games}")
    
    print("\nStatistics:")
    # Count wins for each team (accounting for multiple games between same teams)
    team_wins = defaultdict(int)
    for u, _, e in G.edges(data=True):
        team_wins[u] += e['N']
    
    # Find team with most wins
    most_wins = max(team_wins.items(), key=lambda x: x[1])
    print(f"Team with most wins: {most_wins[0]} ({most_wins[1]} wins)")
    
    # Count losses for each team
    team_losses = {}
    for u, v, data in G.edges(data=True):
        team_losses[v] = team_losses.get(v, 0) + 1
    
    # Find team with most losses
    most_losses = max(team_losses.items(), key=lambda x: x[1])
    print(f"Team with most losses: {most_losses[0]} ({most_losses[1]} losses)")

def main():
    # Load games from JSON
    games = load_games('basketball_games.json')
    
    # Build the graph
    G = build_game_graph(games)
    
    # Print some basic statistics
    print_graph_stats(G)
    
    # Save the graph (optional)
    # Can be loaded later with nx.read_gexf('basketball_graph.gexf')
    nx.write_gexf(G, 'basketball_graph.gexf')

if __name__ == "__main__":
    main()
