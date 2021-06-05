import pyke

if __name__ == '__main__':
    print(pyke.execute(
    """
    select * from account.all
        where enemies.includes.champion.championName("pyke")
    """
    ))
    print(pyke.execute(
    """
    select len(wins), losses from account
        where matches.enemies
    """
    ))
