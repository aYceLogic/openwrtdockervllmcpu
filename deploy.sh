IP=192.168.1.1
OPENWRTBASEDIR='/mnt/sda'

scp -O "$(dirname "$0")/vllmsample.py" "$(dirname "$0")/env.sh" root@${IP}:${OPENWRTBASEDIR}/models/;
ssh -tt root@${IP} "docker run --rm -it --shm-size=64m --network host -v ${OPENWRTBASEDIR}/models:/workspace/models -v ${OPENWRTBASEDIR}/root_cache:/root/.cache --name vllm -p 8000:8000 --entrypoint bash openeuler/vllm-cpu -c 'source /workspace/models/env.sh'"


