from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional, Any
from model import Pato

app = FastAPI(title="API de Patos da DS14", version="0.0.1",description="Api de patos que a sala escolheu")

def fake_db():
    try:
        print("conectando no banco de dados")
    finally:
        print("Fechando a conexão com o banco de dados")


patos = {
    1:{
        "nome":"Luca",
        "especie":"Pato canadense",
        "idade":25,
        "cor":"Cinza e verde",
        "foto":"https://www.publicdomainpictures.net/pictures/190000/nahled/canadian-duck-2.jpg"
    },
        2:{
        "nome":"Perrry",
        "especie":"Orintorinco",
        "idade":5,
        "cor":"Verde",
        "foto":"https://preview.redd.it/6gle9y2sryk71.jpg?auto=webp&s=29e0880d84b81d8a830ba99d81746c0a50783309"
    }
}

@app.get("/")
async def raiz():
    return{"mensagem":"Deu certo"}

@app.get("/patos",description="retoena todos os patos ", summary="Retorna todos os patos")
async def get_patos(db:Any = Depends(fake_db)):
    return patos

@app.get("/patos/{pato_id}")
async def get_pato(pato_id:int):
    try:
        pato=patos[pato_id]
        return pato
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe pato com esse ID {pato_id}")
    
    
@app.post("/patos", status_code=status.HTTP_201_CREATED)
async def post_pato(pato:Optional[Pato]=None):
    next_id=len(patos)+1
    patos[next_id]=pato
    del pato.id
    return pato
    
    
@app.put("/patos/{pato_id}",status_code=status.HTTP_202_ACCEPTED)
async def put_pato(pato_id:int, pato:Pato):
    if pato_id in patos:
        patos[pato_id]=pato
        pato.id=pato_id
        del pato.id
        return pato
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe pato com esse ID {pato_id}")
    
    
@app.delete("/patos/{pato_id}")    
async def delete_pato(pato_id:int):
    if pato_id in patos:
        del patos[pato_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe pato com esse ID {pato_id}")

@app.get("/calculadora")
async def calcular(num1:int,num2:int):
    soma= num1+num2
    return soma

if __name__=="__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)