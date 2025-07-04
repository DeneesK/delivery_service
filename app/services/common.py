from db.db import AsyncSessionFactory


class DBObjectService:
    def __init__(self, session_maker: AsyncSessionFactory) -> None:
        self.session_maker = session_maker
