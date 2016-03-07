John Fulgoni
Homework 2
README.txt

1) Dependency Graphs
A projective sentence is where the parse tree has no crossing dependencies.
To determine if the graph is projective, you first add an arc where the child index is less than the parent index.
Then, you check the indices of arcs within the index range of the child and parent.
If any node has an arc that connects to an index less than the child, or greater than the parent, then graph is non-projective, since the dependencies must cross.

Projective Sentence:
John will continue teaching the class.

Non-Projective Sentence:
A game was played today between the Mets and Blue Jays.

____________________________________________
2) Bad Features
Results:

Starting Bad Features
Bad Features Results
UAS: 0.229038040231 
LAS: 0.125473013344
Time: 74.7035279274

The performance of this parser means that 22% of the words were matched with the correct head,and that only 12.5% were matched with the correct head and dependency label.
This means that the features that were chosen are poor measures of sentence dependency.

_______________________________________________
3) Feature Extractor

I added features first based on the chart provided in Table 3.2 on page 31 of:
http://books.google.com/books/about/Dependency_Parsing.html?id=k3iiup7HB9UC

I chose to add all features with a positive attribute for Stack 0 and 1, as well as Buffer 0 and 1.
Which included the Lemma, Tag, and Ctag where appropriate

Features I've added (Parentheses were given at the start):
Stack 0: (Form), Lemma, Tag, Ctag, (Feats, Ldep, Rdep)
Stack 1: Ctag
Buffer 0: (Form), Lemma, Tag, Ctag, (Feats, Ldep, Rdep)
Buffer 1: Form, Ctag

Complexities:
Form, Lemma, Tag, Ctag = O(1), since we just look up the results in the 'token' list
Ldep, Rdep = O(n), since it has to go through the list of arcs for a given index
Feats = O(k), with accessing it being O(1) since it's in tokens, but we have to look and add each individual feature after we split it.

Results:
The results for all three languages significantly increase the accuracy of the UAS and LAS.
What I believe had the biggest impact was appending the Tag and Ctag features.
Adding the Lemma got the LAS up to about 20%, but adding Tag and Ctag brought it all the way up to 60.
I then added the Ctag features for Stack 1 and Buffer 1, and the form for Buffer 1, and that brought Swedish over 67%.

Starting Swedish
 Number of training examples : 200
 Number of valid (projective) examples : 180
Training support vector machine...
done!
Swedish Results
UAS: 0.798247361083 
LAS: 0.684923322047
Time: 133.456676006

Starting English
 Number of training examples : 200
 Number of valid (projective) examples : 200
Training support vector machine...
done!
English Results
UAS: 0.808176100629 
LAS: 0.745283018868
Time: 83.4556910992

Starting Danish
 Number of training examples : 200
 Number of valid (projective) examples : 174
Training support vector machine...
done!
Danish Results
UAS: 0.803992015968 
LAS: 0.727145708583
Time: 88.6158938408

Arc-Eager Parser:
The arc-eager parser has a complexity of O(n), since it operates on all the words in a sentence, and passes through only once.
The parser will only operate on sentences that are projective, because if the sentence is deemed non-projective, then it will not work.


4) Parse Script
Still struggling to get a proper parse tree using this.
Not sure what I'm doing wrong. When I hover over a word in the editor, I can see a TAG and CPOS, which appear to be correct.
