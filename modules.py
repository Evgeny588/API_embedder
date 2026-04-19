import os
import gc
import sys
from datetime import datetime

from fastembed import TextEmbedding


def init_model(model: str | None = None):
    """
    Инициализация модели эмбеддингов.
    """

    model_name = model or os.getenv("MODEL")

    try:
        embedding_model = TextEmbedding(model_name=model_name, cache_dir="cache_models")

        return embedding_model
    except Exception as e:
        print(f"Ошибка при инициализации модели {model_name}: {e}")
        raise e


def clear_memory():
    """RAM cleaner для CPU режима"""

    gc.collect()

    if sys.platform.startswith("linux"):
        try:
            import ctypes

            libc = ctypes.CDLL("libc.so.6")
            libc.malloc_trim(0)
        except Exception:
            pass


def write_embedding(embedding) -> str:
    """
    Сохраняет эмбеддинг в текстовый файл с именем по текущей дате и времени.
    """
    output_dir = "outputs"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(embedding.tolist()))

    return filepath
