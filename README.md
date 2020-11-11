## Tech Stack
- Language: Python
- Framework: Django, Django Rest Framework
- Dev/Ops: Docker, Travis CI

## Highlights:
- Test-driven development (TDD)
- Using Docker for easy deployment
- Travis CI tools for testing when checking in codes
- Unit Testing in Django
- Mocking with unittests: testing database connection before other command

## API Intro
An API for managing personal recipe 
- Get all recipes  
GET /api/recipe/
- Create recipe  
POST /api/recipe/
- Update partial recipe  
PATCH /api/recipe/<id>
- Update full recipe  
PUT /api/recipe/<id>
- Remove a recipe  
DELETE /api/recipe/<id>