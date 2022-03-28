import sqlalchemy
import sqlalchemy.orm
import interview_app.core.config as settings

engine = sqlalchemy.create_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True)
SessionLocal = sqlalchemy.orm.sessionmaker(autocommit=False, autoflush=False, bind=engine)
