import json
import os
import pickle
import random
from operator import itemgetter

import numpy as np
# need to install tesseract with conda install -c conda-forge tesseract
import pytesseract
from sklearn.cluster import DBSCAN

# IMAGE_DIRECTORY = "D:\\Alie\\Documents\\CollectesTwitter\\AhashExps\\allGJ\\SteakAllPictures"
IMAGE_DIRECTORY = "D:\\Alie\\Documents\\CollectesTwitter\\AhashExps\\grand_remplacement"
MODELS_DIRECTORY = "D:\\Alie\\Documents\\Projets\\AnalysesImages\\outputs\\vectors"

with open(os.path.join(MODELS_DIRECTORY, "tree.pkl"), "rb") as f:
    tree = pickle.load(f)

with open(os.path.join(MODELS_DIRECTORY, "dic_vec_pca_10.pkl"), "rb") as f:
    vector_dic = pickle.load(f)

with open(os.path.join(MODELS_DIRECTORY, "dic_ahashs.pkl"), "rb") as f:
    hash_dic = pickle.load(f)

# with open(r"D:\Alie\Documents\Projets\AnalysesImages/outputs/vectors/dic_ocr.json", "r", encoding='utf-8') as f:
#     dic_ocr = json.load(f)

image_labels = list(vector_dic.keys())
# ocr_data = {image: dic_ocr[hash_dic[image]] for image in image_labels}

# TODO: update image_labels according to what's really in the directory

vectors = list(vector_dic.values())


def get_all_images():
    all_images = sorted(zip(hash_dic.values(), hash_dic.keys()))
    # display the images at a random start
    i = random.randint(0, len(all_images) - 1)
    return [{'name': image, 'dist': None} for _, image in [*all_images[i:], *all_images[:i]]]


def find_similar(image_name, nb=len(image_labels)):
    vector = vector_dic[image_name]
    dist, ind = tree.query(vector.reshape(1, -1), k=nb)
    indices = [x for x in ind[0]]
    distances = [x for x in dist[0]]
    print(distances[0])
    return [{'name': image_labels[i], 'dist': float('%.2f'%(distances[index]))} for index, i in enumerate(indices)]


def make_clusters():
    res = []
    clusters = DBSCAN(eps=3).fit(vectors)
    for cluster in list(set(clusters.labels_)):
        image_clusters = np.asarray(image_labels)[clusters.labels_ == cluster]
        ahash_clusters = itemgetter(*image_clusters)(hash_dic)
        res.append([{'name': '/static/' + image, 'dist': None} for _, image in sorted(zip(ahash_clusters, image_clusters))])
    return res


# def get_ocr_data():
#     return ocr_data



