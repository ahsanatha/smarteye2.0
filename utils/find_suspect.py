import json
import numpy as np
import cv2
import os
from scipy.spatial import distance

ctr = 0

def cosineSimilarity(a, b):
    return 1 - distance.cosine(a, b)

def find_idx_suspect(cam_idx, suspect_ft, target_dir):
    global ctr
    ctr = 0
    print('start find idx suspect')
    threshold_similarity = 0.90
    
    # Open Json from start time (suspect picked) until end time (reporting time)
    with open('static/Json ' + str(cam_idx) +'/0.json') as json_file:
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
                image = cv2.imread('static/Camera ' + str(cam_idx) + '/' + dt['image'])
                rc_img = cv2.rectangle(image.copy(), 
                                       (bbox[idx_suspect][1], bbox[idx_suspect][0]), 
                                       (bbox[idx_suspect][3], bbox[idx_suspect][2]), (0,0,255), 2)
                cv2.imwrite(target_dir + '/' + str(ctr) + '.jpg', rc_img)
                ctr += 1
                print('Found suspect in frame ', str(i))
                return i, idx_suspect # return number of frame and suspect index of the frame
    return -1, -1

def find_suspect(cam_idx, frame_num, suspect_ft, target_dir, goes='forward'):
    global ctr
    threshold_similarity = 0.90
    print('start finding suspect')
    # Open Json from start time (suspect picked) until end time (reporting time)
    with open('static/Json ' + str(cam_idx) +'/0.json') as json_file:
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
            image = cv2.imread('static/Camera ' + str(cam_idx) + '/' + dt['image'])
            idx_suspect = np.argmax(sim) # Find the most similar to suspect feature
            if sim[idx_suspect] > threshold_similarity:
                rc_img = cv2.rectangle(image.copy(), 
                                       (bbox[idx_suspect][1], bbox[idx_suspect][0]), 
                                       (bbox[idx_suspect][3], bbox[idx_suspect][2]), (0,0,255), 2)
                cv2.imwrite(target_dir + '/' + str(ctr) + '.jpg', rc_img)
                ctr += 1
            else:
                cv2.imwrite(target_dir + '/' + str(ctr) + '.jpg', image)
                ctr += 1
    print('done finding suspect')


if __name__ == '__main__':
    cam = 0
    suspect_ft = [
                        -0.20103244483470917,
                        0.1068970263004303,
                        -0.04029526934027672,
                        0.02151142805814743,
                        0.016779689118266106,
                        0.09878851473331451,
                        0.032723456621170044,
                        0.1752738505601883,
                        0.08075065165758133,
                        -0.0645892322063446,
                        -0.03539903834462166,
                        0.05210938677191734,
                        -0.13572922348976135,
                        0.017378322780132294,
                        -0.0875438004732132,
                        0.024278102442622185,
                        0.056456975638866425,
                        -0.08927277475595474,
                        -0.06437205523252487,
                        0.024065738543868065,
                        0.05854900926351547,
                        0.027030305936932564,
                        -0.04840238392353058,
                        0.08090505748987198,
                        -0.15388745069503784,
                        -0.00340868323110044,
                        -0.07530340552330017,
                        -0.07250108569860458,
                        -0.16997632384300232,
                        -0.09734346717596054,
                        -0.022611750289797783,
                        -0.10509739071130753,
                        0.07557757943868637,
                        -0.06378451734781265,
                        -0.023769469931721687,
                        0.12902066111564636,
                        -0.010504028759896755,
                        0.026612892746925354,
                        -0.043699149042367935,
                        -0.0634840801358223,
                        -0.008921469561755657,
                        0.17289628088474274,
                        -0.008797811344265938,
                        0.04646986722946167,
                        -0.08032363653182983,
                        -0.001692935940809548,
                        0.02565416879951954,
                        -0.03629124537110329,
                        -0.10218074917793274,
                        -0.05656883120536804,
                        -0.10476583987474442,
                        0.05374633148312569,
                        -0.12059946358203888,
                        -0.09073860198259354,
                        -0.07899414002895355,
                        -0.021986013278365135,
                        -0.006156681105494499,
                        0.0171939879655838,
                        0.03651804104447365,
                        -0.02954697608947754,
                        -0.043941885232925415,
                        -0.04194074869155884,
                        0.09040293097496033,
                        0.020973972976207733,
                        0.13285943865776062,
                        -0.0006226306431926787,
                        -0.19155718386173248,
                        -0.07986964285373688,
                        0.07529489696025848,
                        -0.06039538234472275,
                        0.097948357462883,
                        -0.01997723989188671,
                        0.07020580023527145,
                        -0.0924365296959877,
                        0.07117181271314621,
                        -0.08239199966192245,
                        -0.13845756649971008,
                        -0.013990468345582485,
                        -0.03638681024312973,
                        -0.11739028245210648,
                        -0.0057169110514223576,
                        0.03902219235897064,
                        0.13067109882831573,
                        0.13801385462284088,
                        -0.08465748280286789,
                        0.029338710010051727,
                        -0.06950333714485168,
                        0.08485444635152817,
                        0.03485336899757385,
                        -0.012904619798064232,
                        0.07349511981010437,
                        -0.017557868734002113,
                        -0.11471392959356308,
                        -0.021434981375932693,
                        -0.024126775562763214,
                        -0.11331292986869812,
                        -0.20273330807685852,
                        -0.07652334868907928,
                        0.1513354778289795,
                        0.015750663354992867,
                        0.008597122505307198,
                        -0.014200210571289062,
                        0.023227335885167122,
                        -0.033209070563316345,
                        -0.08531960099935532,
                        0.020557096228003502,
                        -0.13034385442733765,
                        0.20839186012744904,
                        0.18162435293197632,
                        -0.03873958811163902,
                        0.14590860903263092,
                        -0.005377938039600849,
                        0.0009916649432852864,
                        -0.17189450562000275,
                        -0.009933077730238438,
                        0.04460475221276283,
                        0.08257395774126053,
                        -0.06947868317365646,
                        0.0354592390358448,
                        0.06997231394052505,
                        0.00561651261523366,
                        0.025294966995716095,
                        0.12930987775325775,
                        0.12203720211982727,
                        0.002890147967264056,
                        -0.09622450917959213,
                        0.11879222095012665,
                        -0.2648364305496216
                    ]
    frame_num, suspect_idx = find_idx_suspect(cam, suspect_ft, 'res' + str(cam))
    if (frame_num is not -1):
        find_suspect(cam, frame_num, suspect_ft, 'res' + str(cam), 'forward')
        find_suspect(cam, frame_num, suspect_ft, 'res' + str(cam), 'backward')