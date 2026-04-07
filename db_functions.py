from init_db import Workout, Exercise, WorkoutExercise, WorkoutExerciseSet
from sqlalchemy import create_engine, select, event
from sqlalchemy.orm import Session, sessionmaker
from datetime import date

engine = create_engine("sqlite+pysqlite:///./test_db.db", echo=True)
SessionLocal = sessionmaker(bind=engine)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def add_workout(session: Session, workout_exercises: list[WorkoutExercise], date: date = date.today(), title: str = "gym", description: str | None = None) -> int:
    workout = Workout(date=date, title=title, description=description)
    workout.workout_exercises = workout_exercises
    session.add(workout)
    session.flush()
    return workout.id

def add_exercise(session: Session, title: str, description: str | None = None) -> int:
    exercise = Exercise(title=title, description=description)
    session.add(exercise)
    session.flush()
    return exercise.id

def add_workout_exercise(session: Session, workout_id: int, exercise_id: int, exercise_number: int) -> int:
    stmt = select(Workout).where(Workout.id == workout_id)
    workout = session.scalars(stmt).one_or_none()
    if not workout:
        raise ValueError(f"Workout with id {workout_id} does not exist")
    we = WorkoutExercise(workout_id=workout_id, exercise_id=exercise_id, exercise_number=exercise_number)
    session.add(we)
    session.flush()
    return we.id

def add_workout_exercise_set(session: Session, workout_exercise_id: int, set_number: int, reps: int, weight: float) -> int:
    stmt = select(WorkoutExercise).where(WorkoutExercise.id == workout_exercise_id)
    workout_exercise = session.scalars(stmt).one_or_none()
    if not workout_exercise:
        raise ValueError(f"Workout exercise with id {workout_exercise_id} does not exist")
    workout_exercise_set = WorkoutExerciseSet(set_number=set_number, reps=reps, weight=weight, workout_exercise_id=workout_exercise_id)
    session.add(workout_exercise_set)
    session.flush()
    return workout_exercise_set.id

def get_workouts_by_date(session: Session, date: date):
    stmt = select(Workout).where(Workout.date == date)
    return session.scalars(stmt).all()

def get_last_workouts(session: Session, num_workouts: int):
    stmt = select(Workout).order_by(Workout.date.desc()).limit(num_workouts)
    return session.scalars(stmt).all()

def get_workout_by_id(session: Session, workout_id:int):
    stmt = select(Workout).where(Workout.id == workout_id)
    return session.scalars(stmt).one_or_none()

def get_exercises(session: Session):
    stmt = select(Exercise)
    return session.scalars(stmt).all()

def get_exercise_by_id(session: Session, exercise_id: int):
    stmt = select(Exercise).where(Exercise.id == exercise_id)
    return session.scalars(stmt).one_or_none()

def get_workout_exercise_by_id(session: Session, workout_exercise_id: int):
    stmt = select(WorkoutExercise).where(WorkoutExercise.id == workout_exercise_id)
    return session.scalars(stmt).one_or_none()

def get_workout_exercise_set_by_id(session: Session, workout_exercise_set_id: int):
    stmt = select(WorkoutExerciseSet).where(WorkoutExerciseSet.id == workout_exercise_set_id)
    return session.scalars(stmt).one_or_none()

def update_set(session: Session, workout_exercise_set_id: int, new_reps: int | None = None, new_weight: float | None = None):
    stmt = select(WorkoutExerciseSet).where(WorkoutExerciseSet.id == workout_exercise_set_id)
    workout_exercise_set = session.scalars(stmt).one_or_none()
    if workout_exercise_set:
        if new_reps is not None:
            workout_exercise_set.reps = new_reps
        if new_weight is not None:
            workout_exercise_set.weight = new_weight

def erase_workout(session: Session, workout_id: int):
    stmt = select(Workout).where(Workout.id == workout_id)
    workout = session.scalars(stmt).one_or_none()
    if workout:
        session.delete(workout)
    else:
        raise ValueError(f"Workout with id {workout_id} does not exist")

def erase_workout_exercise(session: Session, workout_exercise_id: int):
    stmt = select(WorkoutExercise).where(WorkoutExercise.id == workout_exercise_id)
    workout_exercise = session.scalars(stmt).one_or_none()
    if workout_exercise:
        session.delete(workout_exercise)
    else:
        raise ValueError(f"Workout exercise with id {workout_exercise_id} does not exist")

def erase_workout_exercise_set(session: Session, workout_exercise_set_id: int):
    stmt = select(WorkoutExerciseSet).where(WorkoutExerciseSet.id == workout_exercise_set_id)
    workout_exercise_set = session.scalars(stmt).one_or_none()
    if workout_exercise_set:
        session.delete(workout_exercise_set)
    else:
        raise ValueError(f"Workout exercise set with id {workout_exercise_set_id} does not exist")

def erase_exercise(session: Session, exercise_id: int):
    stmt = select(Exercise).where(Exercise.id == exercise_id)
    exercise = session.scalars(stmt).one_or_none()
    if exercise:
        session.delete(exercise)
    else:
        raise ValueError(f"Exercise with id {exercise_id} does not exist")

