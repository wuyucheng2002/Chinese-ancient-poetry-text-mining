#BSUB -gpu "num=1:mode=exclusive_process"
#BSUB -J bertMT
#BSUB -n 1
#BSUB -o %J.out
#BSUB -e %J.err
#BSUB -q gpu

python train.py --gpu=1