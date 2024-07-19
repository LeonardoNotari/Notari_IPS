#%% Cell1

import matplotlib.pyplot as plt
import subprocess
import os
import hashlib
from math import log

#riceve una stringa di bit e restituisce un valore hash 
def return_hash(bit_string):
        byte_string = bytes(bit_string, 'utf-8')
        hash_object = hashlib.new('MD5')
        hash_object.update(byte_string)
        return hash_object.hexdigest()

def to_bits(data):
    return ''.join(format(byte, '08b') for byte in data)

class Img:
    def __init__(self, name, model, tags, tags_value):
        self.name = name
        self.model = model
        self.tags = tags
        self.tags_value = tags_value


tags = []
tags_value = []
images = []
models = []
path = os.path.abspath(__file__)   # si assegna il path dello script
path = path[:-9]                   # si elimina il nome 'script.py', di lunghezza 9, per ottenere il path della directory
images_path = path + "images\\"    # si entra nella directory images
models = os.listdir(images_path)   # si assegna una lista di nomi dei modelli
for m in models:
    model_images_path = images_path + m + '\\'   # si ricostruisce dal path dello script il path di ogni immagine
    image_names = os.listdir(model_images_path)  # si assegna una lista di nomi delle immagini per ogni modello
    for image_name in image_names:
        img_path = model_images_path + image_name
        command = ['exiftool', model_images_path + image_name]
        metadata = subprocess.check_output(command)  # si estraggono i metadati con l'eseguibile exiftool.exe
        try: 
            metadata = metadata.decode('utf-8')
            metadata = metadata[:-1].split('\n')
            image_tags = []
            image_tags_value = []
            for s in metadata:
                a = s.split(':')                    # per ogni riga dei metadati si dividono tag e valore in una variabile di appoggio
                tag = a[0].rstrip()                 # si eliminano gli spazi alla fine di ogni tag 
                tag_value = tag + a[1].rstrip()     # si concatenano nuovamente i tag ai valori per l'analisi delle coppie
                if 'Binary data' in tag_value:      # se la coppia tag-valore presenta la stringa 'Binary data' che indica che il valore non è stato decodificato si converte la stringa di bit con una hash
                    t = tag.replace(' ','')
                    value = subprocess.run(['exiftool', '-b', f'-{t}', img_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    bits_value = to_bits(value.stdout)
                    tag_value = tag + ' ' + return_hash(bits_value)
                image_tags.append(tag)
                image_tags_value.append(tag_value)
                if tag not in tags:
                    tags.append(tag)
                if tag_value not in tags_value:
                    tags_value.append(tag_value)
            images.append(Img(image_name, m, image_tags, image_tags_value))
        except Exception as e:
            print("An exception has occurred:" + e)
            


# %% Cell2

result_tag = []
for m in models:
    for t in tags:
        PG = 0   # Numero di immagini del modello G
        PnG = 0  # Numero di immagini di modelli diversi da G
        wG = 0   # Numero di immagini del modello G che presentano il tag w
        wnG = 0  # Numero di immagini di modelli diversi da G che presentano il tag w
        for i in images:
            if m == i.model:
                PG += 1
                if t in i.tags:
                    wG += 1
            else:
                PnG += 1
                if t in i.tags:
                    wnG += 1
        PwG = wG/PG                     # Probabilità che il tag w si trovi in un'immagine del modello G
        PwnG = wnG/PnG                  # Probabilità che il tag w si trovi in immagini di modelli diversi da G
        L = PwG/(PwnG + 1/len(images))  # si calcola il coefficiente di verosomiglianza
        result_tag.append([t, m, L]) 
        
        
result_tag_value = []
for m in models:
    for t in tags_value:  # si procede in modo analogo per le coppie tag-valore
        PG = 0
        PnG = 0
        wG = 0
        wnG = 0
        for i in images:
            if m == i.model:
                PG += 1
                if t in i.tags_value:
                    wG += 1
            else:
                PnG += 1
                if t in i.tags_value:
                    wnG += 1
        PwG = wG/PG
        PwnG = wnG/PnG
        L = PwG/(PwnG + 1/len(images))
        result_tag_value.append([t, m, L]) 


#%% Cell3


for i in range(len(models)):
    tags_result = []
    
    Ls = []
    result = result_tag                          # si sceglie se rappresentare i risultati dei soli tag o le coppie tag valore
    result = sorted(result, key=lambda x: x[2])  # si ordinano i risultati in base al valore della verosomiglianza
    for l in result:   
        if l[1] == models[i] and l[2] > 0:
            tags_result.append(l[0])
            Ls.append(log(l[2],10)) 
     
            
    plt.figure(figsize=(10, 0.25*len(Ls)))     
    plt.barh(tags_result,Ls)
    plt.title(models[i])

    ticks = [0, 1, 2]
    plt.xticks(ticks, ticks)
    plt.xlim(0, 2)
    plt.xlabel('Likelyhood')
    plt.ylabel('Tags')
    plt.tight_layout()
    # Use the follow lines to save the plots
    #directory_path = path + '\\Plots\\' + models[i]        
    #plt.savefig(directory_path)
    plt.show()
















