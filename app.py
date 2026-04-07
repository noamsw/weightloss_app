from fastapi import FastAPI, HTTPException
import db_functions as db
from datetime import date as Date
from app_models import InputWorkout, Exercise, InputWorkoutExercise, InputWorkoutExerciseSet, OutputExercise, OutputWorkout, OutputWorkoutExercise, OutputWorkoutExerciseSet
from collections.abc import Sequence

app = FastAPI()

def format_output_workout(workouts: Sequence[db.Workout]) -> list[OutputWorkout]:
    formated_workouts: list[OutputWorkout] = []
    for workout in workouts:
        wo = OutputWorkout(id=workout.id, title=workout.title, date=workout.date, description=workout.description)
        if workout.workout_exercises:
            wo.exercises = []
            for we in workout.workout_exercises:
                owe = OutputWorkoutExercise(id=we.id, workout_id=we.workout_id, exercise_id=we.exercise_id, exercise_number=we.exercise_number)
                if we.workout_exercise_sets:
                    owe.sets = []
                    for workout_exercise_set in we.workout_exercise_sets:
                        owe.sets.append(OutputWorkoutExerciseSet(id=workout_exercise_set.id, workout_exercise_id=workout_exercise_set.workout_exercise_id, set_number=workout_exercise_set.set_number, reps=workout_exercise_set.reps, weight=workout_exercise_set.weight))
                wo.exercises.append(owe)
        formated_workouts.append(wo)
    return formated_workouts

@app.post("/workout/")
async def create_workout(workout: InputWorkout):
    with db.SessionLocal() as session:
        try:
            workout_id = db.add_workout(session, [], date=workout.date, title=workout.title, description=workout.description)
            session.commit()
            return {"workout_id": workout_id}
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=str(e))


@app.post("/exercise/")
async def create_exercise(exercise: Exercise):
    with db.SessionLocal() as session:
        try:
            exercise_id = db.add_exercise(session, exercise.title, exercise.description)
            session.commit()
            return {"exercise_id": exercise_id}
        except Exception as e:
            session.rollback()
            raise HTTPException(status_code=500, detail=str(e))


@app.post("/workout_exercise/")
async def create_workout_exercise(workout_exercise: InputWorkoutExercise):
    with db.SessionLocal() as session:
        try:
            workout_exercise_id = db.add_workout_exercise(session, workout_exercise.workout_id, workout_exercise.exercise_id, workout_exercise.exercise_number)
            session.commit()
            return {"workout_exercise_id": workout_exercise_id}
        except ValueError as e:
            session.rollback()
            raise HTTPException(status_code=404, detail=str(e))

@app.post("/workout_exercise_set/")
async def create_workout_exercise_set(workout_exercise_set: InputWorkoutExerciseSet) -> dict[str, int]:
    with db.SessionLocal() as session:
        try:
            workout_exercise_set_id = db.add_workout_exercise_set(session, workout_exercise_set.workout_exercise_id, workout_exercise_set.set_number, workout_exercise_set.reps, workout_exercise_set.weight)
            session.commit()
            return {"workout_exercise_set_id": workout_exercise_set_id}
        except ValueError as e:
            session.rollback()
            raise HTTPException(status_code=404, detail=str(e))

@app.get("/workouts")
async def get_workouts_by_date(date: Date) -> list[OutputWorkout]:
    with db.SessionLocal() as session:
        workouts = db.get_workouts_by_date(session, date)
        if not workouts:
            raise HTTPException(status_code=404, detail="No workouts found for the given date")
        return format_output_workout(workouts)

@app.get("/exercises/")
async def get_exercises() -> list[OutputExercise]:
    with db.SessionLocal() as session:
        out_exercises: list[OutputExercise] = []
        exercises = db.get_exercises(session)
        if not exercises:
            raise HTTPException(status_code=404, detail="No exercises found")
        for exercise in exercises:
            out_exercises.append(OutputExercise(id=exercise.id, title=exercise.title, description=exercise.description))
        return out_exercises

@app.get("/workouts/last")
async def get_last_workouts(limit: int) -> list[OutputWorkout]:
    with db.SessionLocal() as session:
        workouts = db.get_last_workouts(session, limit)
        if not workouts:
            raise HTTPException(status_code=404, detail="No workouts found")
        return format_output_workout(workouts)

@app.get("/workout/{workout_id}")
async def get_workout_by_id(workout_id: int):
    with db.SessionLocal() as session:
        workout = db.get_workout_by_id(session, workout_id)
        if workout:
            return format_output_workout([workout])[0]
        else:
            raise HTTPException(status_code=404, detail="Workout not found")

@app.delete("/workout/{workout_id}")
async def delete_workout(workout_id: int):
    with db.SessionLocal() as session:
        try:
            db.erase_workout(session, workout_id)
            session.commit()
            return {"message": "Workout deleted successfully"}
        except ValueError as e:
            session.rollback()
            raise HTTPException(status_code=404, detail=str(e))

@app.delete("/workout_exercise/{workout_exercise_id}")
async def delete_workout_exercise(workout_exercise_id: int):
    with db.SessionLocal() as session:
        try:
            db.erase_workout_exercise(session, workout_exercise_id)
            session.commit()
            return {"message": "Workout exercise deleted successfully"}
        except ValueError as e:
            session.rollback()
            raise HTTPException(status_code=404, detail=str(e))

@app.delete("/workout_exercise_set/{workout_exercise_set_id}")
async def delete_workout_exercise_set(workout_exercise_set_id: int):
    with db.SessionLocal() as session:
        try:
            db.erase_workout_exercise_set(session, workout_exercise_set_id)
            session.commit()
            return {"message": "Workout exercise set deleted successfully"}
        except ValueError as e:
            session.rollback()
            raise HTTPException(status_code=404, detail=str(e))



