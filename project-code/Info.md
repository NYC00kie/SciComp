# General

In diesem Ordner wird die Codebase des Projects sein.

Dont use the Cuda, its ass and fucking slow, I dont know why.


# Probleme

## GPU

Bei der Implementation des Diffusions Algorithmus in Cuda mithilfe von numba gibt es ein Problem dabei mehrere Threads oder mehrere Blöcke (mehr Blöcke sind schlechter als mehr Threads, wie rausgefunden wurde.) zu benutzten, da an den Rändern der Blöcke eine Deadzone vorkommt, wo sich speicherzonen von einem Block und dem anderen überlappen und am Ende überschreiben. Bei Threads kommt es dazu, das diese Inerhalb der Blöcke sich gegenseitig überschreiben.

Für die Threads gäbe es eine Lösung, und zwar, dass man den vom Block zu bearbeitenden Daten Bereich in Shared Memory legt (nur für Threads, es gibt scheinbar kein Shared Memory zwischen Blöcken ) und in diesem Arbeitet, da dieser zwischen Threads geteilt wird.

### Solution
Das ist die Lösung, es wird in einem Block atomic added zum shared Memory, so können alle Blöcke ihren Bereich gleichzeitig berechnen und danach addiert der aller erste Thread ins grid_out


# Ideen

Implement the Diffusion for every Element (Glucose, Oxygen) for a seperate thread so that they can all run in parallel.

# Endlösung

We from now on will use convolution to do the diffusion