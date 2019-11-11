import os
import cv2
import json
import numpy as np
from scipy.spatial import distance

def cosineSimilarity(a, b):
    return 1- distance.cosine(a, b)

def similarity_score(predicts, currents):
    fin = []
    for predict in predicts:
        sub_fin = []
        for current in currents:
            sub_fin.append(cosineSimilarity(predict, current))
        fin.append(sub_fin)
    return np.mean(fin, axis=1)

def find_idx_suspect(cam_idx, suspect_ft, target_dir):
    with open('Json result ' + str(cam_idx) +'/result.json') as json_file:
        data = json.load(json_file)

    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    for i,dt in enumerate(data['data']):
        image = cv2.imread(dt['image'])
        sim = []
        bbox = []
        for j,dd in enumerate(dt['object']):
            if len(dd['bbox']) > 0:
                bb = dd['bbox']
                ft = dd['feature']
                sim.append(cosineSimilarity(ft, suspect_ft))
                bbox.append(bb)
        if len(sim)>0:
            idx_suspect = np.argmax(sim)
            print(i, sim, idx_suspect)
            if sim[idx_suspect] > 0.9:
                rc_img = cv2.rectangle(image.copy(), (bbox[idx_suspect][1], bbox[idx_suspect][0]), (bbox[idx_suspect][3], bbox[idx_suspect][2]), (0,0,255), 2)
                cv2.imwrite(target_dir + '/' + os.path.basename(dt['image']), rc_img)
                return i, idx_suspect
    return -1, -1 

def find_suspect(cam_idx, frame_num, suspect_ft, target_dir, size, goes='forward'):
    max_age = 0

    # Open Json from start time (suspect picked) until end time (reporting time)
    with open('Json result ' + str(cam_idx) +'/result.json') as json_file:
        data = json.load(json_file)

    # Create a list to save suspect's feature caught by tracking algorithm
    current_position = None
    current_features = []
    poss = []
    current_features.append(suspect_ft)

    # Initialize forward / backward search
    if goes == 'forward':
        end = len(data['data'])
        counter = 1
    else:
        end = 0
        counter = -1
    start = frame_num + counter

    # Start loooping on json
    for i in range(start, end, counter):
        # Get i-th data
        dt = data['data'][i]
        # Open i-th image
        image = cv2.imread(dt['image'])
        
        # Get predicted feature (in future we don't need to extract the feature since its already saved from live running webcam)
        features = [] 
        for j,dd in enumerate(dt['object']):
            if len(dd['bbox']) > 0:
                bb = dd['bbox'].copy()
                features.append(dd['feature'])
                center_bb = (bb[2]+bb[0])/2, (bb[3]+bb[1])/2
                h = bb[2] - bb[0]
                w = bb[3] - bb[1]
                r = h/w
                poss.append([center_bb[0], center_bb[1], h, r])
        
        # If there's a person then find the most similar to the suspect
        if len(features) > 0:
            preds = similarity_score(features, current_features)
            id_pred = np.argmax(preds)
            print(i, preds, id_pred)
            if preds[id_pred] > 0.8:
                current_features.append(features[id_pred])
                if len(current_features) > 10:
                    current_features = list(current_features[-10:].copy())
                    current_position = (center_bb[0], center_bb[1], h, r)
                bb = dt['object'][id_pred]['bbox']
                rc_img = cv2.rectangle(image.copy(), (bb[1], bb[0]), (bb[3], bb[2]), (0,0,255), 2)
                cv2.imwrite(target_dir + '/' + os.path.basename(dt['image']), rc_img)
                max_age = 0
            else:
                cv2.imwrite(target_dir + '/' + os.path.basename(dt['image']), image)
                max_age += 1
        else:
            cv2.imwrite(target_dir + '/' + os.path.basename(dt['image']), image)
            max_age += 1
        if max_age > 29:
            break