"""
DataProcessor Module
A data processing utility for ingesting, transforming, analyzing, and exporting numerical datasets.
"""

import math
import csv
from typing import List, Dict, Union, Optional


class DataProcessor:
    """
    DataProcessor manages numerical data collection, performs basic statistical
    analysis, supports data filtering/transformation, and enables CSV I/O.
    """

    def __init__(self, initial_data: Optional[List[Union[int, float]]] = None):
        """Initialize the processor with optional initial numerical data."""
        self.data_list: List[Union[int, float]] = []
        if initial_data:
            for item in initial_data:
                self.add_data(item)

    def add_data(self, item: Union[int, float]) -> None:
        """Adds a single numeric item to the data list."""
        if item is None:
            raise ValueError("Item cannot be None.")
        if not isinstance(item, (int, float)):
            raise TypeError(f"Expected int or float, got {type(item).__name__}")
        self.data_list.append(float(item))

    def batch_add(self, items: List[Union[int, float]]) -> int:
        """Adds multiple numeric items to the dataset. Returns count of successfully added items."""
        count = 0
        for item in items:
            try:
                self.add_data(item)
                count += 1
            except (ValueError, TypeError):
                continue
        return count

    def get_data(self) -> List[float]:
        """Returns a copy of the current data list."""
        return list(self.data_list)

    def clear(self) -> None:
        """Clears all data from the processor."""
        self.data_list.clear()

    def calculate_mean(self) -> float:
        """Calculates arithmetic mean of stored data."""
        if not self.data_list:
            raise ValueError("Cannot calculate mean of empty dataset.")
        return sum(self.data_list) / len(self.data_list)

    def calculate_median(self) -> float:
        """Calculates median of stored data."""
        if not self.data_list:
            raise ValueError("Cannot calculate median of empty dataset.")
        sorted_data = sorted(self.data_list)
        n = len(sorted_data)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_data[mid - 1] + sorted_data[mid]) / 2.0
        return float(sorted_data[mid])

    def calculate_variance(self) -> float:
        """Calculates sample variance of stored data."""
        if len(self.data_list) < 2:
            raise ValueError("Variance requires at least two data points.")
        mean = self.calculate_mean()
        return sum((x - mean) ** 2 for x in self.data_list) / (len(self.data_list) - 1)

    def calculate_std_dev(self) -> float:
        """Calculates sample standard deviation of stored data."""
        return math.sqrt(self.calculate_variance())

    def get_summary_statistics(self) -> Dict[str, float]:
        """Returns a dictionary containing summary statistics for the dataset."""
        if not self.data_list:
            raise ValueError("Cannot generate summary for empty dataset.")
        return {
            "count": len(self.data_list),
            "min": min(self.data_list),
            "max": max(self.data_list),
            "mean": self.calculate_mean(),
            "median": self.calculate_median(),
            "std_dev": self.calculate_std_dev() if len(self.data_list) > 1 else 0.0
        }

    def filter_data(self, min_val: Optional[float] = None, max_val: Optional[float] = None) -> List[float]:
        """Returns filtered list of data points within inclusive range [min_val, max_val]."""
        result = self.data_list
        if min_val is not None:
            result = [x for x in result if x >= min_val]
        if max_val is not None:
            result = [x for x in result if x <= max_val]
        return result

    def transform_data(self, factor: float = 1.0, offset: float = 0.0) -> List[float]:
        """Applies linear transformation (x * factor + offset) to all elements."""
        return [x * factor + offset for x in self.data_list]

    def export_to_csv(self, filepath: str) -> None:
        """Exports dataset to a single-column CSV file."""
        with open(filepath, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["value"])
            for val in self.data_list:
                writer.writerow([val])

    def load_from_csv(self, filepath: str) -> int:
        """Loads numerical values from a CSV file column named 'value' or first column."""
        added = 0
        with open(filepath, mode='r') as file:
            reader = csv.reader(file)
            header = next(reader, None)
            for row in reader:
                if row:
                    try:
                        self.add_data(float(row[0]))
                        added += 1
                    except (ValueError, TypeError):
                        continue
        return added


if __name__ == "__main__":
    # Example workflow demonstration
    processor = DataProcessor([10, 20, 30, 40, 50])
    processor.batch_add([60.5, 70.2, "invalid", 85.0])
    
    print("Dataset:", processor.get_data())
    print("Summary Stats:", processor.get_summary_statistics())
    print("Filtered (>= 30):", processor.filter_data(min_val=30))
    print("Transformed (x2 + 5):", processor.transform_data(factor=2.0, offset=5.0))
