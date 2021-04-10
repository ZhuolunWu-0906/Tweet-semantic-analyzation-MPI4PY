#!/bin/bash
#SBATCH --time=0-12:00:00
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=4
module purge
module load foss/2019b
module load python/3.7.4
time srun -n 8 python3 tweetScores.py bigTwitter.json AFINN.txt melbGrid.json