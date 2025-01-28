import os
import requests
import json
from langchain.prompts import PromptTemplate
from langchain_community.llms import Ollama

# Conexión al modelo Phi usando Ollama
llm = Ollama(
    model="phi",
    base_url="http://localhost:11434"  # Ajusta al puerto correcto si cambiaste el puerto
)

# Plantilla de prompt para que el modelo extraiga información
scraping_prompt = PromptTemplate(
    input_variables=["html_content"],
    template="""
    Analiza el siguiente contenido HTML y extrae los datos solicitados en el siguiente formato JSON.

    Información a extraer:
    - Títulos de publicaciones (etiquetas <h1>, <h2>, <h3>).
    - Detalles de tablas (<table class="itemDisplayTable">).
    - URLs de archivos PDF disponibles.

    Devuelve únicamente un JSON estructurado, como este ejemplo:
    [
        {{
            "Nombre": "string",
            "URL del perfil": "string",
            "Perfil": {{
                "Email": "string"
            }},
            "Publicaciones": [
                {{
                    "Título": "string",
                    "Autores/as": "string",
                    "Fecha de publicación": "string",
                    "Resumen": "string"
                }}
            ],
            "Proyectos": [],
            "Tesis": [],
            "Patentes": []
        }}
    ]

    Si no puedes extraer información relevante, devuelve un JSON vacío: [].

    Contenido HTML:
    {html_content}
    """
)

# Directorio donde se guardarán las páginas scrapeadas
SCRAPED_PAGES_DIR = "scraped_pages"
os.makedirs(SCRAPED_PAGES_DIR, exist_ok=True)

def save_page_content(url, page_number):
    """Guarda el contenido HTML de una página en un archivo."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al acceder a la página {url}: {e}")
        return None

    # Guardar el contenido HTML en un archivo
    filename = os.path.join(SCRAPED_PAGES_DIR, f"page_{page_number}.html")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(response.text)

    print(f"Página guardada: {filename}")
    return filename

def process_saved_pages():
    """Procesa los archivos HTML guardados con el modelo y guarda resultados JSON."""
    output_dir = "processed_pages"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(SCRAPED_PAGES_DIR):
        if filename.endswith(".html"):
            filepath = os.path.join(SCRAPED_PAGES_DIR, filename)
            with open(filepath, "r", encoding="utf-8") as file:
                html_content = file.read()[:5000]  # Limitar tamaño para evitar problemas

            # Generar el texto del prompt
            prompt_text = scraping_prompt.format(html_content=html_content)

            try:
                # Ejecutar el modelo con el prompt
                raw_result = llm.invoke(prompt_text)

                # Validar si la salida es un JSON
                if isinstance(raw_result, str):
                    try:
                        result = json.loads(raw_result)
                    except json.JSONDecodeError as e:
                        print(f"Error al decodificar el archivo {filename}: {e}")
                        print("Salida cruda del modelo:", raw_result)
                        result = []
                else:
                    print(f"Formato inesperado en {filename}: {raw_result}")
                    result = []

                # Guardar el resultado en un archivo JSON
                output_filename = os.path.join(output_dir, f"{filename.replace('.html', '.json')}")
                with open(output_filename, "w", encoding="utf-8") as output_file:
                    json.dump(result, output_file, ensure_ascii=False, indent=4)
                print(f"Resultados guardados: {output_filename}")

            except Exception as e:
                print(f"Error al procesar {filename}: {e}")

# Función principal
def main():
    # URL de ejemplo y número de páginas a scrapeear
    base_url = "https://accedacris.ulpgc.es/simple-search?query=&location=researcherprofiles&start="
    num_pages = 5
    limit_per_page = 50

    # Guardar cada página en un archivo
    for i in range(num_pages):
        page_url = f"{base_url}{i * limit_per_page}"
        save_page_content(page_url, i + 1)

    # Procesar los archivos guardados
    process_saved_pages()

if __name__ == "__main__":
    main()
