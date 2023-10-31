#!/bin/sh
#
#BSUB -J hawc2[1-20]%20
#BSUB -q hpc 
#BSUB -n 1
#BSUB -W 01:00
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -u s223597@dtu.dk
##BSUB -B
##BSUB -N
#BSUB -o lsf_log/hawc2_output_%J_%I.out
#BSUB -e lsf_log/hawc2_error_%J_%I.err 


date
START_TIME=`date +%s`
echo whoami
whoami
echo hostname -I
hostname -I

echo "running task $LSB_JOBINDEX/20..."


# Read the list of htc files to run and store them in a bash array named FILE_LIST
readarray -t FILE_LIST < to_run.txt

# Get the htc filename for this job
FILE_NAME=${FILE_LIST[$LSB_JOBINDEX - 1]}

# Run HAWC2
echo "running HAWC2 on $FILE_NAME..."
module load hawc2
HAWC2MB.exe "$FILE_NAME"


END_TIME=`date +%s`
echo done
echo "runtime: $(($END_TIME-$START_TIME)) seconds"