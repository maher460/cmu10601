import math
import json
import numpy as np
import multiprocessing
import itertools
import tqdm

NUM_GAUSSIANS = 32

DEBUG = True

NUM_ITERATIONS = 10


##############################
# numpy settings

# np.seterr(all='raise')


##############################
# Processing data

print("Loading parsed data...")
traindata_processed_file = open("parsed_data/data1.universalenrollparsed", "r")
data = json.loads(traindata_processed_file.read())
traindata_processed_file.close()
print("Done loading parsed data!")

print("Converting dataset to numpy array...")

data_np = np.array(data)

print("Done converting dataset to numpy array!")


num_inst = data_np.shape[0]
num_cattr = data_np.shape[1]

if DEBUG:
    print('num_inst: ', num_inst)
    print('num_cattr: ', num_cattr)

print("Forming all_N_ranges...")
all_N_ranges = [range(num_inst), range(NUM_GAUSSIANS)]
print("Done forming all_N_ranges!")

# if DEBUG:
#   print('all_N_ranges: ', all_N_ranges)

print("Forming all_N_combs...")
all_N_combs = list(itertools.product(*all_N_ranges))
print("Done forming all_N_combs!")



###############################
# Loading initial parameters

print("Loading initial parameters...")
traindata_processed_file = open("parsed_data/data1.initialparameters", "r")
initial_params = json.loads(traindata_processed_file.read())
traindata_processed_file.close()
print("Done loading initial parameters!")

print("Converting initial parameters into numpy arrays...")
mixture_weights = np.array(initial_params['mixture_weights'])

means = np.array(initial_params['means'])

variances = np.array(initial_params['variances'])
print("Done converting initial parameters into numpy arrays!")



###############################
# Calculating new parameters with multiple iterations

iter_count = 0

while iter_count < NUM_ITERATIONS:

    print "\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    print ("Iteration number: " + str(iter_count) + "\n")

    iter_count = iter_count + 1


    # Summary: N(X; mean(k), covar(k))

    def map_gaussian_pdf(x):
        
        inst_idx = x[0]
        g_mean_idx = x[1]
        g_covar_idx = x[1]

        X = data_np[inst_idx]
        mean = means[g_mean_idx]
        covar = variances[g_covar_idx]

        X_sub_mean_square = np.square(np.subtract(X, mean))
        X_sub_mean_div_covar = np.divide(X_sub_mean_square, covar)
        sum_X_sub_mean_div_covar = np.sum(X_sub_mean_div_covar)

        #det_covar = np.prod(covar)
        two_pi_d = np.multiply(np.power(np.pi, num_cattr), 2)

        #one_div_root_two_pi_d_det_covar = np.divide(1,np.sqrt(det_covar * two_pi_d))

        two_pi_d_ln = 257*(math.log(2*math.pi))

        covar_ln = np.log(np.array(covar))
        det_covar_ln = np.sum(covar_ln)

        ln_one_div_root_two_pi_d_det_covar = (-0.5) * (two_pi_d_ln + det_covar_ln)

        # try:
        #     ln_one_div_root_two_pi_d_det_covar = np.log(one_div_root_two_pi_d_det_covar)   # RuntimeWarning: divide by zero encountered in log
        # except Exception as e:
        #     print "\n\nERROR:"
        #     print e
        #     print ("inst_idx", inst_idx)
        #     print ("g_mean_idx", g_mean_idx)
        #     print ("covar", covar)
        #     print ("two_pi_d", two_pi_d)
        #     print ("det_covar", det_covar)
        #     print ("one_div_root_two_pi_d_det_covar", one_div_root_two_pi_d_det_covar)
        #     print "\n"

        ln_res = (ln_one_div_root_two_pi_d_det_covar)+((-0.5)*sum_X_sub_mean_div_covar)
        res = np.power(np.e, ln_res)

        # if res == 0.0:
        #     print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

        #     print ("inst_idx", inst_idx, X)
        #     print ("g_mean_idx", g_mean_idx, mean)
        #     print ("two_pi_d", two_pi_d, two_pi_d_ln)
        #     print ("covar", covar, covar_ln)
        #     print ("det_covar_ln", det_covar_ln)
        #     print ("ln_one_div_root_two_pi_d_det_covar", ln_one_div_root_two_pi_d_det_covar)
        #     print ("sum_X_sub_mean_div_covar", sum_X_sub_mean_div_covar)
        #     print ("ln_res", ln_res)
        #     print ("res", res)

        #     print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        
        if res == 0.0:
            zero_count = 1
        else:
            zero_count = 0

        return (x, res, zero_count)

    all_N_combs_res_dict = {}
    zero_counts = 0

    print(">>>>> About to map gaussian pdf...")
    pool = multiprocessing.Pool()

    total_computations = len(all_N_combs)
    for res in tqdm.tqdm(pool.imap_unordered(map_gaussian_pdf, all_N_combs,
                                             chunksize=10),
                         total=total_computations):
        all_N_combs_res_dict[res[0]] = res[1]
        zero_counts = zero_counts + res[2]

    #all_N_combs_res = pool.map(map_gaussian_pdf, all_N_combs)

    pool.close()
    pool.join()
    print(">>>>> Done with parallel map gaussian pdf....")

    print("zero_counts: ", zero_counts)

    # print "About to start the heavy N computations..."
    # total_computations = len(all_N_combs)
    # count = 0

    # all_N_combs_res = []
    # for a in all_N_combs:
    #     try:
    #         res = map_gaussian_pdf(a)
    #         print res
    #         all_N_combs_res.append(res)
    #         count = count + 1
    #         if count % 10000 == 0:
    #             print "   Completed computing " + str(count) + " of " + str(total_computations) + " computations"
    #     except Exception as e:
    #         print ("a", a)
    #         print ("data_np[a[0]]", data_np[a[0]])
    #         print ("means[a[1]]", means[a[1]])
    #         print ("covar[a[2]]", covar[a[2]])
    #         print e
    # print "Done with the heavy N computations"

    #print all_N_combs_res

    # print all_N_combs_res_dict


    g_indices = range(NUM_GAUSSIANS)

    # Summary: sum(P(k') * N(X; mean(k'), covar(k')))
    def map_sum_g_weight_N_X(x):
        res = 0.0
        for i in g_indices:
            N_combs_res_key = (x, i)
            res = res + (mixture_weights[i] * all_N_combs_res_dict[N_combs_res_key])

        return (x, res)


    inst_indices = range(num_inst)
    sum_g_weights_N_X = {}
    max_log_likelihood = 0.0

    print(">>>>> About to map sum_g_weight_N_X...")
    pool = multiprocessing.Pool()

    total_computations = num_inst
    for res in tqdm.tqdm(pool.imap_unordered(map_sum_g_weight_N_X, inst_indices,
                                             chunksize=10),
                         total=total_computations):
        sum_g_weights_N_X[res[0]] = res[1]

        if (res[1] != 0.0 and (not math.isnan(res[1]))):
            max_log_likelihood = max_log_likelihood + np.log(res[1])

    pool.close()
    pool.join()
    print(">>>>> Done with parallel map sum_g_weight_N_X....")


    # Summary: P(k | X)
    def map_posteriori_prob(x):

        inst_idx = x[0]
        g_idx = x[1]

        X = data_np[inst_idx]
        g_weight = mixture_weights[g_idx]
        sum_g_weight_N = sum_g_weights_N_X[inst_idx]

        N_combs_res_key = (inst_idx, g_idx)
        N_res = all_N_combs_res_dict[N_combs_res_key]

        # old_settings = np.seterr(all='ignore')
        # np.seterr(all='raise')
        try:
            res0 = np.multiply(mixture_weights[g_idx], N_res)
            res = np.divide(res0, sum_g_weight_N)   # RuntimeWarning: invalid value encountered in double_scalars
        except Exception as e:
            print "\n\nError:"
            print e
            print (mixture_weights[g_idx], N_res, sum_g_weight_N)
            print ("inst_idx", inst_idx)
            print ("g_idx", g_idx)
            print ("N_res", N_res)
            print ("mixture_weights[g_idx]", mixture_weights[g_idx])
            print ("sum_g_weight_N", sum_g_weight_N)
            print "\n"
        # np.seterr(**old_settings)

        return (x, res)


    posteriori_probs = {}
    sum_posteriori_probs = [0.0] * NUM_GAUSSIANS
    sum_posteriori_probs_X = np.array([[0.0] * num_cattr] * NUM_GAUSSIANS)
    print(">>>>> About to map posteriori probs...")
    pool = multiprocessing.Pool()

    total_computations = len(all_N_combs)
    for res in tqdm.tqdm(pool.imap_unordered(map_posteriori_prob, all_N_combs,
                                             chunksize=10),
                         total=total_computations):
        posteriori_probs[res[0]] = res[1]
        sum_posteriori_probs[(res[0][1])] = sum_posteriori_probs[(res[0][1])]+res[1]
        sum_posteriori_probs_X[(res[0][1])] = np.add(sum_posteriori_probs_X[(res[0][1])],(res[1]*np.array(data_np[res[0][0]])))

    #all_N_combs_res = pool.map(map_gaussian_pdf, all_N_combs)

    pool.close()
    pool.join()
    print(">>>>> Done with parallel map posteriori probs....")

    # print posteriori_probs
    # print sum_posteriori_probs
    # print sum_posteriori_probs_X

    new_weights = []
    new_means = []
    for i in g_indices:
        new_weight = (sum_posteriori_probs[i] / (num_inst * 1.0))
        new_weights.append(new_weight)

        new_mean_np = (sum_posteriori_probs_X[i] / sum_posteriori_probs[i])
        new_mean = new_mean_np.tolist()
        new_means.append(new_mean)



    # Summary: sum(P(k|X) (X - mean(k))^2)
    def map_sum_numer_covar(x):
        inst_idx = x[0]
        g_idx = x[1]

        X = data_np[inst_idx]
        posteriori_prob_res_key = (inst_idx, g_idx)
        posteriori_prob = posteriori_probs[posteriori_prob_res_key]
        new_mean = means[g_idx]

        res = posteriori_prob * np.square(np.subtract(X, new_mean))

        return (x, res)

    new_covars_np = np.array([[0.0] * num_cattr] * NUM_GAUSSIANS)

    print(">>>>> About to map sum_numer_covar...")
    pool = multiprocessing.Pool()

    total_computations = len(all_N_combs)
    for res in tqdm.tqdm(pool.imap_unordered(map_sum_numer_covar, all_N_combs,
                                             chunksize=10),
                         total=total_computations):
        new_covars_np[(res[0][1])] = np.add(new_covars_np[(res[0][1])], res[1])

    pool.close()
    pool.join()
    print(">>>>> Done with parallel map sum_numer_covar....")

    for i in g_indices:
        new_covars_np[i] = new_covars_np[i] / sum_posteriori_probs[i]

    new_covars = new_covars_np.tolist()

    # print new_weights
    # print new_means
    # print new_covars
    
    mixture_weights = np.array(new_weights)
    means = np.array(new_means)
    variances = new_covars_np

    print ("max_log_likelihood", max_log_likelihood)











