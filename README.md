# Enpoints to implement
POST /students → Add new student (with courses)
GET /students → List all students
    filters: ?min_age=21, ?course=Math
GET /students/{id} → Get single student (with their courses)
PUT /students/{id} → Update student (add/remove courses)
DELETE /students/{id} → Delete student
