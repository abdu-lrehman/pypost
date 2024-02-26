from app.controllers.admin_controller import router as adminRouter
from app.controllers.book_controller import router as bookRouter
from app.controllers.login_controller import router as loginRouter
from app.controllers.user_controller import router as userRouter
from app.db_config.db_connect import dbconnect
from app.middleware.user_dependency import app

dbconnect()


app.include_router(userRouter, prefix="/user", tags=["users"])
app.include_router(loginRouter, prefix="/login", tags=["login"])
app.include_router(adminRouter, prefix="/admin", tags=["admin"])
app.include_router(bookRouter, prefix="/book", tags=["books"])
