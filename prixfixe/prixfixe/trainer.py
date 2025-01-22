import json
from pathlib import Path
import pandas as pd
import numpy as np
import torch
import tqdm
from scipy.stats import pearsonr, spearmanr

from .prix_fixe_net import PrixFixeNet
from .dataprocessor import DataProcessor


from typing import Any
from abc import ABCMeta, abstractmethod

# default metrics to compute
DEFAULT_METRICS = {
    "MSE": lambda y, y_pred:  (np.square(y_pred - y)).mean(),
    "pearsonr": lambda y, y_pred: pearsonr(y, y_pred)[0],
    "spearmanr": lambda y, y_pred: spearmanr(y, y_pred)[0]
}

class Trainer(metaclass=ABCMeta):
    """
    Performs training of the model
    Responsible for training procedure introduced by a team 
    (optimizers, schedulers, etc.)
    """   
    
    @abstractmethod
    def __init__(
        self,
        model: PrixFixeNet, 
        dataprocessor: DataProcessor,
        model_dir: str | Path,
        num_epochs: int,
        device: torch.device = torch.device("cpu"),
        **kwargs):
        """
        Parameters
        ----------
        model
            PrixFixeNet model instance
        dataprocessor
            onject containing all information about train and validation datasets
        model_dir
            path to log intermediate results and save trained model 
        num_epochs
            Number of epochs to perform training
        device
            device to use during training
        """
        super().__setattr__("__CAN_ASSIGN__", True)
        self.model = model
        self.dataprocessor = dataprocessor
        self.model_dir = Path(model_dir)
        if self.model_dir.exists():
            raise Exception(f"Model dir '{model_dir}' already exists")
        self.model_dir.mkdir(parents=True)
        self.num_epochs = num_epochs
        self.device = device
        self.train_dataloader = self.dataprocessor.prepare_train_dataloader()
        self.train_fixed_dataloader = self.dataprocessor.prepare_train_fixed_dataloader()
        self.valid_dataloader = self.dataprocessor.prepare_valid_dataloader()
        self.test_dataloader = self.dataprocessor.prepare_test_dataloader()
        self.optimizer = None # should be overwritten by subclass
        self.scheduler = None # may be overwritten by subclass
        self.best_val_pearson = - np.inf        
             
    @abstractmethod
    def train_step(self, batch: dict[str, Any]) -> float:
        """
        Performs one step of the training procedure
        """
        ...
    
    @abstractmethod
    def on_epoch_end(self) -> list[float]:
        """
        Trainer actions on each epoch end
        For e.g - calling scheduler
        """
        ...
        
    def train_epoch(self) -> list[float]:
        if not self.model.training:
            self.model = self.model.train()
        lst = []
        for batch in tqdm.tqdm(self.train_dataloader,
                               total=self.dataprocessor.train_epoch_size(),
                               desc="Train epoch",
                               leave=False):
        # for batch in self.train_dataloader:
            loss = self.train_step(batch)
            lst.append(loss)
        self.on_epoch_end()
        return lst
        
        
    def fit(self):
        """
        Fit model using the train dataset from dataprocessor
        """
        
        self.dataprocessor.train.to_csv(self.model_dir / f"train.csv", index=False)
        self.dataprocessor.valid.to_csv(self.model_dir / f"val.csv", index=False)
        self.dataprocessor.test.to_csv(self.model_dir / f"test.csv", index=False)


        for epoch in tqdm.tqdm(range(1, self.num_epochs+1)):
            self.train_epoch()
            
            self.pred_train(epoch)
            metrics_val=self.validate(epoch)
            metrics_test=self.test(epoch)
 
            self._dump_metrics(metrics_val, epoch, 'val')
            self._dump_metrics(metrics_test, epoch, 'test')
            self._dump_best(metrics_val, 'val')
            # self._dump_model_end_of_epoch(epoch)
    
    def pred_train(self, epoch):
        if self.train_fixed_dataloader is None:
            raise Exception("No train dataset was provided")

        if self.model.training:
            self.model = self.model.eval()
        
        with torch.inference_mode():
            y_pred_vector, y_vector = [], []
            # for batch in tqdm.tqdm(self.valid_dataloader,
            #                        desc="Validation", 
            #                        leave=False):
            for batch in self.train_fixed_dataloader:
                y_pred, y = self._evaluate(batch)
                y_pred, y = y_pred.cpu().numpy().reshape(-1), y.cpu().numpy()
                y_pred_vector.extend(y_pred)
                y_vector.extend(y)

        score_path = self.model_dir / f"train.csv"
        df = pd.read_csv(score_path)
        # Append a new column with predictions for the current epoch
        column_name = f'Epoch_{epoch}'  # Epochs are zero-indexed
        df[column_name] = y_pred_vector
        df.to_csv(score_path, index=False)

        return
    
    def validate(self, epoch):
        if self.valid_dataloader is None:
            raise Exception("No valid dataset was provided")

        if self.model.training:
            self.model = self.model.eval()
        
        with torch.inference_mode():
            y_pred_vector, y_vector, y_pred_vector_metric = [], [], []
            # for batch in tqdm.tqdm(self.valid_dataloader,
            #                        desc="Validation", 
            #                        leave=False):
            for batch in self.valid_dataloader:
                y_pred, y = self._evaluate(batch)
                y_pred, y = y_pred.cpu().numpy().reshape(-1), y.cpu().numpy()
                y_pred_vector.extend(y_pred)
                y_pred_vector_metric.append(y_pred)
                y_vector.append(y)
        score_path = self.model_dir / f"val.csv"
        df = pd.read_csv(score_path)
        # Append a new column with predictions for the current epoch
        column_name = f'Epoch_{epoch}'  # Epochs are zero-indexed
        df[column_name] = y_pred_vector
        df.to_csv(score_path, index=False)
        metrics = self._calc_metrics(y_pred_vector_metric, y_vector)
        return metrics

    def test(self, epoch):
        if self.test_dataloader is None:
            raise Exception("No test dataset was provided")

        if self.model.training:
            self.model = self.model.eval()
        
        with torch.inference_mode():
            y_pred_vector, y_vector, y_pred_vector_metric = [], [], []
            # for batch in tqdm.tqdm(self.valid_dataloader, 
            #                        desc="Validation", 
            #                        leave=False):
            for batch in self.test_dataloader:
                y_pred, y = self._evaluate(batch)
                y_pred, y = y_pred.cpu().numpy().reshape(-1), y.cpu().numpy()
                y_pred_vector.extend(y_pred)
                y_pred_vector_metric.append(y_pred)
                y_vector.append(y)
        score_path = self.model_dir / f"test.csv"
        df = pd.read_csv(score_path)
        # Append a new column with predictions for the current epoch
        column_name = f'Epoch_{epoch}'  # Epochs are zero-indexed
        df[column_name] = y_pred_vector
        df.to_csv(score_path, index=False)
        metrics = self._calc_metrics(y_pred_vector_metric, y_vector)
        return metrics

    def _calc_metrics(self, y_pred, y) -> dict[str, float]:
        y = np.concatenate(y)
        y_pred = np.concatenate(y_pred)
        
        return {name: float(fn(y, y_pred)) for name, fn in DEFAULT_METRICS.items()}
      
    def _dump_metrics(self, metrics, epoch, tag):
        score_path = self.model_dir / f"{tag}_metrics.json"

        # Check if the file exists. If it does, append a comma and newline
        if score_path.exists():
            with open(score_path, "a") as outp:
                outp.write(",\n")

        # Append the new metrics
        with open(score_path, "a") as outp:
            json.dump({f"epoch_{epoch}": metrics}, outp)

            

    def _evaluate(self, batch: dict[str, Any]):
        with torch.no_grad():
            X = batch["x"]
            y = batch["y"]
            X = X.to(self.device)
            y = y.float().to(self.device)
            y_pred = self.model.forward(X)
        return y_pred.cpu(), y.cpu()

    def _dump_best(self, metrics, tag):
        curr_pearson = metrics["pearsonr"]
        if tag == 'val':
            if curr_pearson > self.best_val_pearson:
                self.best_val_pearson = curr_pearson
                self._dump_model(tag)

    def _dump_model(self, tag):
        model_path = self.model_dir / f"model_{tag}.pth"
        torch.save(self.model.state_dict(), model_path)
        
        if self.optimizer is not None:
            optimizer_path = self.model_dir / f"optimizer_{tag}.pth"
            torch.save(self.optimizer.state_dict(), optimizer_path)
        
        if self.scheduler is not None:
            scheduler_path = self.model_dir / f"scheduler_{tag}.pth"
            torch.save(self.scheduler.state_dict(), scheduler_path)

    def _dump_model_end_of_epoch(self, epoch):
        model_path = self.model_dir / f"model_{epoch}.pth"
        torch.save(self.model.state_dict(), model_path)

    def __setattr__(self, name: str, value: Any) -> None:
        if not hasattr(self, "__CAN_ASSIGN__"):
            raise Exception("Cannot assign parameters to Trainer subclass object before Trainer.__init__() call")
        super().__setattr__(name, value)
        
