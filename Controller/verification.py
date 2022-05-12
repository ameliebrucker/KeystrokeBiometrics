thresholds = (80, 160, 240, 320, 400, 480, 560, 640, 720, 800)

def verify_without_encryption(learnsamples, testsamples):
    modelvalues = create_modelvalues(learnsamples)
    print("modelvalues")
    print(str(modelvalues))

    # dictionary with threshold : number of successful verfications
    results = {}
    for th in thresholds:
        results[th] = 0

    verification_possible = False
    for testsample in testsamples:
        print("testvalues")
        print(str(testsample.values_per_feature_and_char.items()))
        vectors = build_vectors_as_list (modelvalues, testsample.values_per_feature_and_char.items())
        print("vectors")
        print(str(vectors))
        if (len(vectors) > 0):
            verification_possible = True
            euklidean_distance = calculate_euklidean_distance(vectors)
            print ("eulidische distance")
            print (euklidean_distance)

            # compare threshold with euklidean distance, if <= sample is verified, number of verification rises by 1
            for k, v in results.items():
                if euklidean_distance <= k:
                    results[k] = v+1
        print ("verification possible")
        print (str(verification_possible))
        print ("results")
        print (str(results))
    return (verification_possible, results)

"""
modelbildung
d = {fd, cd, td} der Wertemengen W1, …, Wwn in L, deren Werte für f (Merkmalstyp) und c (Zeichen) übereinstimmen: fd = fm und cd = cm.
Aus den Zeiterfassungen [td1, …, tdn] dieser Datenpunkte wird die Durchschnittszeit tmean berechnet. In der neuen Modelwertemenge WModel
wird für jede Merkmal-Zeichen-Kombination ein Datenpunkt {fm, cm, tmean} 

"""
def create_modelvalues(learnsamples):
    # combine values from learnsamples
    model = {}
    # für jedes samples wird werden werte in dictionary "model" integriert (k: / value=[t1, t2, t3, ...])
    for s in learnsamples:
        for k, v in s.values_per_feature_and_char.items():
            if k in model:
                model[k].extend(v)
            else:
                model[k] = v
    # create model
    for k, v in model.items():
        # dict nach muster (k: / value= t_mean) entsteht
        size = len(v)
        if size > 1:
            t_mean = 0
            for time in v:
                t_mean += time
            t_mean /= size
            model[k] = round(t_mean)
        else:
            model[k] = v[0]
    return model

def build_vectors_as_list (modelvalues, testvalues):
     # find matching pairs (fm=ft, cm=ct)
    vectors = []
    for k, v in testvalues:
        reference_value = modelvalues.get(k, None)
        if reference_value is not None:
            # zeit, da form (f, c): [t1, t2, t3, ...]
            for time in v:
                vectors.append((reference_value, time))
    # result: vector_combination = [(r1, u1), ..., (rn, un)]
    return vectors

def calculate_euklidean_distance (vector_list):
    # calculate euklidean distance per r u pair
    euklidean_distance = 0
    for pair in vector_list:
        euklidean_distance += (pair[0] - pair[1])**2
    euklidean_distance = euklidean_distance**0.5
    print("distanz ohne normalisierung")
    print(str(euklidean_distance))
    #normalization
    # D (R, U) Norm = D (R, U) / [N]1/2
    euklidean_distance_norm = euklidean_distance / (len(vector_list)**0.5)
    return round(euklidean_distance_norm, 4)

def create_testvalues_by_nearest_neighbor(model, testsample):
    # form {(f,c): (t1, t2, ...)}
    test_values = {}
    # für jeden wert in testsample
    for k_test, v_test in testsample.values_per_feature_and_char.items():
        nearest_neighbor = None
        for k_model, v_model in model.items():
            if (k_test[0] == k_model[0]):
                # same feature
                distance = abs(v_test[0] - v_model)
                if nearest_neighbor is None or distance < nearest_neighbor:
                    nearest_neighbor = distance


