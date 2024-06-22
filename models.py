from sqlalchemy import create_engine
from sqlalchemy import Column, BigInteger, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship, Mapped 
from sqlalchemy_utils import ChoiceType
import enum

engine = create_engine(
    "postgresql://root:hCCsIkIg7d@195.133.197.29:5432/kdz",
    echo=True
)

class Base(DeclarativeBase):
    def __repr__(self) -> str:
        cols = [
            f"{col}={getattr(self, col)}" for col in self.__table__.columns.keys()]
        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    telegram_id = Column(BigInteger, unique=True)
    last_activity = Column(TIMESTAMP)


class Ticket(Base):
    __tablename__ = 'ticket'

    id = Column(BigInteger, primary_key=True)
    driver_id = Column(ForeignKey("driver.id", ondelete="CASCADE"), nullable=False)
    amount = Column(BigInteger, nullable=True)

    driver = relationship("Driver", back_populates="tickets")


class Truck(Base):
    __tablename__ = 'truck'

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(BigInteger)
    color = Column(String)
    vin_number = Column(String)


class TripReport(Base):
    __tablename__ = 'trip_report'

    id = Column(BigInteger, primary_key=True)
    url = Column(String, )
    driver_id = Column(ForeignKey("driver.id", ondelete="CASCADE"), nullable=False)

class OfficialCompany(Base):
    __tablename__ = 'official_company'

    id = Column(BigInteger, primary_key=True)
    name = Column(String)
    owner = Column(String)
    

class Driver(Base):
    __tablename__ = 'driver'

    id = Column(ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)

    phone = Column(String(20))
    contact_email = Column(String(150))

    last_name = Column(String(250))
    first_name = Column(String(250))

    tickets = relationship("Ticket", back_populates="driver")


class Service(Base): 
    __tablename__ = "service"

    id = Column(BigInteger, primary_key=True)
    driver_id = Column(ForeignKey("driver.id", ondelete="CASCADE"), nullable=False)
    date_of_service = Column(TIMESTAMP)
    sum_of_outlays = Column(BigInteger)
