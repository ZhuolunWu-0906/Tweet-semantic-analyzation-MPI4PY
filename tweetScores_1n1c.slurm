#!/bin/bash
#SBATCH --time=0-12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
module purge
module load foss/2019b
module load python/3.7.4
time srun -n 1 python3 tweetScores.py bigTwitter.json AFINN.txt melbGrid.json