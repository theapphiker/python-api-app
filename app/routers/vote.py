from fastapi import Response, status, HTTPException, APIRouter, Depends
from app import schemas, database, oauth2
from psycopg import errors

router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)

@router.post("/")
def vote(vote: schemas.Vote, current_user: int = Depends(oauth2.get_current_user), db=Depends(database.get_db)):
    cursor, conn = db

    # Check if the post exists
    cursor.execute("SELECT 1 FROM dev.posts WHERE id = %s;", (vote.post_id,))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {vote.post_id} does not exist"
        )

    if vote.dir == 1:
        cursor.execute(
            """INSERT INTO dev.votes (post_id, user_id) VALUES (%s, %s)
               ON CONFLICT DO NOTHING;""",
            (vote.post_id, current_user.get('id'))
        )
    else:
        cursor.execute(
            """DELETE FROM dev.votes WHERE post_id = %s AND user_id = %s;""",
            (vote.post_id, current_user.get('id'))
        )

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)