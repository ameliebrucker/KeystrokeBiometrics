thresholds = (80, 160, 240, 320, 400, 480, 560, 640, 720, 800)

# testvalues: [(values_sample_1 = {(f1, c2): [t1, t2], ...), (values_sample_2), ...]
# modelvalues: {k: t_mean}
def verify_per_threshold(learnsamples, testsamples, encrypted):
    modelvalues = create_modelvalues(learnsamples)
    print("modelvalues")
    print(str(modelvalues))
    testvalues_per_sample = []
    if encrypted:
        for s in testsamples:
            testvalues_per_sample.append(create_testvalues_by_nearest_neighbor(modelvalues, s))
    else:
        for s in testsamples:
            testvalues_per_sample.append(s.values_per_feature_and_char)

    # dictionary with threshold : number of successful verfications
    results = {}
    for th in thresholds:
        results[th] = 0
    compared_values = 0
    for testvalues in testvalues_per_sample:
        print("testvalues")
        print(str(testvalues))
        vectors = build_vectors_as_list (modelvalues, testvalues)
        print("vectors")
        print(str(vectors))
        vector_size = len(vectors)
        if (vector_size > 0):
            compared_values += vector_size
            euklidean_distance = calculate_euklidean_distance(vectors)
            print ("eulidische distance")
            print (euklidean_distance)
            # compare threshold with euklidean distance, if <= sample is verified, number of verification rises by 1
            for k, v in results.items():
                if euklidean_distance <= k:
                    results[k] = v+1
        print ("results")
        print (str(results))
        print ("compared Values")
        print (str(compared_values))
    return (compared_values, results)

"""
modelbildung
d = {fd, cd, td} der Wertemengen W1, …, Wwn in L, deren Werte für f (Merkmalstyp) und c (Zeichen) übereinstimmen: fd = fm und cd = cm.
Aus den Zeiterfassungen [td1, …, tdn] dieser Datenpunkte wird die Durchschnittszeit tmean berechnet. In der neuen Modelwertemenge WModel
wird für jede Merkmal-Zeichen-Kombination ein Datenpunkt {fm, cm, tmean} 

"""
# modelvalues: {k: t_mean}

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
    # create model by calculating mean values
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
    for k, v in testvalues.items():
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
    #normalization
    # D (R, U) Norm = D (R, U) / [N]1/2
    euklidean_distance_norm = euklidean_distance / (len(vector_list)**0.5)
    return round(euklidean_distance_norm, 4)

# form {(f, c by nearest neighbor): (t1, t2, ...)}
# k_test[1] wird ignoriert
def create_testvalues_by_nearest_neighbor(model, testsample):
    testvalues = {}
    # für jeden wert in testsample
    for k_test, v_test in testsample.values_per_feature_and_char.items():
        for t in v_test:
            nearest_neighbor_key = None
            # für jedes model wert vergleichen
            for k_model, v_model in model.items():
                # fm = ft, same feature
                if (k_test[0] == k_model[0]):
                    distance = abs(v_test[0] - v_model)
                    if nearest_neighbor_key is None or distance < nearest_neighbor_distance:
                        nearest_neighbor_distance = distance
                        nearest_neighbor_key = k_model
            # nearest neighbor was found
            if (nearest_neighbor_key is not None):
                if nearest_neighbor_key in testvalues:
                    testvalues[nearest_neighbor_key].append(t)
                else:
                    testvalues[nearest_neighbor_key] = [t]
    return testvalues

