#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --gres=gpu:1
#SBATCH --time=10:00:00
#SBATCH --mem=32GB
#SBATCH --job-name=latincy-test
#SBATCH --mail-type=END
#SBATCH --mail-user=pjb311@nyu.edu
#SBATCH --output=%j.out
#SBATCH --error=%j.err

module purge;

# conda
module load anaconda3/2024.02;
source /share/apps/anaconda3/2024.02/etc/profile.d/conda.sh;
conda activate /scratch/pjb311/spacy-dev
export PATH=/scratch/pjb311/spacy-dev/bin:$PATH;

# cuda
module load cuda/11.6.2

weasel run all
