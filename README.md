# Flask Workout App

This is a Flask app I built for a Cloud Computing course. The app was originally deployed using the
Google Cloud Platform. Unfortunately there are fees associated with that, so it's no longer up.

When it was up, it could track the workouts of multiple users, storing data in GCP's Datastore.
It had three views: one for selecting a user, one for editing workouts as a whole, and one for
editing the exercises within a workout. It used an API at https://api.api-ninjas.com/v1/exercises
as a way to search for exercises.