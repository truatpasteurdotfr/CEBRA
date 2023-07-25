FROM  docker.io/continuumio/miniconda3

# Install conda packages.
RUN conda update -y conda \
    && conda update --all -y \
    && conda clean --all --yes

# pymol runtime
RUN	apt-get update && \
	DEBIAN_FRONTEND=noninteractive apt-get -y upgrade && \
	DEBIAN_FRONTEND=noninteractive apt-get -y install \
	wget \
	&& \
	DEBIAN_FRONTEND=noninteractive apt-get -y autoremove

RUN	wget https://raw.githubusercontent.com/truatpasteurdotfr/CEBRA/main/conda/cebra-cuda117.yml && \
	conda env create -f cebra-cuda117.yml

