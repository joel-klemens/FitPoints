# RESTful API - Joel Klemens

##Explanation of FitPoints API 

## USER STORIES
1. As a user I would like to view my profile from internet connected devices.
2. As a user I would like to view my workout history from internet connected devices.
3. As a user I would like to view my friends public profile from internet connected devices.
4. As a user I would like to view my friends workout history from internet connected devices.
5. As a user I would like to add new workouts from internet connected devices.
6. As a user I would like to make changes to my workout history internet connected devices.
7. As a user I would like to make changes to my profile from internet connected devices.
8. As a user I would like to delete a workout created by accident from internet connected devices.
9. As a user I would like to do a search to find other users I am looking for.

## GENERAL DESIGN
-> The web browser will be the client that the user will interact with allowing them to make requests for information, adding new items and changing existing items on their workout profile. The purpose for the RESTful API is to implement CRUD, the basic functions of persistent storage, to the FIT points database. Outside of the application users will be able to use a browser to access information which is stored as JSON objects.

## ENDPOINTS
1.  /users/self
-> GET, this will return a json string of the users profile information
{
"username": "Joel13",
"age":"22",
"firstname":"Joel",
"lastname":"Klemens"
}
2. /user/user-id
-> GET, this will retrun a json string of the users profile along with the information that they allow to be public. This json string will be similar to what is seen above, other information may include the amount of fit points they have, the amount of time they have spent working out, the total number or workouts that they have logged.
3. /user/self/workout-history
-> GET, this will return a json string list of the types of workouts the user has completed along with details on their workout and the amount of fit points they scored for the workout.
4. /user/user-id/workout-history
-> GET, this will return a json string list of the types of workouts the user has completed along with the public details about each workout and various other information that is part of the user class.
5. /user/self/new-workout
->POST, this will allow the user to input their information about a new workout and have it added to their profile.
6. /user/self/edit-workout
-> PUT, this will allow for the user to modify an existing workout.
7. /user/self/edit-profile
-> PUT, this will allow the user to update the current information they have in their user class profile.
8. /user/self/edit-workout
-> DELETE, this will allow for the user to delete a workout that they no longer wish to keep saved.
9. /users/search
-> GET, this will allow users to search for other users profiles.

## HTTP STATUS CODES
-> Based off of the error codes used by the Amazon RESTful API.  Status codes are used by the server in order to respond to the client.

200 OK -> Success

201 CREATED -> Created

400 BAD REQUEST -> Invalid input parameter preventing the action to be completed, will be accompanied by an indicator as to which                   paramete was invalid.

401 UNAUTHORIZED -> Invalid authentication token for security purposes.

403 FORBIDDEN -> User does no exist, propeties do not belong to user, security.

404 NOT FOUND -> Unable to find requested resource

412 PRECONDITION FAILED -> Precondition failed

429 TOO MANY REQUESTS -> Request rate limiting DDOS attacks

500 SERVER ERROR -> Server not working as intended

503 SERVICE NOT AVAILABLE -> Service not available


## ENHANCEMENT OF DESIGN

-> This RESTful API works great with the object oridented design of the application due to the fact that it is all about the manipulation of JSON strings.  Each class in the application can be described by a JSON string that can be requested, edited, created or deleted through the API.
