import numpy as np
from sklearn.metrics import *
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")
# colormap=[sns.set_palette("PuBuGn_d")]
# %matplotlib inline


def plot_precision_recall(y_true, y_prob, model, c='#3e5f7e', alpha=1):
    '''
    Plot precision recall from known y_true, y_prob.
    '''
    precision, recall, _ = precision_recall_curve(y_true, y_prob)
    # plt.clf()
    plt.plot(recall, precision, c=c, label=model, alpha=alpha)
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.ylim([0.0, 1.05])
    plt.xlim([0.0, 1.0])


def main():
    y_true = np.array([1,0,0,1,0,0,1,0,0,1])
    svm_prob = np.array([0.98, 0.2, 0.1, 0.99, 0.55, 0.05, 0.4, 0.35, 0.65, 0.75])
    lr_prob = np.array([0.85, 0.3, 0.22, 0.9, 0.4, 0.2, 0.1, 0.35, 0.81, 0.5])
    y_pred = np.array([1,0,0,1,1,0,0,0,1,1])

    plot_precision_recall(y_true, svm_prob, "SVM")
    plot_precision_recall(y_true, lr_prob, "LR", c='#dc3912', alpha=0.6)
    plt.title('Precision-Recall Curve for SVM & LR models')
    plt.legend()
    plt.savefig('pr_curve.png')
    plt.show()


if __name__ == '__main__':
    main()
