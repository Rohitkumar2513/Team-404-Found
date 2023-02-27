# Notes

2 levels of users:  
level 1: Low level user(Employee). Can login to app, mark attendence for himself, view his past attendence, view future attendence slots  
level 2: Higher level user(Boss). Can login, Edit other's attendence, view attendence of each employee(add graphs here), Set new attendence slots, export data and download  

Lets try to do it without authentication processes since its just a prototype. There wont be any sign up or login.  
Add some sort of a button which opens a modal where I can enter a hard coded password to go into sudo mode(high level user). Validate password through client side js (if else podhum).

# Todo

- [x] JSON file to store metadata abt dataset instead of editing lists in source code
- [x] Add face recognition model to flask app
- [x] Add fps
- [x] Automatically update json when collecting new data
- [ ] Implement a high level user simulation for 
- [ ] Design attendance system (unique id for each attendence everyday)
- [ ] Script to create attendence slot with unique id
- [ ] Create mongo db database
- [ ] Link flask app with mongo db
- [ ] Get location during attendance 
- [ ] Store one sample frame from attendance video
- [ ] Mark attendence like this sample document:
```json
{
    "_id": "35s4adf5a4sdf54a6sdf4a6d4f6asd4f6a",
    "attendance id": "Unique id for attendance",
    "attendence": True | False (False if no attendence and None for all below values),
    "timestamp": Datetime object,
    "location": {
        "lat": 69,
        "lon": 420
    },
    "screenshot": "upload to imgur and paste url here? OR None to mark attendance without video"
}
```
- [ ] Add mail/telegram notification method after successful attendance(using threading?)
- [ ] Display attendance as a table to user
- [ ] High level user can edit attendence of others
