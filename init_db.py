from sqlalchemy import Float, ForeignKey, create_engine, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date as Date
from sqlalchemy import DATE

class Base(DeclarativeBase):
    pass

class Workout(Base):
    __tablename__ = "workouts"
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[Date] = mapped_column(DATE, default=Date.today)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)
    workout_exercises: Mapped[list["WorkoutExercise"]] = relationship(back_populates="workout", cascade="all, delete-orphan")
    def __repr__(self) -> str:
        string = f"Workout(id={self.id!r}, date={self.date!r}, title={self.title!r}, description={self.description!r})"
        if self.workout_exercises:
            string += "\nWorkout Exercises:"
            for exercise in self.workout_exercises:
                string += f"\n\t{exercise}"
        return string


class Exercise(Base):
    __tablename__ = "exercises"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    description: Mapped[str | None] = mapped_column(String(200), nullable=True)

    def __repr__(self) -> str:
        string = f"Exercise(id={self.id!r}, title={self.title!r}, description={self.description!r})"
        return string

class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"
    __table_args__ = (
        UniqueConstraint("workout_id", "exercise_number"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    exercise_number: Mapped[int] = mapped_column(Integer)
    workout_id: Mapped[int] = mapped_column(ForeignKey("workouts.id", ondelete="CASCADE"))
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id", ondelete="RESTRICT"))
    workout: Mapped["Workout"] = relationship(back_populates="workout_exercises")
    exercise: Mapped["Exercise"] = relationship()
    workout_exercise_sets: Mapped[list["WorkoutExerciseSet"]] = relationship(back_populates="workout_exercise", cascade="all, delete-orphan")
    def __repr__(self) -> str:
        return f"WorkoutExercise(id={self.id!r}, workout_id={self.workout_id!r}, exercise_number={self.exercise_number!r}, exercise_id={self.exercise_id!r})"


class WorkoutExerciseSet(Base):
    __tablename__ = "workout_exercise_sets"
    __table_args__ = (
        UniqueConstraint("workout_exercise_id", "set_number"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    set_number: Mapped[int] = mapped_column(Integer)
    reps: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)
    workout_exercise_id: Mapped[int] = mapped_column(ForeignKey("workout_exercises.id", ondelete="CASCADE"))
    workout_exercise: Mapped["WorkoutExercise"] = relationship(back_populates="workout_exercise_sets")
    def __repr__(self) -> str:
        return f"WorkoutExerciseSet(id={self.id!r}, workout_exercise_id={self.workout_exercise_id!r}, set_number={self.set_number!r}, reps={self.reps!r}, weight={self.weight!r})"

def init_db():
    engine = create_engine("sqlite+pysqlite:///./test_db.db")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()

