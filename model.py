import numpy as np
import tensorflow as tf


class CustomConv2D(tf.keras.layers.Conv2D):
    def __init__(self, *args, mask=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.mask = mask

    def build(self, input_shape):
        result = super().build(input_shape)
        self.applyMask()
        return result

    def applyMask(self):
        # I believe this doesn't affect efficiency very much.
        for x, y in self.mask:
            self.kernel[x, y, :, :].assign(tf.zeros_like(self.kernel[x, y, :, :]))


class CustomModel(tf.keras.Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conv1 = CustomConv2D(1, (3, 3), mask=[[0, 2], [2, 0]], padding="same")
        self.conv2 = tf.keras.layers.Conv2D(1, (3, 3), padding="same")
        self.flatten = tf.keras.layers.Flatten()
        self.dense = tf.keras.layers.Dense(10, activation="softmax")

    def call(self, inputs):
        x = self.conv1(inputs)
        x = self.conv2(x)
        x = self.flatten(x)
        x = self.dense(x)
        return x

    def train_step(self, data):
        # When training, apply the mask to the weights after each training step.
        result = super().train_step(data)
        for layer in self.layers:
            if isinstance(layer, CustomConv2D):
                layer.applyMask()
        return result


class Network:
    def __new__(cls, cfg):
        if cfg.networkType == "fullyconnected":
            raise FCNetwork(cfg)
        elif cfg.networkType == "resnet":
            return NotImplementedError
        else:
            raise NotImplementedError


##################################
######## Start FC Network ########


class FCNetwork(tf.keras.Model):
    # defaulted to use NCHW
    def __init__(self, cfg):
        super().__init__()
        self.cfg = cfg
        inputShape = (cfg.planes, cfg.gridSize, cfg.gridSize)
        boolMask = cfg.boolMask  # 1d
        layers = cfg.layers
        actionSize = cfg.actionSize

        self.flatten = tf.keras.layers.Flatten()
        self.maskLayer = tf.keras.layers.Lambda(
            lambda x: tf.boolean_mask(x, boolMask, axis=1)
        )
        self.FClayers = []
        for layer in layers:
            self.FClayers.append(tf.keras.layers.Dense(layer, activation="relu"))
        self.policyHead = tf.keras.layers.Dense(actionSize, activation="softmax")
        self.valueHead = tf.keras.layers.Dense(1, activation="tanh")

    def call(self, inputs):
        x = self.flatten(inputs)
        x = self.maskLayer(x)
        for layer in self.FClayers:
            x = layer(x)
        policy = self.policyHead(x)
        value = self.valueHead(x)
        return policy, value

    # as for trainging, define a Trainer class


######### End FC Network #########
##################################
