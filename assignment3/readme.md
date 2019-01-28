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