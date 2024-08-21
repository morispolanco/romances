import streamlit as st
import together
import secrets

# Esconder la API Key en los secretos de Streamlit
API_KEY = secrets.get("TOGETHER_API_KEY")

# Definir la función para generar un romance
def generar_romance(num_versos, tema):
    # Establecer la estructura métrica del romance
    estructura = "8a 8- 8a 8- 8a 8- 8a"

    # Establecer la rima para los pares de versos
    rimas = {"a": ["madrugaba", "caballo", "mar", "bebe", "cantar", "escuchar", "caminante", "navegante", "mal", "vientos", "furias"], 
             "b": ["mañanita", "orillas", "aviones", "paraban", "detiene", "vuelve", "Dios", "terrestre", "marino", "atras", "adelante"]}

    # Generar el romance
    romance = []
    for i in range(num_versos):
        verso = ""
        if i % 2 == 0:
            verso += f"{rimas['a'][i//2]} "
        else:
            verso += f"{rimas['b'][i//2]} "
        verso += f"{tema} "
        verso += f"{estructura}"
        romance.append(verso)

    return "\n".join(romance)

# Página principal de la app
st.title("Generador de Romances")

# Ingresar el número de versos y el tema
num_versos = st.number_input("Número de versos:", min_value=1, max_value=99)
tema = st.text_input("Tema del romance:")

# Generar el romance
if st.button("Generar romance"):
    romance = generar_romance(num_versos, tema)
    st.write(romance)
