#!/bin/bash

TEST_DIR=$(cd $(dirname "${BASH_SOURCE[0]}") && pwd)
cd ${TEST_DIR}

IMAGE_NAME=$1
CURRENT_VERSION=$2

echo "Running e2e test: ${IMAGE_NAME}:${CURRENT_VERSION}"

OUTPUT_DIR=/tmp/single_species_$(uuidgen)

docker run --rm -v $(pwd):/data -v /tmp:/tmp ${IMAGE_NAME}:${CURRENT_VERSION} query_single_species -c /data/config.txt -o ${OUTPUT_DIR}

echo -n "Checking results ... "

diff "${OUTPUT_DIR}/EvoPPI_Results.csv" "Expected_EvoPPI_Results.csv"
if [ $? -ne 0 ]; then
    echo "FAILED"
    echo -e "\tTest error: ${OUTPUT_DIR}/EvoPPI_Results.csv is different to Expected_EvoPPI_Results.csv"
    exit 1
fi

echo "OK"