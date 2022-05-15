thresholds = (800, 720, 640, 560, 480, 400, 320, 240, 160, 80, 0)

def verify_per_threshold(learnsamples, testsamples, encrypted):
    """
    performs verification process for each testsample against model (build from learnsamples) with different thresholds

    Parameter:
    learnsamples: samples from "valid" user
    testsample: samples to check against learnsamples
    encrypted: boolean, indicates whether character values from learnsamples should be treated as encrypted

    Return:
    number of compared values, results as dictionary with thresholds and acceptance rate in %
    """
    modelvalues = create_modelvalues(learnsamples)
    print("modelvalues")
    print(str(modelvalues))
    testvalues_per_sample = []
    if encrypted:
        for s in testsamples:
            # replace unknown (encrypted) char values with possible matches by nearest neighbor 
            testvalues_per_sample.append(create_testvalues_by_nearest_neighbor(modelvalues, s))
    else:
        for s in testsamples:
            testvalues_per_sample.append(s.values_per_feature_and_chars)
    compared_values = 0
    # create results dictionary with key: threshold, value: number of successful verfications
    results = {}
    for th in thresholds:
        results[th] = 0
    # do verification process for every testsample
    for testvalues in testvalues_per_sample:
        print("testvalues")
        print(str(testvalues))
        # form vectors from modelvalues and testvalues
        vectors = build_vectors_as_list (modelvalues, testvalues)
        vector_size = len(vectors)
        if (vector_size > 0):
            # model and testvalues are comparable
            compared_values += vector_size
            euklidean_distance = calculate_euklidean_distance(vectors)
            print ("eulidische distance")
            print (euklidean_distance)
            # compare all thresholds with euklidean distance
            for k, v in results.items():
                if euklidean_distance <= k:
                    # adjust number of successful verfications
                    results[k] = v+1
    # calculate acceptance rate in percentage 
    for k, v in results.items():
        results[k] = round(v/len(testsamples) * 100, 2)
    print ("results in %")
    print (str(results))
    return (compared_values, results)

def create_modelvalues(learnsamples):
    """
    forms model dictionary with mean time values from learnsamples

    Parameter:
    learnsamples: samples which should be used to form model

    Return:
    model dictionary, key: (feature, chars) value: time_mean
    """

    model = {}
    # for every sample put values in model dictionary
    for s in learnsamples:
        for k, v in s.values_per_feature_and_chars.items():
            if k in model:
                # key is already in model dictionary, add time value to list
                model[k].extend(v)
            else:
                # key is not in model dictionary, add new pair
                model[k] = v
    # for every pair in model dictionary calculate mean time
    for k, v in model.items():
        size = len(v)
        if size > 1:
            t_mean = 0
            for time in v:
                t_mean += time
            t_mean /= size
            model[k] = round(t_mean)
        else:
            # change value from list to single value
            model[k] = v[0]
    return model

def build_vectors_as_list (modelvalues, testvalues):
    """
    forms list which represents vectors matching in features and chars for every point

    Parameter:
    modelvalues: dictionary representing the model values, key: (feature, char) value: time_mean
    testvalues: dictionary representing the test values, key: (feature, char) value: [time_1, ..., time_n]

    Return:
    list [(r1, u1), ..., (rn, un)] which represents the vectors R = [r1, ..., rn], U = [u1, ..., un]
    """

    vectors = []
    # for every testvalue find modelvalue with matching feature and chars
    for feature_chars, timelist in testvalues.items():
        reference_value = modelvalues.get(feature_chars, None)
        if reference_value is not None:
        # feature-chars-combination is in testvalues AND modelvalues
            for time in timelist:
                # add new tuple with time from model and time from testvalues
                vectors.append((reference_value, time))
    return vectors

def calculate_euklidean_distance (vector_list):
    """
    calculates normalized euklidean distance

    Parameter:
    vector_list: list of tuples [(r1, u1), ..., (rn, un)], which represents the vectors R = [r1, ..., rn], U = [u1, ..., un]

    Return:
    normalized euklidean distance
    """

    # euklidean distance: D(R,U) = ((r1 - u1)^2 + ... + (rn - un)^2) ^ 0.5
    euklidean_distance = 0
    # sum each result for (ri - ui)^2
    for pair in vector_list:
        euklidean_distance += (pair[0] - pair[1])**2
    # draw root from sum
    euklidean_distance = euklidean_distance**0.5
    # normalize: D(R,U) / N^1/2
    euklidean_distance_norm = euklidean_distance / (len(vector_list)**0.5)
    return round(euklidean_distance_norm, 4)

def create_testvalues_by_nearest_neighbor(model, testsample):
    """
    pretends char values from testsample are unknown (e.g. encrypted) and finds possible matching char values from model, based on nearest neighbor

    Parameter:
    model: model dictionary, key: (feature, chars) value: time_mean
    testsample: sample with pretended encryption of char values

    Return:
    dictionary with test values but char value from model, key: (f, c by nearest neighbor) value: [time_1, ..., time_n]
    """
    
    testvalues = {}
    # for each value in testsample search for nearest neighbor
    for k_test, v_test in testsample.values_per_feature_and_chars.items():
        for t in v_test:
            nearest_neighbor_key = None
            # compare each value from model with test value
            for k_model, v_model in model.items():
                if (k_test[0] == k_model[0]):
                    # feature values are matching, compare time values
                    # char values k_test[1] are ignored
                    distance = abs(v_test[0] - v_model)
                    if nearest_neighbor_key is None or distance < nearest_neighbor_distance:
                        # current model value is best match
                        nearest_neighbor_distance = distance
                        nearest_neighbor_key = k_model
            if (nearest_neighbor_key is not None):
                # nearest neighbor was found
                if nearest_neighbor_key in testvalues:
                    # key is already in testvalues, add time value to list
                    testvalues[nearest_neighbor_key].append(t)
                else:
                    # key is not in testvalues, insert new pair
                    testvalues[nearest_neighbor_key] = [t]
    return testvalues

