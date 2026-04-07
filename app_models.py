from datetime import date as Date
from pydantic import BaseModel
from pydantic import Field
from typing import Annotated

class InputWorkout(BaseModel):
    title: str
    date: Date = Field(default_factory=Date.today)
    description: str | None = None

class Exercise(BaseModel):
    title: str
    description: str | None = None

class InputWorkoutExercise(BaseModel):
    workout_id: int
    exercise_id: int
    exercise_number: int

class InputWorkoutExerciseSet(BaseModel):
    workout_exercise_id: int
    set_number: int
    reps: int
    weight: float

class OutputWorkoutExerciseSet(BaseModel):
    id: int
    workout_exercise_id: int
    set_number: Annotated[int, Field(gt=0)]
    reps: Annotated[int, Field(gt=0)]
    weight: Annotated[float, Field(gt=0)]

class OutputWorkoutExercise(BaseModel):
    id: int
    workout_id: int
    exercise_id: int
    exercise_number: Annotated[int, Field(gt=0)]
    sets: list[OutputWorkoutExerciseSet] | None = None

class OutputWorkout(BaseModel):
    id: int
    title: str
    date: Date = Field(default_factory=Date.today)
    description: str | None = None
    exercises: list[OutputWorkoutExercise] | None = None

class OutputExercise(BaseModel):
    id: int
    title: str
    description: str | None = None