import os
import pandas as pd

from graph import Graph

class Experiment():
    def __init__(
        self,
        graph: Graph,
        experiment_id: int,
        number_of_iterations: int,
        decay_rate: float,
        random_coauthorship: float,
        lower_threshold: float,
        upper_threshold: float
        ) -> None:
        
        self.graph = graph
        self.experiment_id = experiment_id
        
        self.number_of_iterations = number_of_iterations
        self.decay_rate = decay_rate
        self.random_coauthorship = random_coauthorship
        
        # Generate output folder
        self.output_folder = f'output/experiment_{self.experiment_id}'
        
        os.makedirs('output', exist_ok=True)
        os.makedirs(self.output_folder, exist_ok=True)
        
        # Save parameters to CSV
        parameters_df = pd.DataFrame({
            'Number of Iterations': [number_of_iterations],
            'Decay Rate': [decay_rate],
            'Random Coauthorship': [random_coauthorship],
            
            'Lower Threshold': [lower_threshold],
            'Upper Threshold': [upper_threshold]
        })
        
        parameters_df.to_csv(f'{self.output_folder}/parameters.csv', index=False)
        
    def perform_experiment(self) -> None:
        results01 = []
        results00 = []
        density = []

        # Save initial state
        results01.append(self.graph.get_number_of_clusters(0.1))
        results00.append(self.graph.get_number_of_clusters(0.0))
        density.append(self.graph.get_density())

        for i in range(self.number_of_iterations):
            print(f'\nStarting iteration {i+1}...')
            
            # Simulate iteration
            self.graph.simulate_iteration(self.random_coauthorship)
            self.graph.relationship_decay(self.decay_rate)

            # Save results
            results01.append(self.graph.get_number_of_clusters(0.1))
            results00.append(self.graph.get_number_of_clusters(0.0))
            density.append(self.graph.get_density())
            
        
        # Save results to CSV
        results_df = pd.DataFrame({
            'Iteration': list(range(self.number_of_iterations + 1)),
            '10% Threshold Clusters': results01,
            '0% Threshold Clusters': results00,
            'Graph Density': density
        })
        
        results_df.to_csv(f'{self.output_folder}/results.csv', index=False)