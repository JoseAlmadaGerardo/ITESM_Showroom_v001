import streamlit as st

import streamlit as st
from openai import OpenAI
#import PyPDF2
header= {
    "authorization":st.secrets["auth_token"],
    "content-type": "application/json"
    }

st.set_page_config(page_title="UCase_005", page_icon="📊")
st.markdown("# UCase_005")
st.sidebar.header("UCase_005")

# Title.
st.title("Manufacturing: Use Case #5​")
st.subheader("Factory Asset Effectiveness.​")
st.write("📄 Answers to questions about .TX, .MD, and .PDF documents. Upload a document below and ask a question about it – GPT will answer!")
st.write("Note: To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys)."
)
# Solicitar al usuario su clave de API de OpenAI mediante `st.text_input`.
# Alternativamente, puedes almacenar la clave de API en `./.streamlit/secrets.toml` y acceder a ella
# mediante `st.secrets`, ver https://docs.streamlit.io/develop/concepts/connections/secrets-management

#st.secrets["OpenAI_key"] == "auth_key"
openai_api_key = st.text_input("Clave API de OpenAI", type="password")
if not openai_api_key:
    st.info("Por favor, introduce tu clave API para continuar.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

   # Permitir al usuario cargar un archivo mediante `st.file_uploader`.
    uploaded_file = st.file_uploader(
        "Sube un documento (.txt o .md)", type=("txt", "md")
    )

    # Pedir al usuario una pregunta mediante `st.text_area`.
    question = st.text_area(
        "¡Ahora haz una pregunta sobre el documento!",
        placeholder="¿Puedes darme un resumen breve?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:

        # Procesar el archivo subido y la pregunta.
        document = uploaded_file.read().decode()
        messages = [
            {
                "role": "user",
                "content": f"Aquí tienes un documento: {document} \n\n---\n\n {question}",
            }
        ]

        # Generar una respuesta utilizando la API de OpenAI.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        # Mostrar la respuesta en la aplicación utilizando `st.write_stream`.
        st.write_stream(stream)
