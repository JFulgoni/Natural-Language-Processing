John Fulgoni
UNI: jsf2154
Homework 4 README

Part A Time: ~3 minutes
(with 10 iterations)
Part B Time: ~3 minutes
Total Time: ~6 minutes

=============================
Part A Results:

With 10 Iterations:
Starting A1
IBM Model 1
---------------------------
Average AER: 0.665

A1 Time: 43.1826610565
Starting A2
IBM Model 2
---------------------------
Average AER: 0.650

A2 Time: 128.168908119
Total A Time: 171.351569176

---------------------------
Comparison Results:

Sentence 5 is better for Model 2
IBM1: 0.75
IBM2: 0.666666666667

Sentence 5:
[u'Ich', u'bitte', u'Sie', u',', u'sich', u'zu', u'einer', u'Schweigeminute', u'zu', u'erheben', u'.']
[u'Please', u'rise', u',', u'then', u',', u'for', u'this', u'minute', u"'", u's', u'silence', u'.']
IBM1: 0-1 1-1 2-1 3-4 4-10 5-10 6-10 7-10 8-10 9-1
IBM2: 0-0 1-1 2-0 3-2 4-10 5-10 6-10 7-7 8-10 9-0

Sentence 14 is better for Model 1
IBM1: 0.674418604651
IBM2: 0.720930232558

Sentence 14:
[u'Meine', u'Frage', u'betrifft', u'eine', u'Angelegenheit', u',', u'die', u'am', u'Donnerstag', u'zur', u'Sprache', u'kommen', u'wird', u'und', u'auf', u'die', u'ich', u'dann', u'erneut', u'verweisen', u'werde', u'.']
[u'My', u'question', u'relates', u'to', u'something', u'that', u'will', u'come', u'up', u'on', u'Thursday', u'and', u'which', u'I', u'will', u'then', u'raise', u'again', u'.']
IBM1: 0-0 1-16 2-4 3-7 4-2 5-3 6-12 7-10 8-10 9-8 10-2 11-2 12-14 13-11 14-9 15-12 16-13 17-15 18-2 19-2 20-2
IBM2: 0-0 1-16 2-4 3-7 4-2 5-3 6-12 7-17 8-10 9-8 10-2 11-2 12-14 13-11 14-9 15-12 16-13 17-15 18-2 19-2 20-2

Overall, IBM2 performs 1.5% better than IBM1 using 10 iterations.
This is most likely due to the fact that IBM2 includes the distortion in its calculations, while IBM1 does not.

----------------------------
Finding Converge with Training Iterations:

					Number of Iterations
		1		3		5		10		15		20		25		30
IBM1	0.873	0.641	0.627	0.665	0.665	0.661	0.660	0.660

IBM2	0.646	0.644	0.644	0.650	0.650	0.648	0.649	0.649

Naturally, with more iterations, the programs takes more and more time to run.
IBM1 seems to have its best accuracy somewhere between 3 and 10, and appears to converge around 25-30 iterations.
For the best results for accuracy and time, IBM1 should have somewhere between 1 - 5 iterations.
IBM2 sems to have its best accuracy from 3 to 5, and appears to roughly converge at 25, although there is minimal change from 10 iterations.
Overall, for the best results for accuracy and time, IBM2 should run somewhere between 3 and 5 iterations.

=================================
Part B Results:

For this part of the assignment, I followed along with the pydoc documentation of IBM2.
URL: http://pydoc.net/Python/nltk/3.0.1/nltk.align.ibm2/

Berkeley Aligner
---------------------------
Average AER: 0.593

Total B Time: 170.249657869

I could not get the Berkeley Aligner working with a much greater accuracy than the IBM2 Model.
I chose to leave out any changes to the distortion (q) parameters after the initialization, as it gave a better accuracy.
With the alignment parameters computed, the accuracy of the system was 0.642, which is not much better than IBM2.
Still, it shows that averaging the errors from English to German and German to English is better than simply going in the forwards direction.

Sentence 7 is better for the Berkeley Aligner than both the IBM1 Models and the IBM2 Models.

IBM1: 0.571428571429
IBM2: 0.571428571429
Berkeley: 0.466666666667

Sentence 7:
[u'Frau', u'Pr\xe4sidentin', u',', u'zur', u'Gesch\xe4ftsordnung', u'.']
[u'Madam', u'President', u',', u'on', u'a', u'point', u'of', u'order', u'.']
IBM1: 0-0 1-0 2-2 3-7 4-7
IBM2: 0-0 1-0 2-2 3-5 4-7
Berkeley: 0-1 1-0 2-2 3-3 4-7 5-8