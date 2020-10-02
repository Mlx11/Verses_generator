# Verses_generator
A school project to create repetitive verses of french songs

## Assumptions
The following assumptions were taken: 

 - All verses are equally structured
 - Cross references are linear (a part of a verse n is equal to one in verse n+k with k being constante)
 - Growing verse length is possible if the verse grows always by the element new to the verse n-1. More complex growing behaviour is not possible

## Template Style
The template syntax for a verse contains three elements:
 1. {i} - This gets replaced by the i-th string given to the verse
 2. {:n some text :} - Repetition. Everything after the space following "{:n" and before the space in front of ":}" gets repeated n times. There's no automatic line break after each repetition (use {:n text \n:} to force one)
 3. {[sep]} - This gets replaced by all strings given to the verse separated by "sep".

Example:

    All starts with {1}
    {:2 {[\n]} :}
  with the arguments ("a", "b") creates the verse
  

> All starts with a
> a
> b
> a
> b

## Crosslinking
Crosslinking is used to refere to a phrase used in an other verse. The information is stored in a dictionary containing the elements

 1. from_verse - the relative position of the verse the phrase is taken from (ex. -1 for the verse before)
 2. from_vers_pos - The position where the phrase is taken from inside the tupple specified by from_verse. A zero takes all phrases in that tupple. 
 3. insert_as - specifies at which position the phrase taken should be. If there's already a string at this position no actions will be taken. This is especially useful to solve situations where a certain phrase does not refere to other verses like all the others do (mostly first or last verse)
