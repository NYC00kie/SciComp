# simsimsim_toxicity

<script
  src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML"
  type="text/javascript">
</script>


Lets create a modell that models the population of yeast in a Alcohol producing enviornment.
The Yeast itself produces the alcohol and in turn after some point should kill itself.

I am thinking about modeling this with a compartment model.
The Compartments would be Alive(A), Dead(D) and Alcohol concentration(C).

A would be initialised with a certain number.
D would be initialised with 0
C would be initialised with 0

an Equation could look like this:

$\beta$: normal death rate

$\gamma$: alcohol production rate

$\lambda$: resistance factor

$$
\begin{align}
  \tag{1}
  \dv{A}{t} &= - (\beta \cdot A + \frac{e^C \cdot A}{\lambda} )\\
  \tag{2}
  \dv{C}{t} &= \gamma \cdot A \\
  \tag{3}
  \dv{D}{t} &= \beta \cdot A + \frac{e^C \cdot A}{\lambda} 
\end{align}
$$

