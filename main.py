import streamlit as st
from ytmusicapi import YTMusic

st.set_page_config(page_title="YTMusic Artist Extractor", layout="centered")

st.title("👤 Extração de Nome do Artista")
st.write("Acessando o endpoint `/next` para capturar metadados do artista.")

song_id = st.text_input("Digite o Song ID:", value="ikFFVfObwss")

if st.button("Buscar Artista", type="primary"):
    if song_id:
        with st.spinner("Analisando JSON..."):
            try:
                yt = YTMusic()
                body = {"videoId": song_id}
                response = yt._send_request("next", body)
                
                def find_artist_name(obj):
                    # O nome do artista no YT Music geralmente está em objetos 'runs'
                    # vinculados a um browseId de canal (UC...)
                    if isinstance(obj, dict):
                        if "browseId" in obj and isinstance(obj["browseId"], str):
                            if obj["browseId"].startswith("UC") or obj["browseId"].startswith("FMat"):
                                # Verificamos se o texto está no mesmo nível ou acima
                                return obj.get("text")
                        
                        for v in obj.values():
                            res = find_artist_name(v)
                            if res: return res
                    elif isinstance(obj, list):
                        for item in obj:
                            res = find_artist_name(item)
                            if res: return res
                    return None

                # Tentativa 2: Busca por padrões comuns de texto de autoria
                def fallback_search(obj):
                    if isinstance(obj, dict):
                        # Procura por campos comuns que guardam o nome do artista
                        for key in ["author", "artist", "longBylineText", "byline"]:
                            if key in obj:
                                # Geralmente é uma estrutura de 'runs'
                                try:
                                    return obj[key]["runs"][0]["text"]
                                except:
                                    continue
                        for v in obj.values():
                            res = fallback_search(v)
                            if res: return res
                    return None

                artist = find_artist_name(response) or fallback_search(response)

                if artist:
                    st.success("Artista localizado!")
                    st.header(artist)
                else:
                    st.error("Nome do artista não encontrado no JSON.")
                    with st.expander("Debug: Ver JSON completo"):
                        st.json(response)
                        
            except Exception as e:
                st.error(f"Erro na requisição: {e}")
