import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

df = pd.read_csv(
    'fcc-forum-pageviews.csv',
    parse_dates=['date'],
    index_col='date'
)

df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    df_line = df.copy().reset_index()
    df_line.rename(columns={'value': 'Page Views'}, inplace=True)

    plt.figure(figsize=(18, 6))
    plot = sns.lineplot(data=df_line, x='date', y='Page Views')
    plot.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    plot.set_xlabel("Date")
    plot.set_ylabel("Page Views")
    fig = plot.figure

    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    df_bar = df.copy().reset_index()
    df_bar['Years'] = df_bar['date'].dt.year
    df_bar['Months'] = df_bar['date'].dt.month_name()
    df_bar.rename(columns={'value': 'Page Views'}, inplace=True)

    df_bar = (
        df_bar
        .groupby(['Years', 'Months'])['Page Views']
        .mean()
        .unstack()
        .reindex(columns=[
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ])
    )

    fig = df_bar.plot(kind='bar', figsize=(18, 6)).figure

    plt.xlabel('Years')
    plt.ylabel('Average Page Views')
    plt.legend(title='Months')

    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    df_box = df.copy().reset_index()
    df_box.rename(columns={'value': 'Page Views'}, inplace=True)
    df_box['year'] = df_box['date'].dt.year
    df_box['month'] = df_box['date'].dt.strftime('%b')

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    fig, axes = plt.subplots(1, 2, figsize=(20, 6))

    sns.boxplot(
        ax=axes[0],
        data=df_box,
        x='year',
        y='Page Views'
    )
    axes[0].set_title('Year-wise Box Plot (Trend)')
    axes[0].set_xlabel('Year')
    axes[0].set_ylabel('Page Views')

    sns.boxplot(
        ax=axes[1],
        data=df_box,
        x='month',
        y='Page Views',
        order=month_order
    )
    axes[1].set_title('Month-wise Box Plot (Seasonality)')
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Page Views')

    fig.savefig('box_plot.png')
    return fig
