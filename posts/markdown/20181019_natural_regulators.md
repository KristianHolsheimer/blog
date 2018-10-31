# A Natural Interpretation of Regularization Terms

On this blog, I share cute insights and little nuggets of wisdom that I stumble
upon in my work as a data scientist. I have a pretty solid background in
mathematics and such, but my knowledge and education on the topic of statistics
and machine learning has been much less structured. I learn by collecting these
little insights. Therefore, I though it'd be nice to share these insights with
you.



In this post I'd like to share a little thing I just realized, giving a very
natural interpretation to L2 regularization. I hope you enjoy it as much as I
just did.


## Context

Let's set up the proper context. Suppose we're doing plain-vanilla supervised
learning. That is, we're interested in finding out a way to map inputs $x$ to
outputs $y$. Since the class of such mappings infinite, we restrict the class
to those parametrized by some finite set of parameters $\theta$, i.e.

$$
    f_\theta:\ X\to Y
$$

where $X$ and $Y$ are the space of inputs and outputs, respectively. Let's
denote the labeled data set as

$$
    D\ =\ X\odot Y\ =\ \lbrace(x, y)\ |\ x\in X,\ y\in Y\rbrace
$$

The way I see it, we would like to find the parameters $\theta$ that maximize

\begin{align}
    P(\theta|D)\ =\ \prod_i\ P(\theta|x_i,y_i)
\end{align}

Or equivalently,

\begin{align}
    \log P(\theta|D)\ &=\ \sum_i\ \log P(\theta|x_i,y_i)
\end{align}

Notice that it doesn't matter whether we maximize $P(\theta|D)$ or $\log
P(\theta|D)$, since the logarithm is a monotone function. Using Bayes' rule, we
have

\begin{align}
    P(\theta|D)\ &=\ \frac{P(D|\theta)\ P(\theta)}{P(D)}
\end{align}

or in log-space,

\begin{align}
    \log P(\theta|D)\ &=\ \log P(D|\theta) + \log P(\theta) - \log P(D)
\end{align}

Thus, the optimal set of parameters $\theta_*$ would be:

\begin{align}
    \theta_*\ &=\ \arg\max_\theta\ P(\theta|D) \newline
    &=\ \arg\max_\theta\ \log P(\theta|D) \newline
    &=\ \arg\max_\theta\ \log P(D|\theta) + \log P(\theta)
\end{align}

This general case is known as *Maximum A Posteriori Estimation* (MAP). A very
common choice for the prior $P(\theta)$ is to take a uniform distribution. In
other words, $P(\theta)$ will be **independent of $\theta$**, such that it
drops out of the argmax. Thus the specific case of a uniform $\theta$ prior,
the MAP optimization problem reduces to *Maximum Likelihood Estimation* (MLE):

\begin{align}
    \theta_*\ &=\ \arg\max_\theta\ \log P(D|\theta)
\end{align}


## A Simple Example: Linear Regression

Let's take a specific type of model class. We'll look at the simplest model to
illustrate what's going here: *linear regression*, for which $f_\theta(x) =
\theta\cdot x$. The likelihood is presumed to be a Gaussian:

\begin{align}
    P(D|\theta)\ \propto\ \prod_i\ \exp\left(-\frac{(\theta\cdot x_i - y_i)^2}{2\sigma^2}\right)
\end{align}

Which means that the MLE optimal parameters for linear regression are (omitting
the overall factor $1/\sigma^2$ as it's independent of $\theta$):

\begin{align}
    \theta_*\ &=\ \arg\max_\theta\ \log P(D|\theta)\ =\ \arg\min_\theta\ \sum_i\ \frac12(\theta\cdot x_i - y_i)^2
\end{align}

We have thus recovered our ordinary least squares loss function as the negative
log-likelihood of a Gaussian likelihood function.


## L2 Regularization = Gaussian Prior

The L2 regulator is often introduced as follows.

*We start with a loss function $\sum_i(\theta\cdot x_i - y_i)^2$ and then we
add a regulator $\|\theta\|^2$. Why, you ask? Well because it has all of these
nice properties ... bla bla bla ...*

Although not wrong, it's not very intuitive. I was therefore delighted to find
that there is actually a very natural way in which this term comes about.
Recall that we chose a uniform prior $P(\theta)$. What would happen if we would
choose something else? A Gaussian prior, I hear you say? Sure, let's take a
(multivariate) Gaussian prior, e.g. $\mathcal{N}(\mathbf{0},
\lambda^{-1}\mathbb{I})$, such that

\begin{align}
    P(\theta)\ \propto\ \exp\left( -\frac{\lambda}{2}\ \Vert\theta\Vert^2 \right)
\end{align}

Then, the log-likelihood is no longer the only term in the MAP optimization:

\begin{align}
    \theta_*\ &=\ \arg\max_\theta\ \log P(D|\theta) + \log P(\theta) \newline
    &=\ \arg\max_\theta\ \log P(D|\theta) - \frac{\lambda}{2}\ \Vert\theta\Vert^2
\end{align}

Isn't that nice? As it turns out, adding a L2 regulator is merely a method for
feeding in a Gaussian prior on your model parameters $\theta$. Note that this
prior is typically centered around the origin, but doesn't have to be the case.
For example, in the FRTL-proximal algorithm, the prior is updated in such a way
that it is always centered around the current best estimate of $\theta_*$.


## How did I stumble upon this?

I was reading this nice paper on Variational Auto-Encoders
[[ArXiv:1312.6114](https://arxiv.org/abs/1312.6114)] and I realized that I was
always a bit confused about the difference between *Maximum Likelihood
Estimation* and *Maximum A Posteriori Estimation*, so I decided to have another
look at it before reading on. I learned that the regularization term in the
loss function can have a highly non-trivial form. In fact, there's very little
chance anyone would've come up with the VAE regulator if it weren't derived
from a Bayesian viewpoint (similar to what we did in this post).

