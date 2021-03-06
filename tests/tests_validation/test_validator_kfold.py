import unittest
import numpy as np
import pandas as pd
from supervised.validation.validator_kfold import KFoldValidator
from supervised.validation.validator_base import BaseValidatorException

import os
import shutil


class KFoldValidatorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("SETUP CLASS")
        cls._results_path = "/tmp/k_fold_test"
        os.mkdir(cls._results_path)

    @classmethod
    def tearDownClass(cls):
        print("TEAR DOWN CLASS")

        shutil.rmtree(cls._results_path)

    def test_create(self):

        data = {
            "train": {
                "X": pd.DataFrame(np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), columns=["a", "b"]),
                "y": pd.DataFrame(np.array([0, 0, 1, 1]), columns=["target"]),
            }
        }

        X_train_path = os.path.join(self._results_path, "X_train.parquet")
        y_train_path = os.path.join(self._results_path, "y_train.parquet")
        
        data["train"]["X"].to_parquet(X_train_path, index=False)
        data["train"]["y"].to_parquet(y_train_path, index=False)

        params = {
            "shuffle": False,
            "stratify": False,
            "k_folds": 2,
            "results_path": self._results_path,
            "X_train_path": X_train_path,
            "y_train_path": y_train_path,
        }
        vl = KFoldValidator(params)

        self.assertEqual(params["k_folds"], vl.get_n_splits())
        #for train, validation in vl.split():
        for k_fold in range(vl.get_n_splits()):
            train, validation = vl.get_split(k_fold)

            X_train, y_train = train.get("X"), train.get("y")
            X_validation, y_validation = validation.get("X"), validation.get("y")

            self.assertEqual(X_train.shape[0], 2)
            self.assertEqual(y_train.shape[0], 2)
            self.assertEqual(X_validation.shape[0], 2)
            self.assertEqual(y_validation.shape[0], 2)

    def test_missing_target_values(self):
        
        data = {
            "train": {
                "X": pd.DataFrame(np.array([[1, 0], [2, 1], [3, 0], [4, 1], [5, 1], [6, 1]]), columns=["a", "b"]),
                "y": pd.DataFrame(np.array(["a", "b", "a", "b", np.nan, np.nan]), columns=["target"]),
            }
        }

        X_train_path = os.path.join(self._results_path, "X_train.parquet")
        y_train_path = os.path.join(self._results_path, "y_train.parquet")
        
        data["train"]["X"].to_parquet(X_train_path, index=False)
        data["train"]["y"].to_parquet(y_train_path, index=False)

        params = {
            "shuffle": True, "stratify": True, "k_folds": 2,
            "results_path": self._results_path,
            "X_train_path": X_train_path,
            "y_train_path": y_train_path,
        }
        vl = KFoldValidator(params)

        self.assertEqual(params["k_folds"], vl.get_n_splits())
        
        for k_fold in range(vl.get_n_splits()):
            train, validation = vl.get_split(k_fold)
            X_train, y_train = train.get("X"), train.get("y")
            X_validation, y_validation = validation.get("X"), validation.get("y")

            self.assertEqual(X_train.shape[0], 2)
            self.assertEqual(y_train.shape[0], 2)
            self.assertEqual(X_validation.shape[0], 2)
            self.assertEqual(y_validation.shape[0], 2)

    def test_create_with_target_as_labels(self):

        data = {
            "train": {
                "X": pd.DataFrame(np.array([[0, 0], [0, 1], [1, 0], [1, 1]]), columns=["a", "b"]),
                "y": pd.DataFrame(np.array(["a", "b", "a", "b"]), columns=["target"]),
            }
        }

        X_train_path = os.path.join(self._results_path, "X_train.parquet")
        y_train_path = os.path.join(self._results_path, "y_train.parquet")
        
        data["train"]["X"].to_parquet(X_train_path, index=False)
        data["train"]["y"].to_parquet(y_train_path, index=False)

        params = {
            "shuffle": True, "stratify": True, "k_folds": 2,
            "results_path": self._results_path,
            "X_train_path": X_train_path,
            "y_train_path": y_train_path,
        }
        vl = KFoldValidator(params)

        self.assertEqual(params["k_folds"], vl.get_n_splits())
        
        for k_fold in range(vl.get_n_splits()):
            train, validation = vl.get_split(k_fold)
            X_train, y_train = train.get("X"), train.get("y")
            X_validation, y_validation = validation.get("X"), validation.get("y")



            self.assertEqual(X_train.shape[0], 2)
            self.assertEqual(y_train.shape[0], 2)
            self.assertEqual(X_validation.shape[0], 2)
            self.assertEqual(y_validation.shape[0], 2)


if __name__ == "__main__":
    unittest.main()
