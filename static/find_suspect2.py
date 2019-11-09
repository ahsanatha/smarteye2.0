import json
import numpy as np
import cv2
import os
from scipy.spatial import distance

def cosineSimilarity(a, b):
    return 1 - distance.cosine(a, b)

def find_idx_suspect(cam_idx, suspect_ft, target_dir):
    
    threshold_similarity = 0.9
    
    # Open Json from start time (suspect picked) until end time (reporting time)
    with open('Json ' + str(cam_idx) +'/0.json') as json_file:
        data = json.load(json_file)

    # Iterate for all data
    for i, dt in enumerate(data['data']):
        sim = []
        bbox = []

        for j,dd in enumerate(dt['object']):
            if len(dd['bbox']) > 0:
                bb = dd['bbox']
                ft = dd['feature']
                sim.append(cosineSimilarity(ft, suspect_ft))
                bbox.append(bb)

        if len(sim)>0:
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
            print(sim)
            idx_suspect = np.argmax(sim) # Find the most similar to suspect feature
            if sim[idx_suspect] > threshold_similarity:
                image = cv2.imread('Camera ' + str(cam_idx) + '/' + dt['image'])
                rc_img = cv2.rectangle(image.copy(), 
                                       (bbox[idx_suspect][1], bbox[idx_suspect][0]), 
                                       (bbox[idx_suspect][3], bbox[idx_suspect][2]), (0,0,255), 2)
                cv2.imwrite(target_dir + '/' + dt['image'], rc_img)
                print('Found suspect in frame ', str(i))
                return i, idx_suspect # return number of frame and suspect index of the frame
    return -1, -1

def find_suspect(cam_idx, frame_num, suspect_ft, target_dir, goes='forward'):
    threshold_similarity = 0.86
    
    # Open Json from start time (suspect picked) until end time (reporting time)
    with open('Json ' + str(cam_idx) +'/0.json') as json_file:
        data = json.load(json_file)

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
        
        # Get predicted feature (in future we don't need to extract the feature since its already saved from live running webcam)
        sim = []
        bbox = []
        for j,dd in enumerate(dt['object']):
            if len(dd['bbox']) > 0:
                bb = dd['bbox']
                ft = dd['feature']
                sim.append(cosineSimilarity(ft, suspect_ft))
                bbox.append(bb)
        
        # If there's a person then find the most similar to the suspect
        if len(sim) > 0:
            image = cv2.imread('Camera ' + str(cam_idx) + '/' + dt['image'])
            idx_suspect = np.argmax(sim) # Find the most similar to suspect feature
            if sim[idx_suspect] > threshold_similarity:
                rc_img = cv2.rectangle(image.copy(), 
                                       (bbox[idx_suspect][1], bbox[idx_suspect][0]), 
                                       (bbox[idx_suspect][3], bbox[idx_suspect][2]), (0,0,255), 2)
                cv2.imwrite(target_dir + '/' + dt['image'] + '.jpg', rc_img)
            else:
                cv2.imwrite(target_dir + '/' + dt['image'] + '.jpg', image)


if __name__ == '__main__':
    cam = 0
    suspect_ft = [
                        -0.05385545641183853,
                        0.029841650277376175,
                        -0.02984703704714775,
                        0.004198096226900816,
                        0.02223401702940464,
                        0.0396585650742054,
                        -0.03878176584839821,
                        -0.014437070116400719,
                        -0.1682448834180832,
                        -0.025577988475561142,
                        -0.12515372037887573,
                        -0.045369938015937805,
                        -0.12014202773571014,
                        0.08565638214349747,
                        -0.07886458188295364,
                        0.0318920761346817,
                        0.03371867910027504,
                        0.05497249960899353,
                        0.04084860533475876,
                        -0.05477224662899971,
                        -0.07204066962003708,
                        0.011537213809788227,
                        0.06271880120038986,
                        0.014534786343574524,
                        -0.011187857948243618,
                        0.08945610374212265,
                        -0.02481434866786003,
                        0.08787849545478821,
                        0.001306359888985753,
                        0.054250963032245636,
                        0.008137732744216919,
                        -0.14646916091442108,
                        -0.129246324300766,
                        0.10032714158296585,
                        -0.016291413456201553,
                        -0.11308151483535767,
                        -0.012022903189063072,
                        -0.06331215798854828,
                        -0.1330319494009018,
                        -0.012164603918790817,
                        -0.004498486407101154,
                        0.07080036401748657,
                        0.07222981750965118,
                        0.1967204064130783,
                        -0.02642374485731125,
                        0.1993962973356247,
                        0.09946204721927643,
                        0.016730429604649544,
                        -0.0694008395075798,
                        -0.03843148052692413,
                        -0.03948548063635826,
                        -0.019790997728705406,
                        -0.07993622124195099,
                        -0.03645889088511467,
                        0.1440102905035019,
                        0.16822300851345062,
                        0.024604136124253273,
                        0.1261787712574005,
                        0.06561779975891113,
                        0.06521745771169662,
                        0.10836879909038544,
                        0.10885642468929291,
                        -0.03531474992632866,
                        0.011875111609697342,
                        0.05341236665844917,
                        -0.16295690834522247,
                        0.027938300743699074,
                        0.001999487169086933,
                        0.06569927930831909,
                        0.0743020549416542,
                        0.024821167811751366,
                        0.13097859919071198,
                        0.11884992569684982,
                        -0.000528602977283299,
                        0.08204697072505951,
                        0.06162864342331886,
                        0.049069855362176895,
                        -0.03774868696928024,
                        0.0400407649576664,
                        -0.0015104548074305058,
                        0.025181900709867477,
                        0.03655926138162613,
                        -0.029974117875099182,
                        -0.0033626763615757227,
                        -0.030492093414068222,
                        -0.06008220463991165,
                        -0.1847047209739685,
                        0.20320218801498413,
                        0.051400862634181976,
                        -0.0061086853966116905,
                        -0.1532650589942932,
                        0.011418619193136692,
                        -0.03160426393151283,
                        -0.019080882892012596,
                        -0.11820267885923386,
                        -0.07378426194190979,
                        -0.18680618703365326,
                        0.05539670214056969,
                        -0.13556642830371857,
                        0.03997263312339783,
                        -0.0035431983415037394,
                        -0.06267262995243073,
                        0.0012091074604541063,
                        -0.08822324126958847,
                        -0.06209466978907585,
                        -0.01994890160858631,
                        0.03639136627316475,
                        -0.06491421163082123,
                        -0.07783567905426025,
                        0.15104995667934418,
                        -0.1866169273853302,
                        0.09099656343460083,
                        -0.12860046327114105,
                        -0.08184175193309784,
                        -0.2280367910861969,
                        0.030918020755052567,
                        -0.02521081268787384,
                        -0.09400538355112076,
                        0.044815436005592346,
                        0.004938377998769283,
                        -0.16492052376270294,
                        0.016553647816181183,
                        0.12386446446180344,
                        -0.019634490832686424,
                        -0.003445293754339218,
                        -0.12702840566635132,
                        0.19709934294223785,
                        0.15811803936958313
                    ]
    frame_num, suspect_idx = find_idx_suspect(cam, suspect_ft, 'res' + str(cam))
    if (frame_num is not -1):
        find_suspect(cam, frame_num, suspect_ft, 'res' + str(cam), 'forward')
        find_suspect(cam, frame_num, suspect_ft, 'res' + str(cam), 'backward')