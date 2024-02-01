from fastapi import FastAPI
from fastapi.responses import JSONResponse
from .dbconfig.dbconnect import dbconnect
from .routes.userRoutes import router as userRouter
from .routes.bookRoutes import router as bookRouter
from .routes.loginRoutes import router as loginRouter
from .routes.adminRoutes import router as adminRouter
from .middleware.middleware import app


dbconnect()


app.include_router(userRouter, tags=["users"])
app.include_router(bookRouter, tags=["books"])
app.include_router(loginRouter, tags=["login"])
app.include_router(adminRouter, tags=["admin"])
