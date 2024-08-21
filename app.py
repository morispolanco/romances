import streamlit as st
import requests
import os

# Ocultar la clave API en los secretos de Streamlit
API_KEY = st.secrets["TOGETHER_API_KEY"]

def generate_verse():
    """Genera un verso de romance utilizando la API de Together"""
    try:
        response = requests.get(f'https://api.together.xyz/v1/generate?prompt=romance&max_tokens=50&temperature=0.7&top_p=0.9&n=1&seed=42', headers={'Authorization': f'Bearer {API_KEY}'})
        response.raise_for_status()
        verse = response.json()['generated_text']
        return verse.strip()
    except requests.exceptions.RequestException as e:
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
    return '\n'.join(romance)

def main():
    st.set_page_config(page_title="Generador de Romances")
    st.title("Generador de Romances")

    num_verses = st.number_input("Número de versos (máximo 99):", min_value=1, max_value=99, step=1)
    theme = st.text_input("Tema del romance:")

    if st.button("Generar Romance"):
        if num_verses > 99:
            st.write("Lo siento, el máximo de versos es 99.")
        else:
            try:
                romance = generate_romance(int(num_verses))
                st.markdown(f"**Tema: {theme}**")
                st.markdown(f"```\n{romance}\n```")
            except Exception as e:
                st.error(f"Error generando el romance: {e}")

if __name__ == "__main__":
    main()
