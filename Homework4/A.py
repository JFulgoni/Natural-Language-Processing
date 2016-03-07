import nltk
from nltk.align import IBMModel1
from nltk.align import IBMModel2
from nltk.align import Alignment
import time

one_error = []
two_error = []

# TODO: Initialize IBM Model 1 and return the model.
def create_ibm1(aligned_sents):
    # from homework pdf
    # ibm = IBMModel1(aligned_sents, num_iters)
    ibm = IBMModel1(aligned_sents, 10)
    return ibm

# TODO: Initialize IBM Model 2 and return the model.
def create_ibm2(aligned_sents):
    # nearly the same as above
    ibm = IBMModel2(aligned_sents, 10)
    return ibm

# TODO: Compute the average AER for the first n sentences
#       in aligned_sents using model. Return the average AER.
def compute_avg_aer(aligned_sents, model, n):
    total = 0
    for i in range (0, n):
        alignment = model.align(aligned_sents[i])
        aer = alignment.alignment_error_rate(aligned_sents[i])
        total += aer
    avg_aer = total / float(n)
    return avg_aer

# TODO: Computes the alignments for the first 20 sentences in
#       aligned_sents and saves the sentences and their alignments
#       to file_name. Use the format specified in the assignment.
def save_model_output(aligned_sents, model, file_name):
    my_file = open(file_name, 'wb')
    for i in range (0, 20):
        alignment = model.alignment = model.align(aligned_sents[i])
        my_file.write(str(alignment.words) + '\n')
        my_file.write(str(alignment.mots) + '\n')
        my_file.write(str(alignment.alignment) + '\n\n')

        # Below is for testing, does not go into file
        # Globals are used with compare_models()
        if file_name == "ibm1.txt":
            one_error.append(alignment.alignment_error_rate(aligned_sents[i]))
        else:
            two_error.append(alignment.alignment_error_rate(aligned_sents[i]))
        # Just used to test and compare
        print 'Error Rate ' + str(i + 1) + ': ' + str(alignment.alignment_error_rate(aligned_sents[i]))
    print ''
    my_file.close()

# This function is used just for the grading rubric - to see which sentences are better for which models
# With this, we can see which sentences do better for which
def compare_models():
    for i in range (0, 20):
        if one_error[i] < two_error[i]:
            print 'Sentence ' + str(i + 1) + ' is better for Model 1'
            print one_error[i]
            print two_error[i]
        if two_error[i] < one_error[i]:
            print 'Sentence ' + str(i + 1) + ' is better for Model 2'
            print one_error[i]
            print two_error[i]

def main(aligned_sents):
    t0 = time.time()
    print 'Starting A1'
    ibm1 = create_ibm1(aligned_sents)
    save_model_output(aligned_sents, ibm1, "ibm1.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm1, 50)

    print ('IBM Model 1')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
    tA = time.time()
    print 'A1 Time: ' + str(tA - t0)

    print 'Starting A2'
    ibm2 = create_ibm2(aligned_sents)
    save_model_output(aligned_sents, ibm2, "ibm2.txt")
    avg_aer = compute_avg_aer(aligned_sents, ibm2, 50)
    
    print ('IBM Model 2')
    print ('---------------------------')
    print('Average AER: {0:.3f}\n'.format(avg_aer))
    tB = time.time()
    print 'A2 Time: ' + str(tB - tA)
    print 'Total A Time: ' + str(tB - t0)

    # use this function just for testing
    #compare_models()