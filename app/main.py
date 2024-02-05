from app.controllers.admin_controller import router as adminRouter
from app.controllers.login_controller import router as loginRouter
from app.controllers.user_controller import router as userRouter
from app.db_config.db_connect import dbconnect
from app.middleware.user_dependency import app

dbconnect()


app.include_router(userRouter, tags=["users"])
app.include_router(loginRouter, tags=["login"])
app.include_router(adminRouter, tags=["admin"])
