import streamlit as st
import requests
import os

# Ocultar la clave API en los secretos de Streamlit
API_KEY = st.secrets["TOGETHER_API_KEY"]

def check_api_availability():
    try:
        response = requests.get("https://api.together.xyz/v1/ping", headers={"Authorization": f"Bearer {API_KEY}"})
        response.raise_for_status()
        return True
    except Exception as e:
        st.error(f"La API de Together no está disponible: {e}")
        return False

def generate_verse():
    try:
        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
                "messages": [],
                "max_tokens": 50,
                "temperature": 0.7,
                "top_p": 0.7,
                "top_k": 50,
                "repetition_penalty": 1,
                "stop": ["<|eot_id|>"],
                "stream": True,
            },
        )
        response.raise_for_status()
        json_response = response.json()
        if "choices" in json_response and json_response["choices"]:
            verse = json_response["choices"][0]["text"].strip()
            return verse
        else:
            st.error("La respuesta de la API no contiene el campo 'choices'.")
            return ""
    except Exception as e:
        st.error(f"Error generando el verso: {e}")
        return ""

def generate_romance(num_verses):
    """Genera un romance completo con la estructura métrica especificada"""
    romance = []
    for i in range(num_verses):
        verse = generate_verse()
        if verse:
            if i % 2 == 0:
                romance.append(f"{i+1} {verse},")
            else:
                romance.append(f"{i+1} {verse}")
    return "\n".join(romance)

def main():
    st.set_page_config(page_title="Generador de Romances")
    st.title("Generador de Romances")

    num_verses = st.number_input("Número de versos (máximo 99):", min_value=1, max_value=99, step=1)
    theme = st.text_input("Tema del romance:")

    if st.button("Generar Romance"):
        if num_verses > 99:
            st.write("Lo siento, el máximo de versos es 99.")
        elif not check_api_availability():
            st.write("Lo siento, la API de Together no está disponible en este momento. Por favor, inténtalo de nuevo más tarde.")
        else:
            try:
                romance = generate_romance(int(num_verses))
                st.markdown(f"**Tema: {theme}**")
                st.markdown(f"```\n{romance}\n```")
            except Exception as e:
                st.error(f"Error generando el romance: {e}")

if __name__ == "__main__":
    main()
