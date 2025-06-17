import streamlit as st
import groq 

MODELOS = ['llama3-8b-8192', 'llama3-70b-8192','mixtral-8x7b-32768']

#configurar la pagina

def configurar_pagina():
    st.set_page_config(page_title="CHADbot Python V1")
    st.title("Bienvenidos a CHADbot Version 1")

    #crear cliente d groq

def crear_ciente_groq():
        groq_api_key = st.secrets['GROQ_API_KEY']
        return groq.Groq(api_key=groq_api_key)
    
    #mostrar barra lateral

def mostrar_sidebar():
        st.sidebar.title("Elegi tu modelo de IA favorito")
        modelo = st.sidebar.selectbox('hola',MODELOS,index=0)
        st.write(f'**Elegiste el modelo:** {modelo}')
        return modelo 
    
# INICIALIZAR EL ESTADO DEL CHAT
def inicializar_estado_chat():
     if "mensajes" not in st.session_state:
        st.session_state.mensajes = []


# MOSTRAR MENSAJES PREVIOS
def obtener_mensajes_previos():
      for mensaje in st.session_state.mensajes: #recorre los mensajes de st.session_state.mensajes
            with st.chat_message(mensaje['role']): #quien lo envia?
                  st.markdown(mensaje["content"]) #que envia?



# OBTENER MENSAJE DEL USUARIO
def obtener_mensaje_usuario():
      return st.chat_input("Envia tu mensaje")


#GUARDAR LOS MENSAJES DEL CHAT
def agregar_mensajes_previos(role, content):    
   st.session_state.mensajes.append({"role" : role , "content" : content}) 

#MOSTRAR MENSAJES EN PANTALLA
def mostrar_mensajes_en_pantalla(role, content):
    with st.chat_message(role):
        st.markdown(content)
#OBTENER RESPUESTA DEL MODELO
def obtener_respuesta_modelo(cliente, modelo, mensaje):
    respuesta =  cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream= False
    )
    return respuesta.choices[0].message.content

#



def ejecutar_chat():
        configurar_pagina()
        cliente = crear_ciente_groq()
        modelo = mostrar_sidebar()

    
        inicializar_estado_chat()
        mensaje_usuario = obtener_mensaje_usuario()
        obtener_mensajes_previos()
        print(mensaje_usuario)
        
        if mensaje_usuario:
            agregar_mensajes_previos("user",mensaje_usuario)
            mostrar_mensajes_en_pantalla("user",mensaje_usuario)
        
            respuesta_contenido = obtener_respuesta_modelo(cliente, modelo,st.session_state.mensajes )

            agregar_mensajes_previos("assistant",respuesta_contenido)
            mostrar_mensajes_en_pantalla("assistant",respuesta_contenido)

    

 

    
    #ejecutar la app (si __name__ == "__main__" se ejecuta la funcion y __main__ es mi archivo principal)
    
if __name__ == '__main__':
    ejecutar_chat()

      
