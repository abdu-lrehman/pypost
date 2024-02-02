from app.db_config.db_connect import dbconnect
from app.middleware.middleware import app
from app.routes.admin_routes import router as adminRouter
from app.routes.book_routes import router as bookRouter
from app.routes.login_routes import router as loginRouter
from app.routes.user_routes import router as userRouter

dbconnect()


app.include_router(userRouter, tags=["users"])
app.include_router(bookRouter, tags=["books"])
app.include_router(loginRouter, tags=["login"])
app.include_router(adminRouter, tags=["admin"])
