from dataclasses import dataclass

@dataclass

class DataIngestionArtifact: # significance - holds file paths for training and testing datasets
    training_file_path: str
    test_file_path: str