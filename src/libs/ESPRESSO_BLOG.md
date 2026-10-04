
Original blog post from:

* https://chmod755.tumblr.com/post/31417234230/espresso-heuristic-logic-minimizer

# Espresso Heuristic Logic Minimizer

I bundled up the old espresso program from 1989 and repackaged it. This thing took me a while to find, so I figured I’d post it incase anyone else searching for it could find it a bit easier. It is bundled with the original manpages and examples.  This program got me through 2 semesters of digital design. The example is from a project to design the logic behind a 4-way stoplight.

USAGE:

Format truth table to include:

- .i = number of inputs
- .o = number of outputs
- .ilb = input names
- .ob = output names 

Example:

```
~$ cat input.tt

# Truth Table for Stoplight FSM
.i 14
.o 11

.ilb NS ES turn NSR NSY NSG EWR EWY EWG TR TY TG dir0 dir1
.ob NSR NSY NSG EWR EWY EWG TR TY TG dir0 dir1

000--1--------01000000000
000-----1-----00001000001
000--------1--00000001010
001--1--------01000000001
001-----1-----00001000001
001--------1--00000001001
010--1--------01000000000
010-----1-----00001000000
010--------1--00000001000
011--1--------01000000000
011-----1-----00001000001
011--------1--00000001000
100--1--------01000000010
100-----1-----00001000010
100--------1--00000001010
101--1--------01000000001
101-----1-----00001000001
101--------1--00000001010
110--1--------01000000000
110-----1-----00001000010
110--------1--00000001010
111--1--------01000000000
111-----1-----00001000001
111--------1--00000001010
----1-------0010010010000
----1-------0110010010001
----1-------1010010010010
-------1----0010010010000
-------1----0110010010001
-------1----1010010010010
----------1-0010010010000
----------1-0110010010001
----------1-1010010010010
---1--1--1--0000000100000
---1--1--1--0100000000101
---1--1--1--1000100000010
.e
```

```
~$ espresso -o eqntott input.tt
NSR = (TY&!dir0&dir1) | (EWY&!dir0&dir1) | (NSY&!dir0&dir1) | (TY&!dir1) | (
    EWY&!dir1) | (NSY&!dir1);

NSY = (NSG);

NSG = (NSR&EWR&TR&dir0&!dir1);

EWR = (TY&!dir0&dir1) | (EWY&!dir0&dir1) | (NSY&!dir0&dir1) | (TY&!dir1) | (
    EWY&!dir1) | (NSY&!dir1);

EWY = (EWG);

EWG = (NSR&EWR&TR&!dir0&!dir1);

TR = (TY&!dir0&dir1) | (EWY&!dir0&dir1) | (NSY&!dir0&dir1) | (TY&!dir1) | (
    EWY&!dir1) | (NSY&!dir1);

TY = (TG);

TG = (NSR&EWR&TR&!dir0&dir1);

dir0 = (NSR&EWR&TR&dir0&!dir1) | (NS&!ES&!turn&NSG) | (NS&!turn&EWG) | (
    !ES&!turn&TG) | (TY&dir0&!dir1) | (EWY&dir0&!dir1) | (NSY&dir0&!dir1) | (
    NS&TG);

dir1 = (NSR&EWR&TR&!dir0&dir1) | (!NS&!ES&turn&TG) | (!NS&!ES&EWG) | (!ES
    &turn&NSG) | (turn&EWG) | (TY&!dir0&dir1) | (EWY&!dir0&dir1) | (NSY
    &!dir0&dir1);
```

And VOILA! Simplified boolean expressions.

To install, simply run the INSTALL script, or look through this script to do it yourself. Make sure to make the script executable by running

    chmod 755 INSTALL