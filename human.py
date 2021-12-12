class Human:
    def __init__(
        self,
        address,
        discord_id,   
        accessToken,
        lastUpdate,
        testCredits,
        shares,
        credits
    ):
        self.address = address
        self.discord_id = discord_id
        self.accessToken = accessToken
        self.lastUpdate = lastUpdate
        self.testCredits = testCredits
        self.shares = shares
        self.credits = credits
        self.msg_out_of_credit=False
        self.not_registered_msg=False
        self.auth_tries=0