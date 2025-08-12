from fastapi import FastAPI, HTTPException, Query ,Request,Response
from funCods import save_html_page, gmini, chunk_text, gmini_Chunk_summry, optimize_chunks_for_api, create_fallback_summary,final_merge_prompt
from pydantic import BaseModel
import re,json
import asyncio
import sys
from typing import Optional
from firebase_config import login as firebaseLogin ,signup as firebasessignup , TokenPayload,verifyFirebaseToken

from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse




# Fix for Windows asyncio event loop policy
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Item(BaseModel):
    q: str
    url:str

@app.post("/login/")
async def login(token:TokenPayload):
    res = await firebaseLogin(token)
    response = JSONResponse({"status":"ok","res":res},status_code=200)
    response.set_cookie(
        key="token",
        value=token.token,
        httponly=True,
        samesite="Lax"
    )
    print(token)
    return response

@app.post("/singup/")
async def createAccount(token:TokenPayload):
    # print(data)
    res = await firebasessignup(token)
    # print(token)
    response = JSONResponse({"statue":"ok"},status_code=200)
    response.set_cookie(
        key= "token",
        value=token.token,
        httponly=True,
        samesite="Lax"
    )
    return response

@app.get('/verify-auth/')
async def auth_check(req: Request):
    token = req.cookies.get('token')
    # print(token)
    if not token:
        raise HTTPException(status_code=401 , detail="Not authenticated")
    try:
        decoded = verifyFirebaseToken(token)
        return decoded
    except Exception as e:
        raise HTTPException(status_code=401,detail="Invaild token")

@app.get('/logout/')
async def logout(response: Response):
    response.delete_cookie(key='token')
    return {"Logout":"ok","msg":"Cookies Clear!"}

@app.post("/")
# async def read_root(url: Optional[str] = Query(None, description="URL to scrape and summarize")):
async def read_root(item:Item):
    url = item.url
    print("hello")
    print(url)
    if not url:
        return {
            url:"Not Found"
        }
    
    url = url.strip()
    
    # Basic URL validation
    if not url.startswith(('http://', 'https://')):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")

    try:
        # Generate a safe filename from the URL
        safe_filename = re.sub(r'[^a-zA-Z0-9]', '_', url)[:100] + ".html"
        
        # Step 1: Save the HTML and get clean text file
        print(f"🌐 Scraping: {url}")
        clean_text_file = await save_html_page(url=url, file_name=safe_filename)
        
        # Step 2: Chunk the clean text for processing
        print(f"📝 Chunking content from: {clean_text_file}")
        chunks = chunk_text(clean_text_file) # chank contains some array like thigs
        
        if not chunks:
            raise HTTPException(status_code=400, detail="Could not extract meaningful content from the webpage")
        
        print(f"📊 Found {len(chunks)} chunks to process")
        
        # Optimize chunks for API quota
        chunks = optimize_chunks_for_api(chunks, max_daily_requests=45)
        
        # Step 3: Process each chunk with Gemini
        summaries = []
        quota_exceeded = False
        
        for i, chunk in enumerate(chunks):
            print(f"🧠 Summarizing Chunk {i+1}/{len(chunks)}")
            summary = gmini_Chunk_summry(chunk, title=f"Chunk {i+1} Summary")
            
            # Check if quota was exceeded
            if "API Quota Exceeded" in summary or "quota exceeded" in summary.lower():
                quota_exceeded = True
                print(f"🚫 API quota exceeded at chunk {i+1}. Using fallback summary.")
                final_summary = create_fallback_summary(chunks, url)
                break
                
            summaries.append(summary)
            
            # Save each chunk summary
            with open(f"summary_chunk_{i+1}.txt", "w", encoding="utf-8") as f:
                f.write(summary)
        
        # Step 4: Generate final combined summary (only if quota not exceeded)
        if not quota_exceeded and summaries:
            print("🔄 Generating Final Page-Level Summary...")
            combined_input = "\n\n".join(summaries)
            final_summary = gmini(
                f"{final_merge_prompt}. The original URL was: {url}\n\n{combined_input}",
                title="Final Content"
            )
            
            # Check if final summary also hit quota
            if "API Quota Exceeded" in final_summary or "quota exceeded" in final_summary.lower():
                print("🚫 API quota exceeded during final summary. Using fallback.")
                final_summary = create_fallback_summary(chunks, url)
        elif not quota_exceeded:
            final_summary = "No summaries were generated successfully."
        
        cleaned_summary = re.sub(r"^```json\s*|\s*```$", "", final_summary.strip(), flags=re.MULTILINE)
        
        # Save final summary
        with open("final_summary.txt", "w", encoding="utf-8") as f:
            f.write(final_summary)
        try:
            parsed_output = json.loads(cleaned_summary)
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            parsed_output = {
                "error": "Failed to parse AI output as JSON.",
                "raw_output": final_summary
            }
        print("✅ Processing complete!")
        
        # Determine status based on quota usage
        status = "success" if not quota_exceeded else "partial_success_quota_exceeded"
        
        return {
            "url": url,
            "chunks_processed": len(chunks),
            "summaries_generated": len(summaries) if not quota_exceeded else 0,
            "status": status,
            "quota_exceeded": quota_exceeded,
            "output": parsed_output
        }
    
    except Exception as e:
        print(f"❌ Error processing {url}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing URL: {str(e)}")

from funCods import root_run
import time
@app.post("/scrape/")
# async def scrape_with_post(item: Item,req:Request):
async def scrape_with_post(item: Item,req:Request):

    res = await auth_check(req)
    email = res.get("firebase",{}).get("identities",{}).get("email",[None][0])
    # if not res["firebase"]['identities']['email'][0]:
    if not email:
        return {"auth":False,"msg":"You need to Login"}
    print("User",res)
    print("q:",item.q)
    # time.sleep(3)
    return await root_run(q=item.q)

@app.post("/sayan/")
# async def scrape_with_post(item: Item,req:Request):
async def scrape_with_post(item: Item,req:Request):

    print("Sayan's Request")
    print("q:",item.q)
    return await root_run(q=item.q)

# add for problem of port
if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8000))  # Render provides PORT env var
    uvicorn.run("main:app", host="0.0.0.0", port=port)

