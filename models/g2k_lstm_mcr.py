# import torch
import torch.nn as nn
import tensorflow as tf
import numpy as np
# import tensorflow.gra as grad
import nri_learned as nri
import networkx_graph as nx
from torch.nn import functional as F
import torch.cuda


class g2k_lstm_mcr():
    def __init__(self, in_features, out_size, obs_len, num_nodes, lambda_reg):
        # super(g2k_lstm_mcr).__init__()
        # self.relu = tf.nn.relu_layer()
        self.out_size = num_nodes
        self.lambda_reg = tf.Variable(lambda_reg, dtype=tf.float64)
        self.init_w = tf.initializers.random_normal(mean=0, stddev=1, seed=0, dtype=tf.float64)

        self.outputs = tf.placeholder_with_default(input=tf.random.normal(shape=[int(in_features.shape[0])+2,
                                             int(in_features.shape[0])],
                                               mean=0, stddev=1, seed=0, dtype=tf.float64),#dtype=tf.float64,
                                      shape=[int(in_features.shape[0])+2,
                                             int(in_features.shape[0])],name="outputs")
        self.ngh = tf.placeholder_with_default(input=tf.random.normal(shape=[int(in_features.shape[0]), int(in_features.shape[0])],
                                               mean=0, stddev=1, seed=0, dtype=tf.float64),
                                               shape=[int(in_features.shape[0]), int(in_features.shape[0])], name="ngh")

        self.visual_path = tf.placeholder_with_default(input=tf.random.normal(shape=[1, int(in_features.shape[0])],
                                               mean=0, stddev=1, seed=0, dtype=tf.float64), #dtype=tf.float64,
                                          shape=[1, in_features.shape[0]], name="visual_path")

        self.pred_path_band = tf.placeholder_with_default(input=tf.random.normal(shape=[2,8,num_nodes],
                                               mean=0, stddev=1, seed=0, dtype=tf.float64), #dtype=tf.float64,
                                             shape=[2,8,num_nodes], name="pred_path_band")

        # self.bias_k = tf.Variable(name='bias_k', initial_value= \
        #                           self.init_w(shape=(in_features.shape[0],)),
        #                           # shape=(in_features.shape[1].value, 1),
        #                           dtype=tf.float64)



        with tf.variable_scope("krnl_weights"):
            self.weight_v = tf.Variable(name='weight_v', initial_value= \
                                        self.init_w(shape=(8, int(in_features.shape[0]) + 2)),
                                        # shape=tf.shape(1,in_features.shape[1].value),
                                        dtype=tf.float64)

            self.bias_v = tf.Variable(name='bias_v', initial_value= \
                                      self.init_w(shape=(int(in_features.shape[0]),)),
                                      # shape=tf.shape(1,in_features.shape[1].value),
                                      dtype=tf.float64)

            self.weight_o = tf.Variable(name='weight_o', initial_value= \
                                        self.init_w(shape=(int(in_features.shape[0]), num_nodes)),
                                        # shape=tf.shape(1,in_features.shape[1].value),
                                        dtype=tf.float64)

            self.weight_c = tf.Variable(name='weight_c', initial_value= \
                                        self.init_w(shape=(16, obs_len)),
                                        # shape=tf.shape(1,in_features.shape[1].value),
                                        dtype=tf.float64)

        self.forward()
        # self.pred_path, self.cost = self.forward()
        # self.pred_path, self.cost = self.forward(self.outputs,self.ngh, self.visual_path)
        # def randomWalker(self, in_features, w, b):
        #
        #     # random walks with restarts to estimate pedestrians proximecs.
        #     # consider lars et al. 2011 Supervised
        #     # weighted random walker (use hard-attention mechanism that relies on VFOA)
        #     # kernel = random_walk ...
        #     return

    def forward(self):
        # st_graph = nodes
        # pred_path_band = self.randomWalker(graph=st_graph, edges_mat=edges)
        # embedded_spatial_vislet = tf.nn.relu(tf.nn.xw_plus_b(self.visual_path, self.weight_v, self.bias_v))

        embedded_spatial_vislet = tf.Variable(tf.matmul(self.weight_v, self.outputs) + self.bias_v) # 8x10
        # ngh_temp = tf.Variable((self.lambda_reg * self.ngh) )# 8x10
        ngh_temp = tf.Variable(tf.matmul(embedded_spatial_vislet , self.ngh))
        self.cost = tf.gradients(ys=ngh_temp, xs=embedded_spatial_vislet, unconnected_gradients='zero')
        self.cost = tf.squeeze(self.cost)
        self.cost = tf.nn.relu(self.cost)

        self.temp_path = tf.Variable(tf.matmul(self.weight_c, self.cost))  # 16x10
        self.temp_path = tf.Variable(tf.matmul(self.temp_path, self.weight_o))  # 16xn

        self.pred_path_band = tf.reshape(self.temp_path, (2, 8, self.out_size))  # 2x8xn
        # ngh = tf.Variable(initial_value=tf.multiply(embedded_spatial_vislet, ngh),
        #                   trainable=True,
        #                   name='ngh')
        # self.mlp()
        # with tf.GradientTape() as t:
        #     t.watch(outputs)
        #     # out = f(outputs, ngh)
        # return t.gradient(outputs, ngh)
        # pred_path_band = grad.jacobian(output=outputs, inputs=ngh)
        # d_outputs need to be square matrix (positive-definite) NOT necessary
        # convex loss
        # Jacobian is the following m × n matrix
        # compute neighborhood as a function of the social and spatial features
        # determined by social embedded features.
        # ys_temp = tf.zeros_like(self.ngh)


        # self.cost = tf.transpose(self.cost)
        # self.cost = tf.matmul(self.ngh, self.outputs)



        # pred_path_band = tf.matmul(self.weight_k, tf.squeeze(self.cost)) + self.bias_k
        # pred_path_band = tf.nn.xw_plus_b(x=tf.transpose(d_outputs), weights=self.weight_k, biases=self.bias_k)
        # estimate gradient of every pedestrian function using Jacobian (matrix calculus).
        # return self.pred_path_band, self.cost
        # return np.array(pred_path_band), np.array(d_outputs)

    def backward(self):
        return

    def register_backward_hook(self, hook):
        return





