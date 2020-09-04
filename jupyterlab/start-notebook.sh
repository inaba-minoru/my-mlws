#!/bin/bash
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

set -e

cd "$MY_JUPYTERLAB_DIR"
python -m jupyterlab

# . /usr/local/bin/start.sh python -m jupyterlab "$NOTEBOOK_ARGS" "$@"

# if [[ ! -z "${JUPYTERHUB_API_TOKEN}" ]]; then
#   # launched by JupyterHub, use single-user entrypoint
#   exec /usr/local/bin/start-singleuser.sh "$@"
# elif [[ ! -z "${JUPYTER_ENABLE_LAB}" ]]; then
#   # custom: use NOTEBOOK_ARGS also for start without jupyterhub
#   # . /usr/local/bin/start.sh jupyter lab "$NOTEBOOK_ARGS" "$@"
#   cd "$JUPYTERLAB_PATH"
#   . /usr/local/bin/start.sh python -m jupyterlab "$NOTEBOOK_ARGS" "$@"
# else
#   # custom: use NOTEBOOK_ARGS also for start without jupyterhub
#   . /usr/local/bin/start.sh jupyter notebook "$NOTEBOOK_ARGS" "$@"
# fi