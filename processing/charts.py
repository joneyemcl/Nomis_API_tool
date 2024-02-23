"""
Functions for chart templates
"""

import logging

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_style('whitegrid')


def bar(df: pd.DataFrame, path: str):
    logging.debug(f'creating bar chart with {df}')
    # setting figure
    fig, ax = plt.subplots(figsize=(6, 1.2))
    # creating plot
    ax = df.plot.bar(color=['#052d3f', '#84a2af'], ax=ax)
    # spine
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # axis labels
    ax.set_ylabel('')
    # grid
    ax.yaxis.grid(color='#f5f5f5', ls='--')
    ax.xaxis.grid(False)
    # ticks lables
    vals = ax.get_yticks()
    ax.set_yticklabels(['{0:.0f}%'.format(x * 100) for x in vals])
    for tick in ax.get_xticklabels():
        tick.set_rotation(0)
    # legend
    ax.legend(loc=(0.65, 0.6))
    # saving figure
    logging.debug(f'saving img to {path}')
    fig.savefig(path, bbox_inches='tight', dpi=300)


def line(df: pd.DataFrame, path='', pct=False, width=6, height=2):
    logging.debug('creating line chart')
    # setting figure
    fig, ax = plt.subplots(figsize=(width, height))
    ax = df.plot.line(color=['#ff5000', '#052d3f', '#84a2af'], lw=0.9, ax=ax)
    # spines
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # customising axis
    ax.set_xlim([None, None])
    # tick labels
    if pct == True:
        vals = ax.get_yticks()
        ax.set_yticklabels(['{0:.0f}%'.format(x * 100) for x in vals])
    # grind
    ax.grid(color='#f5f5f5', ls='--')
    # legend
    ax.legend()
    # save
    if path:
        logging.debug(f'saving line chart to {path}')
        fig = ax.get_figure()
        fig.savefig(path, bbox_inches='tight', dpi=300)