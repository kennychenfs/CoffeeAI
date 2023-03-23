import tensorflow as tf


class Trainer:
    def __init__(self, model, cfg):
        self.model = model
        self.cfg = cfg
        if self.config.optimizer == "SGD":
            self.optimizer = tf.keras.optimizers.SGD(
                learning_rate=cfg.lrInit,
                momentum=cfg.momentum,
            )
        elif self.config.optimizer == "Adam":  # the best
            self.optimizer = tf.keras.optimizers.Adam(
                learning_rate=cfg.lrInit,
            )
        elif self.config.optimizer == "Adadelta":
            self.optimizer = tf.keras.optimizers.Adadelta(
                learning_rate=cfg.lrInit,
            )
        else:
            raise NotImplementedError(
                f"{self.config.optimizer} is not implemented. You can change the optimizer manually in train.py."
            )

    @tf.function
    def trainStep(self, data):
        with tf.GradientTape() as tape:
            policy, value = self.model(data)
            policyLoss, valueLoss = self.model.lossFn(
                value, policy, data["valueTarget"], data["policyTarget"]
            )
            loss = policyLoss + valueLoss
        gradients = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(gradients, self.model.trainable_variables))
        return policyLoss, valueLoss

    @staticmethod
    def lossFn(value, policy, valueTarget, policyTarget):
        policyLoss = tf.keras.losses.CategoricalCrossentropy(from_logits=False)(
            policyTarget, policy
        )
        valueLoss = tf.keras.losses.MeanSquaredError()(valueTarget, value)
        return policyLoss, valueLoss
