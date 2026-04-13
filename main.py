import streamlit as st
from ytmusicapi import YTMusic

st.set_page_config(page_title="YTMusic Artist Extractor", layout="centered")

st.title("👤 Extração de Nome do Artista")
st.write("Buscando artista via `longBylineText` no endpoint `/next`.")

song_id = st.text_input("Digite o Song ID:", value="ikFFVfObwss")

if st.button("Buscar Artista", type="primary"):
    if song_id:
        with st.spinner("Lendo metadados..."):
            try:
                yt = YTMusic()
                body = {"videoId": song_id}
                response = yt._send_request("next", body)
                
                artist_name = None

                # Função de busca específica para o padrão identificado
                def extract_artist(obj):
                    if isinstance(obj, dict):
                        # Alvo direto no campo que você encontrou
                        if "longBylineText" in obj:
                            try:
                                # O primeiro item do 'runs' costuma ser o nome do artista
                                return obj["longBylineText"]["runs"][0]["text"]
                            except (KeyError, IndexError):
                                pass
                        
                        # Busca recursiva caso o campo esteja mais profundo
                        for v in obj.values():
                            result = extract_artist(v)
                            if result: return result
                    elif isinstance(obj, list):
                        for item in obj:
                            result = extract_artist(item)
                            if result: return result
                    return None

                artist_name = extract_artist(response)

                if artist_name:
                    st.success("Artista encontrado!")
                    st.header(f"🎸 {artist_name}")
                else:
                    st.error("Não foi possível localizar 'longBylineText' no JSON.")
                    with st.expander("Inspecionar JSON bruto"):
                        st.json(response)
                        
            except Exception as e:
                st.error(f"Erro na requisição: {e}")
