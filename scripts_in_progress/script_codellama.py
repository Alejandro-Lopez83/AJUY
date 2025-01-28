import os
import requests
import json
from langchain_ollama import OllamaLLM  # Asegúrate de usar langchain-ollama

# Configuración del modelo CodeLlama
llm = OllamaLLM(
    model="codellama",  # Cambia a tu modelo descargado
    base_url="http://localhost:11434"  # Asegúrate de que Ollama está corriendo en este puerto
)

# Plantilla de prompt para que el modelo extraiga información
scraping_prompt = """
Analiza el siguiente contenido HTML y extrae los datos solicitados en el siguiente formato JSON.

Devuelve exclusivamente un JSON estructurado, como este ejemplo:
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

No incluyas ningún texto adicional, ni explicaciones, ni comentarios, ni código, únicamente un JSON válido. Si no puedes extraer información relevante, devuelve exactamente esto: [].

Contenido HTML (limitado a 5000 caracteres):
{html_content}
"""

# Directorios para archivos guardados
SCRAPED_PAGES_DIR = "scraped_pages"
PROCESSED_PAGES_DIR = "processed_pages"
os.makedirs(SCRAPED_PAGES_DIR, exist_ok=True)
os.makedirs(PROCESSED_PAGES_DIR, exist_ok=True)

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

def extract_json(raw_result):
    """Intenta extraer el JSON de la salida del modelo."""
    try:
        # Encuentra la primera ocurrencia de un JSON en la salida
        start_idx = raw_result.find("[")
        end_idx = raw_result.rfind("]") + 1
        if start_idx != -1 and end_idx != -1:
            json_str = raw_result[start_idx:end_idx]
            return json.loads(json_str)
        else:
            print("No se encontró un JSON válido en la salida.")
            return []
    except json.JSONDecodeError as e:
        print("Error al decodificar la salida del modelo:", e)
        return []

def process_saved_pages():
    """Procesa los archivos HTML guardados con CodeLlama y guarda resultados JSON."""
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

                # Validar y extraer el JSON de la salida
                result = extract_json(raw_result)

                # Guardar el resultado en un archivo JSON
                output_filename = os.path.join(PROCESSED_PAGES_DIR, f"{filename.replace('.html', '.json')}")
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
