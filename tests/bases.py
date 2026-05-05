from core.annotations import ModelType
from core.db.bases import Base
from fixtureforge import ForgeFactory
from fixtureforge.integrations.sqlalchemy import SyncSQLAlchemyForge


class BaseModelFactory(ForgeFactory):
    """Base factory for SQLAlchemy models using FixtureForge."""

    class Config:
        seed = 42  # deterministic CI mode — no flaky tests
        sqlalchemy_session_persistence = "commit"

    @staticmethod
    def check_factory(
        factory_class: type["BaseModelFactory"],
        model: type[Base],
        session,
    ) -> None:
        """Test that factory creates successfully."""
        forge = SyncSQLAlchemyForge(session=session, factory=factory_class)
        obj = forge.create()
        objs = forge.create_batch(size=2)
        assert isinstance(obj, model)
        assert len(objs) == 2
        for i in objs:
            assert isinstance(i, model)
