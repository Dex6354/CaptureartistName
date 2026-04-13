import streamlit as st
from ytmusicapi import YTMusic

st.set_page_config(page_title="YTMusic Artist Extractor", layout="centered")

st.title("🎵 Extração de Nome do Artista")
st.write("Acessando o endpoint `/next` para capturar metadados do artista.")

song_id = st.text_input("Digite o Song ID:", value="ikFFVfObwss")

if st.button("Buscar Artista", type="primary"):
    if song_id:
        with st.spinner("Simulando requisição..."):
            try:
                yt = YTMusic()
                
                # Requisição ao endpoint 'next'
                body = {"videoId": song_id}
                endpoint = "next"
                response = yt._send_request(endpoint, body)
                
                artist_name = None

                # Função para buscar o nome do artista no JSON
                # O YT Music armazena o artista geralmente em 'byline' ou 'longBylineText'
                def find_artist(obj):
                    if isinstance(obj, dict):
                        # Verifica se é um objeto de navegação de artista
                        if "browseId" in obj and isinstance(obj["browseId"], str):
                            if obj["browseId"].startswith("UC") or obj["browseId"].startswith("FMat"):
                                # Se encontrar o ID do artista, o texto associado é o nome
                                if "text" in obj:
                                    return obj["text"]
                        
                        for v in obj.values():
                            result = find_artist(v)
                            if result: return result
                    elif isinstance(obj, list):
                        for item in obj:
                            result = find_artist(item)
                            if result: return result
                    return None

                artist_name = find_artist(response)

                if artist_name:
                    st.success("Nome do Artista encontrado!")
                    st.header(f"👤 {artist_name}")
                else:
                    st.error("Não foi possível localizar o nome do artista no JSON.")
                    with st.expander("Inspecionar JSON completo"):
                        st.json(response)
                        
            except Exception as e:
                st.error(f"Erro na requisição: {e}")
