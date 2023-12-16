from dungeon.units.mobs.mob import Mob


class KillerRobot(Mob):
    @property
    def name(self) -> str:
        return 'Killer Robot'

class FaultyRobot(Mob):
    @property
    def name(self) -> str:
        return 'Faulty Robot'

class Console(Mob):
    @property
    def name(self) -> str:
        return 'Console'

class Robot(Mob):
    @property
    def name(self) -> str:
        return 'Robot'

class Zombie(Mob):
    @property
    def name(self) -> str:
        return 'Killer Robot'

class Ghoul(Mob):
    @property
    def name(self) -> str:
        return 'Faulty Robot'

class Sleeper(Mob):
    @property
    def name(self) -> str:
        return 'Console'

class Ghost(Mob):
    @property
    def name(self) -> str:
        return 'Robot'
