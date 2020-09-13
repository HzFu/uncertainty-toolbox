"""
Examples of code for visualizations.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
#plt.ion()

import uncertainty_toolbox.data as udata
import uncertainty_toolbox.metrics as umetrics
import uncertainty_toolbox.viz as uviz



# Set random seed
np.random.seed(11)

# Generate synthetic predictive uncertainty results
n_obs = 650
f, std, y, x = udata.synthetic_sine_heteroscedastic(n_obs)


def make_plots(pred_mean, pred_std, idx1, idx2):
    """Make set of plots."""

    update_rc_params()
    ylims = [-3, 3]
    n_subset = 50

    # Make xy plot
    uviz.plot_xy(
        pred_mean, pred_std, y, x, n_subset=300, ylims=ylims, xlims=[0, 15]
    )
    save_plot(idx1, idx2, 'xy')
    plt.show()

    # Make intervals plot
    uviz.plot_intervals(pred_mean, pred_std, y, n_subset=n_subset, ylims=ylims)
    save_plot(idx1, idx2, 'intervals')
    plt.show()

    # Make parity plot
    uviz.plot_parity(pred_mean, y, hexbins=True)
    save_plot(idx1, idx2, 'parity')
    plt.show()

    # Make calibration plot
    uviz.plot_calibration(pred_mean, pred_std, y)
    save_plot(idx1, idx2, 'calibration')
    plt.show()

    # Make ordered intervals plot
    uviz.plot_intervals_ordered(pred_mean, pred_std, y, n_subset=n_subset, ylims=ylims)
    save_plot(idx1, idx2, 'intervals_ordered')
    plt.show()


def update_rc_params():
    """Update matplotlib rc params."""
    #plt.rcParams['font.family'] = 'serif'
    plt.rcParams.update({'font.size': 14})
    plt.rcParams.update({'xtick.labelsize': 14})
    plt.rcParams.update({'ytick.labelsize': 14})


def save_plot(idx1, idx2, plot_str, file_ext='pdf'):
    """Save a plot."""
    file_name = plot_str + '_' + str(idx1) + '_' + str(idx2) + '.' + file_ext
    plt.savefig(file_name, bbox_inches='tight')

    # Print save message
    print('Saved figure: {}'.format(file_name))


# List of predictive means and standard deviations
pred_mean_list = [
    f,
    #f + 0.1,
    #f - 0.1,
    #f + 0.25,
    #f - 0.25,
]

pred_std_list = [
    std,                # correct
    std * 0.5,          # overconfident
    std * 2.0,          # underconfident
]

# Loop through
miscal_area_list = []
for i, pred_mean in enumerate(pred_mean_list):
    for j, pred_std in enumerate(pred_std_list):
        miscal_area = umetrics.miscalibration_area(pred_mean, pred_std, y)
        mace = umetrics.mean_absolute_calibration_error(pred_mean, pred_std, y)
        rmsce = umetrics.root_mean_squared_calibration_error(pred_mean, pred_std, y)
        miscal_list = [i, j, miscal_area, mace, rmsce]
        miscal_area_list.append(miscal_list)
        
        make_plots(pred_mean, pred_std, i, j)

        #uviz.plot_calibration(pred_mean, pred_std, y)
        print('Completed: {}'.format(miscal_list))

