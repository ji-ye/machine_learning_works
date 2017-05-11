from math import log


def entropy(pi):
    '''
    return the Entropy of a probability distribution:
    entropy(p) = − SUM (Pi * log(Pi) )

    Input:
        pi: (list) [number 1, number 2]

    Return: (float) entropy
    '''
    total = 0
    for p in pi:
        p = p / sum(pi)
        if p != 0:
            total += p * log(p, 2)
        else:
            total += 0
    total *= -1
    return total


def gain(d, a):
    '''
    return the information gain:
    gain(D, A) = entropy(D)−􏰋 SUM ( |Di| / |D| * entropy(Di) )

    Input:
        d: (list)
        a: (list) of list
    '''
    total = 0
    for v in a:
        total += sum(v) / sum(d) * entropy(v)

    gain = entropy(d) - total
    return gain

def main():
    '''
    Calculate exam result
    '''
    energy_hl = [6,4]
    home_insu_pe = [
        [4,1],
        [2,3]
    ]
    home_size_sml = [
        [2,1],
        [3,2],
        [1,1]
    ]
    temperature_hmc = [
        [1,2],
        [2,0],
        [3,2]
    ]
    # first level
    target_entropy = entropy(energy_hl)
    gain_insu = gain(energy_hl, home_insu_pe)
    gain_homesize = gain(energy_hl, home_size_sml)
    gain_temp = gain(energy_hl, temperature_hmc) # largest gain on target
    gain_hot_insu = gain([2,1],[[2,1],[.5, 1]])

    print('### Level One: Split temperature')
    print('           Target entropy: {:.3F}'.format(target_entropy))
    print('Home insulation info gain: {:.3F}'.format(gain_insu))
    print('      Home size info gain: {:.3F}'.format(gain_homesize))
    print('    Temperature info gain: {:.3F}'.format(gain_temp))

    # second level
    gain_hot_insu = gain([1,2],[[0,1],[1,1]])
    gain_hot_size = gain([1,2],[[0,1],[0,1],[1,0]]) # largest gain on hot

    gain_cool_insu = gain([3,2],[[1,2],[2,0]])
    gain_cool_size = gain([3,2],[[1,0],[2,1],[0,1]])

    print('\n','### Level Two: Split hot/cool on insulation or size')
    print('Information gain for:')
    print('    Split Hot on insulation: {:.3F}'.format(gain_hot_insu))
    print('     Split Hot on home size: {:.3F}'.format(gain_hot_size))
    print('    Split Hot on insulation: {:.3F}'.format(gain_cool_insu))
    print('     Split Hot on home size: {:.3F}'.format(gain_cool_size))

if __name__ == '__main__':
    main()
