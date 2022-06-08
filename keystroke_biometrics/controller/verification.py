from math import ceil

def verify_samples(learnsamples, testsamples, encrypted):
    """
    performs verification process for each testsample against model (build from learnsamples)

    Parameter:
    learnsamples: samples from "valid" user
    testsample: samples to check against learnsamples
    encrypted: boolean, indicates whether character values from learnsamples should be treated as encrypted

    Return:
    tuple of
        number of compared values
        maximal euklidean distance from all testsamples
        dictionary with normalized euklidean distance per testsample identifier
    """
    
    if not testsamples or not learnsamples:
        # no compared values, no results
        return (0, 0, {})
    modelvalues = create_modelvalues(learnsamples)
    testvalues_per_sample = []
    if encrypted:
        for s in testsamples:
            # replace unknown (encrypted) char values with possible matches by nearest neighbor 
            testvalues_per_sample.append((create_testvalues_by_nearest_neighbor(modelvalues, s), s.get_short_identifier()))
    else:
        for s in testsamples:
            testvalues_per_sample.append((s.values_per_feature_and_chars, s.get_short_identifier()))
    compared_values = 0
    max_euklidean_distance = 0
    # create eukidean distance dictionary
    euklidean_distance_dict = {}
    # do verification process for every testsample
    for tuple in testvalues_per_sample:
        # form vectors from modelvalues and testvalues
        vectors = build_vectors_as_list (modelvalues, tuple[0])
        vector_size = len(vectors)
        if (vector_size > 0):
            # model and testvalues are comparable
            compared_values += vector_size
            euklidean_distance = calculate_euklidean_distance(vectors)
            # add identifier as key and normalized euklidean distance as value to dictionary
            euklidean_distance_dict[tuple[1]] = euklidean_distance
            # set new max_euklidean_distance if necessary
            if euklidean_distance > max_euklidean_distance:
                max_euklidean_distance = euklidean_distance
    return (compared_values, int(ceil(max_euklidean_distance)), euklidean_distance_dict)

def get_results_per_threshold(distance_per_sample, compared_values, max_threshold):
    """
    provides results per threshold as text and char data

    Parameter:
    distance_per_sample: dictionary with normalized euklidean distance per testsample identifier
    compared_values: number of compared values
    max_threshold: highest threshold

    Return:
    tuple of
        results as text
        y acceptance
        y rejection
    """

    if compared_values == 0:
        # samples contained no comparable data
        return (None, None, None)
    # set thresholds based on max_threshold
    thresholds = []
    for i in range(11):
        thresholds.append(round(max_threshold/10 * i, 0))
    # set acceptance and rejection values as list
    y_acceptance = [0] * 11
    y_rejection = [0] * 11
    for distance in distance_per_sample.values():
        # compare all thresholds with euklidean distance
        for i in range(11):
            if distance <= thresholds[i]:
                # adjust number of successful verfications
                y_acceptance[i] = y_acceptance[i]+1
    # form results as text
    acceptance_text = "Acceptance:\n\n"
    rejection_text = "Rejection:\n\n"
    euklidean_distance_text = "Normalized euklidean distance:\n\n"
    # calculate acceptance rate in percentage 
    testsample_count = len(distance_per_sample)
    for i in range(11):
        acceptance_percentage = round(y_acceptance[i]/testsample_count * 100, 2)
        rejection_percentage = round(100 - acceptance_percentage, 2)
        y_acceptance[i]  = acceptance_percentage
        y_rejection[i] = rejection_percentage
        # append formatted acceptance and rejection values to text
        absolute_threshold = thresholds[i]
        acceptance_text += f"{0.1 * i:.1f} ({absolute_threshold:04.0f} ms) - {acceptance_percentage} %\n"
        rejection_text += f"{0.1 * i:.1f} ({absolute_threshold:04.0f} ms) - {rejection_percentage} %\n"
    # append formatted euklidean distance per testsample to text
    number = 1
    for k, v in distance_per_sample.items():
        euklidean_distance_text += f"{number}. Testsample\n\"{k}\"\nDistance: {v:.4f} ms\n"
        number += 1
    # form result substrings to total results text
    results_as_text = f"Threshold span:\n0 ms (0) - {max_threshold} ms (1)\n\n{acceptance_text}\n{rejection_text}\n{euklidean_distance_text}\nCompared values in total: {compared_values}"
    return (results_as_text, y_acceptance, y_rejection) 
    


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
    # source: F. Monrose, A. D. Rubin: Keystroke dynamics as a biometric for authentication, 2000, http://www1.cs.columbia.edu/~hgs/teaching/security/hw/keystroke.pdf, page 356 (last visit 21/05/2022)
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

