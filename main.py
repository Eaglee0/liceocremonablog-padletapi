from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import Optional
app = FastAPI()
origins = [
    "http://localhost:5000",
    "http://localhost:3000",
    "http://liceocremonablog.it",
    "https://liceocremonablog.it",
    "http://www.liceocremonablog.it",
    "https://www.liceocremonablog.it",
    "http://padlet.liceocremonablog.it",
    "https://padlet.liceocremonablog.it"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
myheader = {
    "Content-type": "application/json",
    "App-Id": "227cf1602fd752e8b4396068c61bb11e47141a3ef8a42fcbbcd01739823c137e",
    'Accept': '*/*'
}


@app.get("/")
async def root():
    return {"body": "hello"}


@app.get("/v1/padlet/")
async def padlet(padlet_username: Optional[str] = None,padlet_name: Optional[str] = None):
    def getpadlet(padlet_id: str, loc_padlet_name: str, loc_padlet_username: str):
        padlet_info = requests.get(
            f"https://padlet.com/api/0.9/public_padlets/{padlet_id}", headers=myheader).json()
        posts = requests.get(
            f"https://padlet.com/api/0.9/public_posts?padlet_id={padlet_id}&padlet_url=https%3A%2F%2Fpadlet.com%2F{loc_padlet_username}%2F{loc_padlet_name}", headers=myheader).json()
        posts_data = []
        for post in posts["data"]:
            print(post["subject"])
            if post["body"] == "":
                body = None
            else:
                body = post["body"]
            posts_data.append({
                "subject": post["subject"],
                "body": body,
                "attachment": post["attachment"],
                "attachment_type": post["attachment_type"]
            })
        info = padlet_info["data"]
        info["posts_number"] = posts["meta"]["total_entries"]
        return {
            "info": info,
            "name": padlet_name,
            "posts": posts_data
        }
    if padlet_name and padlet_username:
        padlets = requests.get(
            f'https://padlet.com/api/0.9/public_padlets?username={padlet_username}',
            headers=myheader,
        ).json()
        try:
            padlets["data"]
        except KeyError:
            return JSONResponse(status_code=404, content={"body": "404 error, user don't found"})
        for mypadlet in padlets["data"]:
            if mypadlet["name"] == padlet_name:
                mypadlet_id = mypadlet["id"]
                return getpadlet(mypadlet_id, padlet_name, padlet_username)
            else:
                pass
        return JSONResponse(status_code=404, content={
            "body": "404 error, padlet not found",
            "padlet_name": padlet_name,
            "padlet_username": padlet_username
        })
    else:
        return JSONResponse(status_code=404, content={"body": "404 error, enter padlet name and padlet username"})
