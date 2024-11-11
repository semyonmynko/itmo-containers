# Используем образ mambaforge для совместимости с `arm64`
FROM condaforge/mambaforge:latest

# Устанавливаем зависимости через mamba, используя платформу linux-64
RUN conda config --env --set subdir linux-64 && \
    mamba install -c bioconda -c conda-forge snakemake blast prokka -y

# Устанавливаем рабочую директорию
WORKDIR /workspace

# Копируем весь проект в контейнер
COPY . /workspace

# Устанавливаем переменные окружения для Conda
ENV PATH /opt/conda/bin:$PATH

# Команда по умолчанию для запуска Snakemake
CMD ["snakemake", "--use-conda"]