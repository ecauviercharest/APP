#!/bin/bash
#SBATCH --account=def-fournier-ab
#SBATCH --nodes=1
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-task=20
#SBATCH --mem=6G 
#SBATCH --mail-user=jonathan.plourde@usherbrooke.ca
#SBATCH --mail-type=ALL
#SBATCH --time=1-00:00
#SBATCH --output=%x-%j.out
DATA=TWI_FD8
CONF=config_TWIFD8_v1
PPROJET=$HOME/projects/def-fournier-ab/jplou07
FILECONF=$PPROJET/conf/$CONF.yaml
BANDS=samples512_overlap70_min-annot10_1bands
module load python/3.6 cuda/9.2.148 gdal
virtualenv --no-download $SLURM_TMPDIR/ENV
source $SLURM_TMPDIR/ENV/bin/activate
pip install --no-index -r $HOME/projects/def-fournier-ab/jplou07/requirements.txt
pip install --no-index $HOME/Wheel/pynvml-8.0.4-py3-none-any.whl
pip install --no-index $HOME/Wheel/s3transfer-0.3.3-py2.py3-none-any.whl
pip install --no-index $HOME/Wheel/botocore-1.15.36-py2.py3-none-any.whl
cd $SLURM_TMPDIR
mkdir $SLURM_TMPDIR/data
cp $SCRATCH/Imagettes/$DATA.tar $SLURM_TMPDIR/data/$DATA.tar
cd data
tar xf $SLURM_TMPDIR/data/$DATA.tar
cd $SLURM_TMPDIR
python $PPROJET/script/python/setpath.py -i $FILECONF -o $FILECONF -d $DATA
python $PPROJET/GDL/train_segmentation.py $FILECONF
#copy and exit
NoTEST=0_$SLURM_JOB_ID
OUTDIR=$SCRATCH/results/$NoTEST
mkdir -p $OUTDIR
cp -r $SLURM_TMPDIR/data/$DATA/$BANDS/model/$CONF/. $OUTDIR
