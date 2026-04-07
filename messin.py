
from requests import session
from sqlalchemy import Float, ForeignKey, create_engine, Integer, String, select, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Session, Mapped, mapped_column, relationship
from datetime import date
from init_db import Base, Workout, Exercise, WorkoutExercise, WorkoutExerciseSet

engine = create_engine("sqlite:///weightloss_app.db")

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
with Session(engine)as session:
    excersise1 = Exercise(title="squat", description="a lower body exercise")
    session.add_all([excersise1])
    session.commit()
    workout_ex_1_set1 = WorkoutExerciseSet(set_number=1, reps=10, weight=100)
    workout_exercise_1 = WorkoutExercise(exercise_number=1, exercise=excersise1, workout_exercise_sets=[workout_ex_1_set1])
    work1 = Workout(date=date(2026, 3, 1), title="gym", description="full body workout")
    work1.workout_exercises = [workout_exercise_1]
    session.add_all([work1])
    session.commit()

with Session(engine) as session:
    # session.query(workout).delete()
    # session.commit()
    del_stmt = select(Exercise).where(Exercise.id == 1)
    ex_to_delete = session.scalars(del_stmt).first()
    session.delete(ex_to_delete)
    session.commit()
    # workout_ex_2_set1 = WorkoutExerciseSet(set_number=1, reps=10, weight=100)
    # workout_exercise_1 = WorkoutExercise(exercise_number=2, exercise=excersise1, workout_exercise_sets=[workout_ex_2_set1])
    # stmt = select(Workout).where(Workout.id == 1)
    # workout = session.scalars(stmt).first()
    # if workout:
    #     workout.workout_exercises.append(workout_exercise_1)
    #     session.commit()

with Session(engine) as session:
    stmt = select(Exercise)
    for ex in session.scalars(stmt):
        print(ex)

    print("\n\n")
    stmt = select(Workout)
    for wo in session.scalars(stmt):
        print(wo)

    print("\n\n")
    stmt = select(WorkoutExercise)
    for workout_ex in session.scalars(stmt):
        print(workout_ex)

    print("\n\n")
    stmt = select(WorkoutExerciseSet)
    for workout_ex_set in session.execute(stmt):
        print(workout_ex_set)
