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

    target_entropy = entropy(energy_hl)
    gain_insu = gain(energy_hl, home_insu_pe)
    gain_homesize = gain(energy_hl, home_size_sml)
    gain_temp = gain(energy_hl, temperature_hmc)

    print('           Target entropy: {:.3F}'.format(target_entropy))
    print('Home insulation info gain: {:.3F}'.format(gain_insu))
    print('      Home size info gain: {:.3F}'.format(gain_homesize))
    print('    Temperature info gain: {:.3F}'.format(gain_temp))


if __name__ == '__main__':
    main()
