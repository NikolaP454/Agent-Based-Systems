import argparse
import pandas as pd

from graph import Graph
from experiment import Experiment

def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline parsing")
    
    parser.add_argument("--experiment_id",
                        type=int,
                        required=True,
                        help="Experiment ID")
    
    parser.add_argument("--lower_threshold",
                        type=int,
                        default=5,
                        help="Lower threshold for clustering")
    
    parser.add_argument("--upper_threshold",
                        type=int,
                        default=200,
                        help="Upper threshold for clustering")
    
    parser.add_argument("--number_of_iterations",
                        type=int,
                        default=20,
                        help="Number of iterations for simulation")
    
    parser.add_argument("--decay_rate",
                        type=float,
                        default=0.9,
                        help="Decay rate for relationships")
    
    parser.add_argument("--random_coauthorship",
                        type=float,
                        default=0.01,
                        help="Probability of random coauthorship")
    
    return parser


if __name__ == '__main__':
    # Get arguments
    args = get_args().parse_args()
    
    EXPERIMENT_ID = args.experiment_id
    LOWER_THRESHOLD = args.lower_threshold
    UPPER_THRESHOLD = args.upper_threshold
    
    NUMBER_OF_ITERATIONS = args.number_of_iterations
    DECAY_RATE = args.decay_rate
    RANDOM_COAUTHORSHIP = args.random_coauthorship
    
    # Load data
    df = pd.read_csv('data/coauth-MAG-gr3.txt', sep=' ', header=None, names=['author1', 'author2', 'power'])
    df = df[df['power'].between(LOWER_THRESHOLD, UPPER_THRESHOLD)]
    
    # Create graph
    graph = Graph(df)
    
    # Perform experiment
    experiment = Experiment(
        graph=graph,
        experiment_id=EXPERIMENT_ID,
        number_of_iterations=NUMBER_OF_ITERATIONS,
        decay_rate=DECAY_RATE,
        random_coauthorship=RANDOM_COAUTHORSHIP,
        lower_threshold=LOWER_THRESHOLD,
        upper_threshold=UPPER_THRESHOLD
    )
    
    experiment.perform_experiment()