import tqdm as tqdm
import pandas as pd
import numpy as np


class Graph():
    def __init__(self, edges_df: pd.DataFrame):
        self.graph = {}
        self.all_authors = list(set(edges_df['author1']).union(set(edges_df['author2'])))
        
        for i, row in tqdm.tqdm(edges_df.iterrows(), total=len(edges_df), desc='Building graph'):
            # Extract row information
            source = int(row['author1'])
            destination = int(row['author2'])
            strength = row['power']
            
            # Add source and destination to graph if not already present
            if source not in self.graph:
                self.graph[source] = {
                    'neighbours': [],
                    'total_strength': 0
                }
                
            if destination not in self.graph:
                self.graph[destination] = {
                    'neighbours': [],
                    'total_strength': 0
                }
                
            # Add edge to graph
            self.graph[source]['neighbours'].append({'destination': destination, 'strength': strength})
            self.graph[source]['total_strength'] += strength
            
            self.graph[destination]['neighbours'].append({'destination': source, 'strength': strength})
            self.graph[destination]['total_strength'] += strength
    
    
    def dfs(self, node: int, visited: set, threshold: float):
        # Mark node as visited
        visited.add(node)
        
        # Visit all neighbours of node
        for edge in self.graph[node]['neighbours']:
            if edge['strength'] / self.graph[node]['total_strength'] > threshold and edge['destination'] not in visited:
                self.dfs(edge['destination'], visited, threshold)
                
    
    def bfs(self, node: int, visited: set, threshold: float):
        # Initialise variables
        queue = [node]
        
        while queue:
            # Get next node from queue
            node = queue.pop(0)
            visited.add(node)
            
            # Visit all neighbours of node
            for edge in self.graph[node]['neighbours']:
                if edge['strength'] / self.graph[node]['total_strength'] > threshold and edge['destination'] not in visited:
                    queue.append(edge['destination'])

    
    def get_number_of_clusters(self, threshold: float = 0) -> int:
        # Initialise variables
        visited = set()
        clusters = 0
        
        # Visit all nodes in graph
        for node in tqdm.tqdm(self.graph, desc='Calculating number of clusters'):
            if node not in visited:
                self.bfs(node, visited, threshold)
                clusters += 1
                
        return clusters
    

    def get_density(self) -> float:
        # Initialise variables
        total_edges = 0
        total_nodes = len(self.graph)
        
        # Count total number of edges
        for node in tqdm.tqdm(self.graph, desc='Calculating density'):
            total_edges += len([1 for neighbour in self.graph[node]['neighbours'] if neighbour['strength'] > 0])
        
        return total_edges / (total_nodes * (total_nodes - 1))
    
    
    def get_number_of_neighbours(self) -> pd.DataFrame:
        # Initialise variables
        neighbours = []
        
        # Count number of neighbours for each node
        for node in tqdm.tqdm(self.graph, desc='Calculating number of neighbours'):
            neighbours.append(len([1 for neighbour in self.graph[node]['neighbours'] if neighbour['strength'] > 0]))
        
        return pd.DataFrame(neighbours, columns=['number_of_neighbours']) 
    
    
    def relationship_decay(self, decay_rate: float = 0.5) -> None:
        for node in tqdm.tqdm(self.graph, desc='Decaying relationships'):
            for neighbour in self.graph[node]['neighbours']:
                neighbour['strength'] *= decay_rate
                
            self.graph[node]['total_strength'] *= decay_rate
    
    
    def simulate_iteration(self, random_prob: float = 0):
        
        for node in tqdm.tqdm(self.graph, desc='Simulating iteration'):
            neighbours = [neighbour['destination'] for neighbour in self.graph[node]['neighbours'] if neighbour['strength'] > 0]
            
            choosen_neighbour = None
            
            # Choose random neighbour with probability random_prob
            if self.graph[node]['total_strength'] < 0 or np.random.rand() < random_prob:
                choosen_neighbour = np.random.choice(self.all_authors)
                
                if choosen_neighbour == node:
                    continue
            
            # Choose neighbour based on strength
            else:
                probabilities = [neighbour['strength'] / self.graph[node]['total_strength'] for neighbour in self.graph[node]['neighbours'] if neighbour['strength'] > 0]
                choosen_neighbour = np.random.choice(neighbours, p=probabilities)
            
            # Update nodes' neighbours
            if choosen_neighbour not in neighbours:
                self.graph[node]['neighbours'].append({'destination': choosen_neighbour, 'strength': 1})
                self.graph[choosen_neighbour]['neighbours'].append({'destination': node, 'strength': 1})
            
            else:
                self.graph[node]['neighbours'][neighbours.index(choosen_neighbour)]['strength'] += 1
                
                nodes_location = [neighbour['destination'] for neighbour in self.graph[choosen_neighbour]['neighbours']].index(node)
                self.graph[choosen_neighbour]['neighbours'][nodes_location]['strength'] += 1
            
            self.graph[node]['total_strength'] += 1
            self.graph[choosen_neighbour]['total_strength'] += 1