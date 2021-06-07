import pyke

if __name__ == "__main__":
    print(
        pyke.execute(
            """
    get * from account, account2
        where enemies includes(champion("pyke"))
    """
        )
    )
    print(
        pyke.execute(
            """
        get * from account, account2
            where account1.champion = champion("pyke")
        """
        )
    )

    print(
        pyke.execute(
            """
    get len(wins), losses from account
        where matches.enemies
    """
        )
    )
