@author: leono
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 24 12:14:48 2024

@author: leono
"""

#%% Cell1

import matplotlib.pyplot as plt
import subprocess
import os
import hashlib
from math import log

def return_hash(stringa_di_bit):
        byte_string = bytes(stringa_di_bit, 'utf-8')
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
path = os.path.abspath(__file__)
path = path[:-9]
images_path = path + "images\\"
models_names = os.listdir(images_path)
for m in models_names:
    print(m)
    models.append(m)
    model_images_path = images_path + m + '\\'
    image_names = os.listdir(model_images_path)
    for image_name in image_names:
        img_path = model_images_path + image_name
        command = ['exiftool', model_images_path + image_name]
        metadata = subprocess.check_output(command)
        try:
            metadata = metadata.decode('utf-8')
            metadata = metadata[:-1].split('\n')
            image_tags = []
            image_tags_value = []
            for s in metadata:
                a = s.split(':')
                tag = a[0].rstrip()
                tag_value = tag + a[1].rstrip()
                if 'Binary data' in tag_value:
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
        PG = 0
        PnG = 0
        wG = 0
        wnG = 0
        for i in images:
            if m == i.model:
                PG += 1
                if t in i.tags:
                    wG += 1
            else:
                PnG += 1
                if t in i.tags:
                    wnG += 1
        PwG = wG/PG
        PwnG = wnG/PnG
        L = PwG/(PwnG + 1/len(images))
        result_tag.append([t, m, L]) 
        
        
result_tag_value = []
for m in models:
    for t in tags_value:
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
    result = result_tag
    result = sorted(result, key=lambda x: x[2])
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
















