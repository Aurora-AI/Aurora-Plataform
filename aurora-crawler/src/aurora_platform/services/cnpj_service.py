from fastapi import HTTPException
import httpx


class CnpjService:
    async def get_cnpj_data(self, cnpj: str):
        url = f"https://api.cnpja.com.br/companies/{cnpj}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                raise HTTPException(status_code=response.status_code)
