class SummonerRunes():
    def __init__(self, connection):
        self.connection = connection

    async def all(self):
        runepages = await self.connection.request('get', '/lol-perks/v1/pages')
        return await runepages.json()

    async def by_name(self, runepage_name):
        runepages = await self.all()
        for runepage in runepages:
            if runepage['name'] == runepage_name:
                return runepage['id']

    async def set_current(self, runepage_id):
        response = await self.connection.request('put', '/lol-perks/v1/currentpage', data=runepage_id)
        return response.status

    async def set_current_by_name(self, runepage_name):
        desired_runepage = await self.by_name(runepage_name)
        if desired_runepage:
            return await self.set_current(desired_runepage)

class Summoner():
    def __init__(self, connection):
        self.runes = SummonerRunes(connection)
        # Implement more features, icons maybe
