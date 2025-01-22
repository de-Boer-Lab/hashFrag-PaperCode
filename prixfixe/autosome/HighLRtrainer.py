import json
import torch
import tqdm

import numpy as np
import torch.nn as nn

from pathlib import Path
from typing import Any

from ..prixfixe import Trainer, PrixFixeNet, DataProcessor, DEFAULT_METRICS

class HighLRTrainer(Trainer):
    def __init__(
        self,
        model: PrixFixeNet, 
        dataprocessor: DataProcessor,
        model_dir: str | Path,
        num_epochs: int,
        lr: float = 0.001,
        device: torch.device = torch.device("cpu")):
        
        model = model.to(device)
        super().__init__(model=model,
                         dataprocessor=dataprocessor,
                         model_dir=model_dir,
                         num_epochs=num_epochs,
                         device=device)
        
        optimizer = torch.optim.Adam(model.parameters(), 
                                      lr = lr)
        self.optimizer=optimizer

    def train_step(self, batch):   
        _, loss = self.model.train_step(batch)
        loss.backward()
        self.optimizer.step()
        self.optimizer.zero_grad()
        return loss.item()
    
    def on_epoch_end(self):
        """
        Autosome sheduler is called during training steps, not on each epoch end
        Nothing to do at epoch end 
        """
        pass
    
    def deduce_max_lr(self):
        # TODO: for now no solution to search for maximum lr automatically, learning rate range test should be analysed manually
        # MAX_LR=0.005 seems OK for most models 
        return 0.005
