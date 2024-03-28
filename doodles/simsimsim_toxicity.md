# simsimsim_toxicity

## No Research done - just an IDEA
Lets create a modell that models the population of yeast in a Alcohol producing enviornment.
The Yeast itself produces the alcohol and in turn after some point should kill itself.

I am thinking about modeling this with a compartment model.
The Compartments would be Alive(A), Dead(D) and Alcohol concentration(C).

A would be initialised with the population number.

D would be initialised with 0.

C would be initialised with 0.

an Equation could look like this:

$\beta$: normal death rate

$\gamma$: alcohol production rate

$\lambda$: resistance factor

$$
\begin{align}
  \frac{d A}{d t} &= - (\frac{\beta \cdot A}{n} + \frac{e^{\sqrt{C}} \cdot A}{\lambda} )\\
  \frac{d C}{d t} &= \gamma \cdot A \\
  \frac{d D}{d t} &= \frac{\beta \cdot A}{n} + \frac{e^{\sqrt{C}} \cdot A}{\lambda} )
\end{align}
$$

