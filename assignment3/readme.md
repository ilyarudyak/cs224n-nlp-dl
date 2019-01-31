## q1
### (a) (i)
Provide 2 examples of sentences containing a named entity with an ambiguous type
(e.g. the entity could either be a person or an organization, or it could either be an organization
or not an entity).
- *Ford Motor Corp.* - name of a corporation (`ORG`), but *Ford* can be 
a name of a person (`PER`);
- *Berkshire Hathaway INC.* - again, *Hathaway* can be name of 
*Anne Hathaway* (`PER`), not name of a corporation (`ORG`);
- actually we have such an example in the assignment: 
*American Airlines, a unit ...*; *American* is labelled as `MISC`, but 
it should be `ORG`;
### (a) (ii)
Why might it be important to use features apart from the word itself to predict
named entity labels?
- from previous examples it's obvious that we have to use context, not only the
word itself; so we have to use window, not word itself;
### (a) (iii)
Describe at least two features (apart from the word) that would help in predicting
whether a word is part of a named entity or not.
- in case of `ORG` we may search for *INC.*, *Corp.* etc.;
- in case of location we may check if there's a name of the country;
- in case of name there can be title: *spokesman Tim Wagner said* (here's title - 
*spokesman*);
### (b) (i)
What are the dimensions of `e(t), W and U` if we use a window of size w?
- `e(t)` is concatenation (not matrix) of embedded vectors each of size `D`;
size of the window is `w`, so we have size of `e(t)`: `(2*w+1)*D`;
- we multiply `e(t)` on the left (as a raw vector), so `W` has shape: `((2*w+1)*D, H)`; 
- again, we multiply `h(t)` from the left, so `U` has shape: `(H, C)`;
### (b) (ii)
- skipped;
### (d) (i)
Report your best development entity-level `F1` score and the corresponding 
token-level confusion matrix. Briefly describe what the confusion matrix tells 
you about the errors your model is making.
- Epoch 10 out of 10: Entity level `P/R/F1: 0.81/0.85/0.83`
- Token-level confusion matrix is below. 

|gold\guess |PER     	|ORG     	|LOC     	|MISC    	|O       |
|-----------|-----------|-----------|-----------|-----------|--------|
|PER     	|2962.00 	|51.00   	|71.00   	|12.00   	|53.00   |
|ORG     	|128.00  	|1679.00 	|122.00  	|51.00   	|112.00  |
|LOC     	|51.00   	|128.00  	|1857.00 	|21.00   	|37.00   |
|MISC    	|44.00   	|68.00   	|55.00   	|993.00  	|108.00  | 
|O       	|49.00   	|59.00   	|17.00   	|31.00   	|42603.00|

- Token-level scores. So we may see that we have some problems with `ORG`.
Most `FP` goes to `LOC` (so we mark an entity as `ORG` but this is actually
`LOC`), most `FN` goes to `PER` (so we missed those entities and mark them 
incorrectly as a `PER`). That's not surprising: many organizations contain 
geographical locations and names. We have 122 `FP` for `LOC` that are actually 
`ORG`. 

|label  |acc  	|prec 	|rec  	|f1  |
|-------|-------|-------|-------|----| 
|PER    |0.99 	|0.92 	|0.94 	|0.93| 
|ORG    |0.99 	|0.85 	|0.80 	|0.82| 
|LOC    |0.99 	|0.88 	|0.89 	|0.88| 
|MISC   |0.99 	|0.90 	|0.78 	|0.84| 

### (d) (ii)
Describe at least 2 modeling limitations of the window-based model and support these conclusions using 
examples from your model’s output (i.e. identify errors that your model made due to its limitations). 
You can also support your conclusions using predictions made by your model on examples manually entered 
through the shell.
- The model can't use previous context (in equations it uses only window, not previous hidden state):
x : author focusing on the impact of artificial intelligence and robotics on society and the economy Ford 
y*:                                                                                                       
y': O      O        O  O   O      O  O          O            O   O        O  O       O   O   O       ORG

x : author focusing on the impact of artificial intelligence and robotics on society and the economy Martin Ford 
y*:                                                                                                              
y': O      O        O  O   O      O  O          O            O   O        O  O       O   O   O       PER    PER
- The model doesn't look into the future as well (we need biRNN):
x : SQUASH - HONG KONG OPEN QUARTER-FINAL RESULTS . 
y*: O      O MISC MISC MISC O             O       O 
y': O      O LOC  MISC MISC O             O       O 
x : HONG KONG 1996-08-30 
y*: LOC  LOC  O          
y': LOC  LOC  O 
## q2
### (a) (i)
How many more parameters does the RNN model in comparison 
to the window-based model?
- In the window-based model we have matrix `W` with dimensions `((2w+1)D, H)`;
here we have 2 matrices: `Wh` with shape `(H, H)` and `We` with shape `(D, H)`;
### (a) (ii)
What is the computational complexity of predicting labels for a sentence of length T 
(for the RNN model)?
- skipped;
### (b) (i)
Name at least one scenario in which decreasing the cross-entropy cost would lead to
an decrease in *entity-level* F1 scores.
**--TODO**
### (b) (ii)
Why it is difficult to directly optimize for F1?
- there's now way we may train network with an arbitrary loss function;
cross entropy is quite unique and it requires token-level compares;
### (d) (i)
How would the loss and gradient updates change if we did not use masking? 
How does masking solve this problem?
- Well, we increase `y` by dummy `NULL` labels; and without mask we account 
for their correct or incorrect prediction, and that's not our goal;
### (g) (i) (ii)
Describe at least 2 modeling limitations of this RNN model and support these con-
clusions using examples from your model’s output. For each limitation, suggest some 
way you could extend the model to overcome the limitation.
- Well, this model still has at least one limitation in common with the previous model:
it can't see into the future.


