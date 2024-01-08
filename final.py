import streamlit as st
import json
import random
from nltk import word_tokenize
from nltk.corpus import cmudict #The Carnegie Mellon University Pronouncing Dictionary 'dictionnaire de prononciation de l'anglais nord-américain'
from googletrans import Translator #est une bibliothèque python gratuite et illimitée qui implémente l'API de Google Translate

#le fichier json des haikus est recupéré sur guthub dans le lien suivant : 
with open('db.json', 'r', encoding='utf-8') as file:
    poems_data = json.load(file)

#upploder le fichier de differents types de poemes français 
with open("Frenchpoems3.json", "r", encoding="utf-8") as file:
    french_poems = json.load(file)

# la demarche suivie pour generer des poemes haikus : 
# -  Elle compte ensuite le nombre de syllabes en analysant 
#  la prononciation phonétique et en relevant le nombre de chiffres à la fin de chaque son 


def count_syllables(word):
    d = cmudict.dict()
    return [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]][0]

#generer un poem en français avec la biblio random 

def generate_random_french_poem():
    random_poem = random.choice(french_poems)
    lines = random_poem["Content"].split("\n")
    random.shuffle(lines)
    return "\n".join(lines)

#traduire de français en anglais 
def translate_to_english(poem):
    translator = Translator()
    translated_lines = [translator.translate(line, dest='en').text for line in poem.split("\n")]
    return "\n".join(translated_lines)

#la meme chose pour generer un haiku par lignes
def generate_random_haiku(data):
    author = random.choice(list(data.keys()))
    haikus = data[author]['haikus']
    poem_lines = random.sample(haikus, 3)
    return poem_lines

#la validation des syllabes : 
#explicaton de l'algo :
# -Prend les trois lignes d'un Haiku et vérifie si le nombre de syllabes dans chaque ligne correspond à la structure
#   classique d'un Haiku, qui est de 5 syllabes dans la première ligne, 7 dans la deuxième, et 5 dans la troisième 

def validate_syllables(poem_lines):
    syllables_per_line = [5, 7, 5]
    for i in range(3):
        words = word_tokenize(poem_lines[i])
        syllable_count = sum(count_syllables(word) for word in words)
        if syllable_count != syllables_per_line[i]:
            return False
    return True



###########################################################################################################
#La partie interface streamlit 

st.title("The best words in the best order")

# un bouton pour choisir le type si haiku ou poesie française 
poem_type = st.radio("Selectionnez un type qui vous passionne:", ["Haiku", "poésie fraçaise"])

# la meme chose pour choisir une langue afin d'effectuer une traduction 
language = st.radio("Selectionnez une langue:", ["Anglais", "Français"])

if poem_type == "Haiku":
    # activer la fct du haiku 
    random_haiku = generate_random_haiku(poems_data)

    
    st.subheader("Voici un Haiku:")
    for line in random_haiku:
        st.write(line)

    # traduction : 
    if language == "Français":
        st.subheader("Traduction:")
        translator = Translator()
        for line in random_haiku:
            translated_line = translator.translate(line, dest='fr').text
            st.write(translated_line)
    elif language == "Anglais":
        st.subheader("Traduction en Anglais:")
        translated_haiku = translate_to_english("\n".join(random_haiku))
        st.write(translated_haiku)

else:
    st.subheader("Voici un poeme en fraçais:")
    random_french_poem = generate_random_french_poem()
    st.write(random_french_poem)

    # traducution auto si anglais est selectionné 
    if language == "Anglais":
        st.subheader("Traduction en Anglais:")
        translated_poem = translate_to_english(random_french_poem)
        st.write(translated_poem)
