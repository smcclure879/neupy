import copy

import numpy as np

from neuralpy.core.properties import NonNegativeNumberProperty
from .backpropagation import Backpropagation


__all__ = ('Quickprop',)


class Quickprop(Backpropagation):
    """ Quickprop :network:`Backpropagation` algorithm optimization.

    Parameters
    ----------
    upper_bound : float
        Maximum possible value for weight update. Defaults to ``1``.
    {optimizations}
    {raw_predict_param}
    {full_params}

    Methods
    -------
    {supervised_train}
    {full_methods}

    Examples
    --------
    Simple example

    >>> import numpy as np
    >>> from neuralpy import algorithms
    >>>
    >>> x_train = np.array([[1, 2], [3, 4]])
    >>> y_train = np.array([[1], [0]])
    >>>
    >>> qpnet = algorithms.Quickprop(
    ...     (2, 3, 1),
    ...     verbose=False
    ... )
    >>> qpnet.train(x_train, y_train)

    See Also
    --------
    :network:`Backpropagation` : Backpropagation algorithm.
    """
    upper_bound = NonNegativeNumberProperty(default=1)

    def layer_weight_update(self, delta, layer_number):
        if not hasattr(self, 'prev_gradients'):
            weight_delta = self.gradients[layer_number]
        else:
            gradient = self.gradients[layer_number]
            prev_gradient = self.prev_gradients[layer_number]
            prev_weight_delta = self.prev_weight_deltas[layer_number]
            weight_delta = prev_weight_delta * (
                gradient / (prev_gradient - gradient)
            )
            upper_bound = self.upper_bound
            weight_delta = np.where(
                weight_delta < upper_bound, weight_delta, upper_bound
            )

        self.weight_deltas.append(weight_delta)
        return weight_delta

    def update_weights(self, weight_deltas):
        self.weight_deltas = []
        super(Quickprop, self).update_weights(weight_deltas)

        self.prev_weight_deltas = copy.copy(self.weight_deltas)
        self.prev_gradients = copy.copy(self.gradients)