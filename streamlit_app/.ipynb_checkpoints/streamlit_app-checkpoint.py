import streamlit as st
import pandas as pd
import ast

# Load dataset groupé
df = pd.read_csv('../grouped2_dataset_levallois_perret.csv')

# convertir le string de list en une vraie list ex: '[1,2,3]' --> [1,2,3]
def extract_image_urls(images_str):
    return ast.literal_eval(images_str)

def main():
    st.title('ANNONCES SIMILAIRES')
    
    grouped = df.groupby('GROUP_KEY').first().reset_index()
    selected_group_key = st.selectbox('Selectionner un GROUP_KEY:', grouped['GROUP_KEY'].tolist())
    st.markdown("""
    <div style='background-color: rgba(94, 107, 128, 0.5);border-radius:10px;padding:10px'>
    <h3>Remarque sur le GROUP_KEY:</h3>
    Le triplet de critères composant le <i>GROUP_KEY</i> est défini comme suit:
    <ol>
    <li><b>Type de propriété</b>: Par exemple, 'APARTMENT', 'HOUSE', etc.</li>
    <li><b>Intervalle de surface </b>: Il s'agit d'une fourchette de surface en mètres carrés. Par exemple, (100, 122) représente un intervalle de 100m² à 122m².</li>
    <li><b>Nombre de pièces</b> : Le nombre total de pièces dans la propriété.</li>
    </ol>
    Ce triplet est utilisé pour regrouper les annonces similaires provenant de différentes sources. Chaque groupe est censé contenir des annonces qui sont très probablement les mêmes mais proviennent de différentes plateformes.</div>
    """, unsafe_allow_html=True)

    st.markdown("""<hr/><hr/>""", unsafe_allow_html=True)
    
    records = df[df['GROUP_KEY'] == selected_group_key]

    for _, record in records.iterrows():
        st.subheader("Description")
        
        # Affiche les premiers 250 caractères de la description
        short_description = record['DESCRIPTION'][:250]
        # Si la description est plus longue que 250 caractères, donne la possibilité d'afficher tout
        if len(record['DESCRIPTION']) > 250:
            show_full_description = st.button("Agrandir", key=record['ID']) 
            if show_full_description:
                st.markdown(record['DESCRIPTION'])
            else:
                st.markdown(short_description + "...")
        else:
            st.markdown(record['DESCRIPTION'])
        
        st.markdown(f"""Publié sur: <b><span style="background-color: green; border-radius:10px;padding:10px; color: white;">{record['CRAWL_SOURCE']}</span></b>""", unsafe_allow_html=True)
        images = extract_image_urls(record['IMAGES'])
        cols = st.columns(3)  

        for i, img_url in enumerate(images):
            cols[i % 3].image(img_url)
        st.markdown("---")

if __name__ == '__main__':
    main()
