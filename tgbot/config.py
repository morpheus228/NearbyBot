from dataclasses import dataclass

from environs import Env

# Order searching limitations
ORDER_AVAILABILITY_RADIUS = 10

# Antispam middleware
PAUSE_TIME = 2
IGNORE_TIME = 120
WARNINGS_LIMIT = 5

# Orders count limitations
MAX_ORDERS_COUNT_AS_CREATOR = 5
MAX_ORDERS_COUNT_AS_EXECUTOR = 5


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous


def load_db_config(path: str = None):
    env = Env()
    env.read_env(path)

    return DbConfig(
        host=env.str('DB_HOST'),
        password=env.str('DB_PASSWORD'),
        user=env.str('DB_USER'),
        database=env.str('DB_NAME'))


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASSWORD'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous()
    )
