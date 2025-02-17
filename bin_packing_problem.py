import os
import math
import random
from qubots.base_problem import BaseProblem

class BinPackingProblem(BaseProblem):
    """
    Bin Packing Problem:
    
    Given a set of items with known weights and bins with uniform capacity,
    assign each item to a bin such that the total weight in any bin does not exceed the bin capacity.
    
    The objective is to minimize the number of bins used.
    
    Candidate solution representation:
      A list of integers of length equal to the number of items.
      Each integer represents the bin (0-indexed) to which the corresponding item is assigned.
    """
    
    def __init__(self, instance_file=None, nb_items=None, bin_capacity=None, weights_data=None):
        if instance_file is not None:
            self._load_instance_from_file(instance_file)
        else:
            if nb_items is None or bin_capacity is None or weights_data is None:
                raise ValueError("Either 'instance_file' or nb_items, bin_capacity, and weights_data must be provided.")
            self.nb_items = nb_items
            self.bin_capacity = bin_capacity
            self.weights_data = weights_data
            self._compute_bins()
    
    def _compute_bins(self):
        total_weight = sum(self.weights_data)
        self.nb_min_bins = int(math.ceil(total_weight / float(self.bin_capacity)))
        self.nb_max_bins = min(self.nb_items, 2 * self.nb_min_bins)
    
    def _load_instance_from_file(self, filename):
        # Resolve relative path with respect to this module's directory.
        if not os.path.isabs(filename):
            base_dir = os.path.dirname(os.path.abspath(__file__))
            filename = os.path.join(base_dir, filename)
        with open(filename, 'r') as f:
            tokens = f.read().split()
        it = iter(tokens)
        self.nb_items = int(next(it))
        self.bin_capacity = int(next(it))
        self.weights_data = [int(next(it)) for _ in range(self.nb_items)]
        self._compute_bins()
    
    def evaluate_solution(self, solution) -> float:
        """
        Evaluate a candidate solution.
        
        The candidate solution should be a list of integers (length = nb_items) where
        each integer is the bin index (0-indexed) to which the item is assigned.
        
        Feasibility:
          - For each bin, the total weight of items assigned to that bin must not exceed bin_capacity.
        
        Objective:
          - Minimize the number of bins used (i.e. the number of unique bin indices in the solution).
        
        Returns the number of bins used if feasible; otherwise, returns a high penalty.
        """
        PENALTY = 1e9
        if not isinstance(solution, (list, tuple)) or len(solution) != self.nb_items:
            return PENALTY
        # Check that each bin assignment is valid.
        for b in solution:
            if not isinstance(b, int) or b < 0 or b >= self.nb_max_bins:
                return PENALTY
        
        # Compute total weight per bin.
        bin_weights = {}
        for i, b in enumerate(solution):
            bin_weights[b] = bin_weights.get(b, 0) + self.weights_data[i]
        # Verify weight constraint for each bin.
        for weight in bin_weights.values():
            if weight > self.bin_capacity:
                return PENALTY
        
        # Objective: number of used bins.
        used_bins = len(bin_weights)
        return used_bins
    
    def random_solution(self):
        """
        Generate a random candidate solution.
        
        Each item is randomly assigned a bin index between 0 and (nb_max_bins - 1).
        """
        return [random.randint(0, self.nb_max_bins - 1) for _ in range(self.nb_items)]
