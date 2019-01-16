import tensorflow as tf


def cross_entropy_loss(y, yhat):

    ### YOUR CODE HERE
    ns, nc = y.shape
    for i in range(ns):
        yhati, yi = yhat[i, :], y[i, :]
        print yhati[tf.argmax(yi)]
    ### END YOUR CODE

    return tf.constant(0)


with tf.Session() as sess:
    out_res = sess.run(cross_entropy_loss(yt, yhatt))