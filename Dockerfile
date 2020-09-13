FROM mltooling/ml-workspace-gpu

ENV \
    MY_JUPYTERLAB_DIR="/jupyterlab" \
    MY_JUPYTERLAB_APP_DIR="$CONDA_DIR/share/jupyter/lab"

RUN \
    pip install --upgrade --pre jupyterlab_code_formatter jupyter_client jupyter_core jupyterlab_server nbclassic -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY jupyterlab/jupyterlab $MY_JUPYTERLAB_DIR/jupyterlab/
COPY jupyterlab/jupyter /etc/jupyter/

COPY jupyterlab/jupyterlab_app $MY_JUPYTERLAB_APP_DIR/
COPY jupyterlab/start-notebook.sh /usr/local/bin/

COPY sslh.conf /etc/supervisor/conf.d/

COPY docker-entrypoint.py /resources/

RUN \
    chmod a+rwx /usr/local/bin/start-notebook.sh && \
    chmod a+rwx /resources/docker-entrypoint.py && \
    # update labextensions
    cd $MY_JUPYTERLAB_DIR && \
    python -m jupyterlab.labextensions update --all && \
    python -m jupyterlab build

CMD [ "python", "/resources/docker-entrypoint.py" ]