import matplotlib.pyplot as plt
import seaborn as sns
import pickle
import json

def plot_hist():
    with open('TS_multi_dop_-2.pt','rb') as f:
        list_dop = pickle.load(f)

    with open('TS_multi_norep_-3.pt','rb') as f:
        list_norep = pickle.load(f)


    plot_dop = sns.distplot(list_dop, hist=True, kde=False, bins=50,color='yellow',label='Dopamine Transporter')
    plt.xlabel('Tanimoto Similarity')
    plt.ylabel('Number of Molecules')
    plt.savefig('TS_mult_dop_hist.png')
    plt.clf()
    plot_norep = sns.distplot(list_norep,hist=True, kde=False, bins=50, color='red',label='Norepinephrine Transporter')
    plt.xlabel('Tanimoto Similarity')
    plt.ylabel('Number of Molecules')
    plt.savefig('TS_mult_norep_hist.png')
    plt.clf()
    fig, ax = plt.subplots()
    plot_dop = sns.distplot(list_dop, hist=True, kde=False, bins=50, color='yellow', label='Dopamine Transporter')
    plot_norep = sns.distplot(list_norep,hist=True, kde=False, bins=50, color='red',label='Norepinephrine Transporter')
    ax.legend()
    plt.xlabel('Tanimoto Similarity')
    plt.ylabel('Number of Molecules')
    plt.savefig('TS_mult_hist.png')
    plt.clf()
    fig, ax = plt.subplots()
    plot_dop = sns.kdeplot(list_dop,  color='yellow', label='Dopamine Transporter',
                            ax=ax, shade=True)
    plot_norep = sns.kdeplot(list_norep, color='red',
                              label='Norepinephrine Transporter', ax=ax, shade=True)
    ax.legend()
    plt.xlabel('Tanimoto Similarity')
    plt.ylabel('Density')
    plt.savefig('TS_mult_kde.png')
    plt.clf()



def plot_density():
    with open('TS_zinc.pt','rb') as f:
        list_zinc = pickle.load(f)
    with open('TS_dopaminedat.pt', 'rb') as f:
        list_dopamine = pickle.load(f)
    with open('TS_conditional_final.pt','rb') as f:
        list_conditional = pickle.load(f)

    fig,ax = plt.subplots()

    plot_zinc = sns.kdeplot(list_zinc,  ax=ax, color='blue', label='Zinc Expert', shade=True)
    plot_dopamine = sns.kdeplot(list_dopamine,  ax=ax, color='red', label='Dopamine Expert', shade=True)
    plot_conditional = sns.kdeplot(list_conditional,  ax=ax, color='green', label='Zinc Expert with Initialization', shade=True)
    ax.legend()
    plt.xlabel('Tanimoto Similarity')
    plt.ylabel('Density')
    # plt.legend([plot_dopamine, plot_zinc, plot_conditional],
    #            ['Dopamine Expert', 'Zinc Expert', 'Zinc Expert with Initialization'])
    plt.savefig('TS_kde.png')

def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


def returnxandy(json_file):
    with open(json_file,'rb') as f:
        x=[]
        y=[]
        data = json.load(f)
        for dp in data:
            if int(dp[1]) > 2385:
                break
            x.append(int(dp[1]))
            y.append(float(dp[2]))

        return x,y

def plotline():
    zinc_file = 'zinc_final_reward.json'
    dopamine_file = 'dopamine_final_reward.json'
    conditional_file = 'conditional_final_reward.json'
    zincx,zincy = returnxandy(zinc_file)
    dopx,dopy = returnxandy(dopamine_file)
    conx,cony = returnxandy(conditional_file)
    plt.plot(zincx,zincy, color=lighten_color('blue'), label='Zinc Expert')
    plt.plot(dopx,dopy,color=lighten_color('red'), label='Dopamine Expert')
    plt.plot(conx,cony,color=lighten_color('green'), label='Zinc Expert with Initialization')
    plt.legend()
    plt.xlabel('No. of Iterations')
    plt.ylabel('Mean Final Reward')
    plt.savefig('Final_Reward_Stats.png')

if __name__ == "__main__":
    plot_hist()


