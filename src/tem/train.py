"""
TEM Training Pipeline
=====================

Trains the Tolman-Eichenbaum Machine on the Hier-SPCNet.
Minimizes sensory prediction error (reconstruction loss) to learn
structural representations (grid cells) of the legal space.

Usage:
    python -m src.tem.train --graph_dir data/processed/graph --epochs 100
"""

import argparse
import torch
import torch.optim as optim
import torch.nn as nn
import torch.nn.functional as F
from pathlib import Path
from tqdm import tqdm

from src.tem.legal_graph_builder import LegalGraphBuilder
from src.tem.model import TolmanEichenbaumMachine
from src.tem.action_space import get_action_dim

def train(
    graph_dir: Path,
    output_dir: Path,
    embedding_dim: int = 128, # Reduced for Pilot
    hidden_dim: int = 256,
    batch_size: int = 16,
    seq_len: int = 10,
    epochs: int = 10,
    lr: float = 1e-3
):
    # 1. Setup Environment
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training on {device}")
    
    builder = LegalGraphBuilder(graph_dir)
    action_dim = get_action_dim()
    
    # 2. Initialize Embeddings (Mock or Real)
    # In production, load these from P0.3
    node_embeddings = builder.get_embedding_matrix(embedding_dim).to(device)
    node_embeddings.requires_grad = False # Fixed sensory input
    
    # 3. Initialize Model
    model = TolmanEichenbaumMachine(
        input_dim=embedding_dim,
        hidden_dim=hidden_dim,
        action_dim=action_dim
    ).to(device)
    
    optimizer = optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    
    # 4. Training Loop
    print("Starting training...")
    model.train()
    
    # Create data loader
    # 100 batches per epoch
    steps_per_epoch = 100 
    data_iter = builder.batch_generator(batch_size, seq_len)
    
    for epoch in range(epochs):
        total_loss = 0.0
        
        pbar = tqdm(range(steps_per_epoch), desc=f"Epoch {epoch+1}/{epochs}")
        for _ in pbar:
            # Get batch
            batch = next(data_iter)
            obs_indices = batch['observations'].to(device) # (B, Seq)
            actions = batch['actions'].to(device)          # (B, Seq-1)
            
            # Lookup embeddings
            # (B, Seq) -> (B, Seq, Emb_Dim)
            observations = F.embedding(obs_indices, node_embeddings)
            
            # Forward pass
            optimizer.zero_grad()
            output = model(observations, actions)
            
            # Calculate Loss
            # Compare predictions x_hat_{t} with actual x_{t}
            # Output predictions start from t=0 (reconstruction) to t=Seq-1
            predictions = output['predictions']
            
            # MSE between predicted embedding and actual embedding
            loss = criterion(predictions, observations)
            
            # Backward
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            
            total_loss += loss.item()
            pbar.set_postfix({'loss': loss.item()})
            
        avg_loss = total_loss / steps_per_epoch
        print(f"Epoch {epoch+1} Complete. Avg Loss: {avg_loss:.4f}")
        
        # Save Checkpoint
        if (epoch + 1) % 5 == 0:
            checkpoint_path = output_dir / f"tem_checkpoint_ep{epoch+1}.pt"
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': avg_loss,
            }, checkpoint_path)
            print(f"Saved checkpoint to {checkpoint_path}")

    # Save Final Model
    final_path = output_dir / "tem_final.pt"
    torch.save(model.state_dict(), final_path)
    print(f"Training complete. Model saved to {final_path}")

if __name__ == '__main__':
    import torch.nn.functional as F # For embedding lookup
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--graph_dir', type=Path, default=Path('data/processed/graph'))
    parser.add_argument('--output_dir', type=Path, default=Path('data/models/tem'))
    parser.add_argument('--epochs', type=int, default=10)
    
    args = parser.parse_args()
    
    args.output_dir.mkdir(parents=True, exist_ok=True)
    
    train(
        graph_dir=args.graph_dir,
        output_dir=args.output_dir,
        epochs=args.epochs
    )

