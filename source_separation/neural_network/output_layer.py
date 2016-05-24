# -*- coding: utf-8 -*-
from keras import backend as K
from keras.engine.topology import Layer
import numpy as np
import theano.tensor as T

class Output_Layer(Layer):
    def __init__(self, output_dim, **kwargs):
        '''
            Initialize the final layer of the network

            :param init_sft: The initial STF of the noisy signal, with length 1024
        '''
        self.output_dim = output_dim
        self.update = []
        self.params = []
        super(Output_Layer, self).__init__(**kwargs)

    def build(self, input_shape):
        self.input_dim = input_shape[1]
        if self.output_dim != self.input_dim:
            raise Exception('OUTPUT LAYER ERROR: input/output dimension mismatch: ' + str(self.output_dim) + ' / ' + str(self.input_dim))
        self.trainable_weights = []

    def call(self, y, mask=None):
        '''
            parameter y is supposed to have twice the length of the STF
        '''
        # Compute mask
        y1, y2 = T.split(K.transpose(y), [16, 16], 2, axis=0)

        mask1 = K.abs(y1) / (K.abs(y1) + K.abs(y2))
        mask2 = K.abs(y2) / (K.abs(y1) + K.abs(y2))
        mask = K.concatenate([mask1, mask2])

        # Apply mask
        out = K.dot(y, mask.flatten().T)
        print "out !!"
        return out

    def get_output_shape_for(self, input_shape):
        return (self.output_dim, self.output_dim) 
