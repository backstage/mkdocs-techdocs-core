#!/bin/sh

PWD=$(pwd)
ASSUMED_TECHDOCS_CONTAINER_DIR="$(dirname "$PWD")/techdocs-container"

echo "Enter the path to your local techdocs-image repository ($ASSUMED_TECHDOCS_CONTAINER_DIR): "

read TECHDOCS_CONTAINER_DIR

if [ ! "$TECHDOCS_CONTAINER_DIR" ]; then
   echo "Using default $ASSUMED_TECHDOCS_CONTAINER_DIR"
   TECHDOCS_CONTAINER_DIR=$ASSUMED_TECHDOCS_CONTAINER_DIR
fi

# Check the dir for the expected catalog file
EXPECTED_CATALOG_CONTENT=$(grep -E "name: techdocs-container$" "${TECHDOCS_CONTAINER_DIR}/catalog-info.yaml")

if [ ! "$EXPECTED_CATALOG_CONTENT" ]; then
    echo "[ERROR] did not find expected content in ${TECHDOCS_CONTAINER_DIR}/catalog-info.yaml, please make sure the dir is correct and that the repo is cloned" 
    exit 1
fi

# From now on we assume the image repo is next to this one
DOCKERFILE="$TECHDOCS_CONTAINER_DIR/Dockerfile"

# Remove and copy this repo to the techdocs container local repo
rm -rf "${TECHDOCS_CONTAINER_DIR}/local-mkdocs-techdocs-core"
cp -r $PWD "${TECHDOCS_CONTAINER_DIR}/local-mkdocs-techdocs-core"

COPY_COMMAND="COPY .\/local-mkdocs-techdocs-core \/local-mkdocs-techdocs-core \n"

# Remove any previously added COPY instruction
sed -i '' '/COPY .\/local-mkdocs-techdocs-core/d' $DOCKERFILE

# Add the COPY instruction
sed -i '' "s/^\(RUN pip install.*\)/${COPY_COMMAND}\1/" $DOCKERFILE

# Install the local version instead of the public release
sed -E -i '' "s/pip install mkdocs-techdocs-core==[0-9]+\.[0-9]+\.[0-9]+/pip install -e \/local-mkdocs-techdocs-core/" $DOCKERFILE

# Build the image
docker build -f $DOCKERFILE -t mkdocs:local-dev . || exit 1

echo "================================================================================\n"
echo "The docker image is built, now use it in your config: \n"

echo 'techdocs:'
echo '  generator:'
echo '    runIn: "docker"'
echo '    dockerImage: mkdocs:local-dev'
echo '    pullImage: false'

