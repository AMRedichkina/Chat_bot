ARG PYTHON_VERSION=3.9.6
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/home/appuser" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Установка правильных прав доступа к домашнему каталогу
RUN mkdir -p /home/appuser && chown -R appuser:appuser /home/appuser

# Установка зависимостей
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

# Переключение на непривилегированного пользователя
USER appuser

# Копирование всего содержимого проекта
COPY . /app

# Экспонирование порта
EXPOSE 8888

# Запуск Jupyter Notebook
CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root"]
