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
    
    def to_dict(self):
        return {
            "address": self.address,
            "discord_id": self.discord_id,
            "accessToken": self.accessToken,
            "lastUpdate": self.lastUpdate,
            "testCredits": self.testCredits,
            "shares": self.shares,
            "credits": self.credits,
        }