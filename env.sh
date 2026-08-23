# 1. Dynamically calculate CPU affinity leaving 2 cores free (minimum of 1 core)
NUM_CORES=$(nproc)
USE_CORES=$(( NUM_CORES - 2 ))
if [ $USE_CORES -lt 1 ]; then
    USE_CORES=1
fi
LAST_CORE=$(( USE_CORES - 1 ))
export CORES_LIST=$(seq -s, 0 $LAST_CORE)
export VLLM_CPU_OMP_THREADS_BIND="$CORES_LIST"

# 2. Align internal OpenMP process threading parameters
export OMP_NUM_THREADS=$USE_CORES
export OMP_PLACES=cores
export OMP_PROC_BIND=spread

# 3. Suppress the large key-value cache registration space
export VLLM_CPU_KVCACHE_SPACE=0

# 4. Clear proxy or visibility filters that block downloading from the hub
export CUDA_VISIBLE_DEVICES=""

# 5. Execute your new script
python3 /workspace/models/vllmsample.py

