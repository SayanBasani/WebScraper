from playwright.async_api import async_playwright
import google.generativeai as genai
from bs4 import BeautifulSoup
import asyncio
import sys
import requests
from urllib.parse import urlparse
import time

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv("gmini_api_key")

# https://aistudio.google.com/apikey
genai.configure(api_key=api_key)



# Save the Html and the Clean Text file with out html css js
async def save_html_page(url, file_name="page.html", scroll_times=3):
    try:
        # Ensure the event loop policy is set for Windows
        # if sys.platform == "win32":
        #     loop = asyncio.get_event_loop()
        #     if not isinstance(loop, asyncio.ProactorEventLoop):
        #         asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        if sys.platform == "win32":
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/114.0.0.0 Safari/537.36"
                )
            )
            page = await context.new_page()

            await page.goto(url, timeout=60000)
            await page.wait_for_timeout(5000)

            try:
                await page.keyboard.press("Escape")
            except:
                pass

            for i in range(scroll_times):
                await page.mouse.wheel(0, 3000)
                await page.wait_for_timeout(2000)

            html_content = await page.content()
            
            # Save raw HTML
            with open(file_name, "w", encoding="utf-8") as f:
                f.write(html_content)
            
            # Extract clean text content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text and clean it
            text_content = soup.get_text()
            lines = (line.strip() for line in text_content.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            clean_text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Save clean text version
            text_file_name = file_name.replace('.html', '_clean.txt')
            with open(text_file_name, "w", encoding="utf-8") as f:
                f.write(clean_text)

            await context.close()
            await browser.close()
            return text_file_name  # Return the clean text file name

    except NotImplementedError as e:
        print(f"⚠️ Playwright failed on Windows, trying fallback method...")
        return save_html_page_fallback(url, file_name)
    
    except Exception as e:
        print(f"⚠️ Playwright failed: {e}, trying fallback method...")
        try:
            return save_html_page_fallback(url, file_name)
        except Exception as fallback_error:
            raise Exception(f"Both Playwright and fallback methods failed. Playwright: {str(e)}, Fallback: {str(fallback_error)}")

# Fallback method using requests instead of Playwright for Windows compatibility.
def save_html_page_fallback(url, file_name="page.html"):
    try:
        # Check if it's a known problematic site
        domain = urlparse(url).netloc.lower()
        social_media_sites = ['facebook.com', 'instagram.com', 'twitter.com', 'linkedin.com', 'tiktok.com']
        
        if any(site in domain for site in social_media_sites):
            print(f"⚠️ Detected social media site: {domain}")
            print("Social media sites often block automated requests and require login.")
        
        # Enhanced headers to look more like a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        
        session = requests.Session()
        response = session.get(url, headers=headers, timeout=30, allow_redirects=True)
        
        # Custom error handling for different status codes
        if response.status_code == 403:
            raise Exception(f"Access forbidden (403). The website '{domain}' blocks automated requests.")
        elif response.status_code == 404:
            raise Exception(f"Page not found (404). The URL '{url}' doesn't exist.")
        elif response.status_code == 400:
            raise Exception(f"Bad request (400). The website '{domain}' rejected the request. This is common for social media sites that require login.")
        elif response.status_code == 429:
            raise Exception(f"Rate limited (429). The website '{domain}' is blocking too many requests.")
        
        response.raise_for_status()
        
        html_content = response.text
        
        # Check if we got actual content or just a login/error page
        if len(html_content.strip()) < 500:
            raise Exception(f"Received very little content ({len(html_content)} chars). The site might be blocking requests or require authentication.")
        
        # Save raw HTML
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # Extract clean text content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Get text and clean it
        text_content = soup.get_text()
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        clean_text = '\n'.join(chunk for chunk in chunks if chunk)
        
        # Validate that we extracted meaningful content
        if len(clean_text.strip()) < 100:
            raise Exception(f"Could not extract meaningful content. The site might be heavily JavaScript-based or require authentication.")
        
        # Save clean text version
        text_file_name = file_name.replace('.html', '_clean.txt')
        with open(text_file_name, "w", encoding="utf-8") as f:
            f.write(clean_text)
        
        print(f"✅ Successfully scraped {len(clean_text)} characters of content")
        return text_file_name
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error while accessing '{url}': {str(e)}")
    except Exception as e:
        raise Exception(f"Fallback scraping failed for '{url}': {str(e)}")

# --- Chunk Text by Word Count ---
def chunk_text(file, max_tokens=3000):
    chunks = []
    current_chunk = []
    current_len = 0

    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # If it's HTML, extract clean text first
        if file.endswith('.html'):
            soup = BeautifulSoup(content, 'html.parser')
            # Remove unwanted elements
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()
            content = soup.get_text()
            
        # Split into lines and process
        lines = content.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            word_count = len(line.split())
            
            # If single line exceeds max_tokens, split it
            if word_count > max_tokens:
                words = line.split()
                for i in range(0, len(words), max_tokens):
                    chunk_words = words[i:i + max_tokens]
                    chunks.append(' '.join(chunk_words))
                continue
            
            # Check if adding this line would exceed the limit
            if current_len + word_count > max_tokens and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_len = word_count
            else:
                current_chunk.append(line)
                current_len += word_count

        # Add the last chunk if it exists
        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        return chunks
        
    except Exception as e:
        print(f"Error reading file {file}: {e}")
        return []


# --- Gemini Summarizer chunk maker ---
chat_session = None
def gmini(prompt, title="Search Query"):
    global chat_session
    try:
        generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
        if chat_session is None:
            chat_session = model.start_chat(history=[])
        
        response = chat_session.send_message(prompt)
        print(f"✅ {title} generated.\n")
        return response.text.strip()

    except Exception as e:
        error_str = str(e)
        if "429" in error_str or "quota" in error_str.lower():
            print(f"🚫 Gemini API quota exceeded. Daily limit reached.")
            print("💡 Solutions:")
            print("   1. Wait 24 hours for quota reset (free tier)")
            print("   2. Upgrade to paid plan at https://aistudio.google.com/")
            return f"❌ API Quota Exceeded: {title} could not be generated due to rate limits. Please try again tomorrow or upgrade your API plan."
        else:
            print(f"❌ Error generating {title}: {e}")
            return f"Error: Could not generate summary for {title}. {str(e)}"


# gen chunk
def gmini_Chunk_summry(data, title="Chunk Summary"):
    try:
        prompt = f"{chunk_prompt} \n the details is: \n {data}"
        response = gmini(prompt,title)
        return response


    except Exception as e:
        print(f"❌ Error generating {title}: {e}")
        return f"Error: Could not generate summary for {title}. {str(e)}"


# --- Enhanced Content Extraction ---
def extract_meaningful_content(html_content):
    """
    Extracts only meaningful content from HTML, removing navigation, ads, etc.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Remove unwanted elements
    unwanted_tags = [
        'script', 'style', 'nav', 'footer', 'header', 'aside', 
        'form', 'button', 'input', 'select', 'textarea',
        'iframe', 'embed', 'object', 'applet'
    ]
    
    # Remove by tag
    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()
    
    # Remove by class/id (common patterns)
    unwanted_selectors = [
        '[class*="nav"]', '[class*="menu"]', '[class*="sidebar"]',
        '[class*="footer"]', '[class*="header"]', '[class*="ad"]',
        '[class*="popup"]', '[class*="modal"]', '[class*="cookie"]',
        '[id*="nav"]', '[id*="menu"]', '[id*="sidebar"]',
        '[id*="footer"]', '[id*="header"]', '[id*="ad"]'
    ]
    
    for selector in unwanted_selectors:
        for element in soup.select(selector):
            element.decompose()
    
    # Try to find main content areas
    main_content = None
    content_selectors = [
        'main', 'article', '[role="main"]', 
        '.content', '.main-content', '.post-content',
        '.entry-content', '.article-content', '#content'
    ]
    
    for selector in content_selectors:
        content = soup.select_one(selector)
        if content:
            main_content = content
            break
    
    # If no main content found, use body
    if not main_content:
        main_content = soup.find('body') or soup
    
    # Extract text and clean it
    text = main_content.get_text(separator='\n', strip=True)
    
    # Clean up the text
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if len(line) > 3:  # Ignore very short lines
            lines.append(line)
    
    return '\n'.join(lines)


# --- API Usage Optimization ---
def optimize_chunks_for_api(chunks, max_daily_requests=45):
    if len(chunks) > max_daily_requests:
        print(f"⚠️ Too many chunks ({len(chunks)}) for daily API limit ({max_daily_requests})")
        print(f"📉 Reducing to {max_daily_requests} chunks to stay within limits")
        # Keep the most important chunks (first and last parts)
        if max_daily_requests >= 4:
            mid_point = max_daily_requests - 2
            selected_chunks = chunks[:mid_point//2] + chunks[-mid_point//2:]
        else:
            selected_chunks = chunks[:max_daily_requests]
        return selected_chunks
    return chunks


def create_fallback_summary(chunks, url):
    """
    Create a basic summary when API quota is exceeded.
    """
    total_chars = sum(len(chunk) for chunk in chunks)
    total_words = sum(len(chunk.split()) for chunk in chunks)
    
    return f"""
        📄 **Fallback Summary for: {url}**

        🔍 **Page Type**: Content extracted successfully but AI analysis unavailable due to API limits

        📊 **Content Statistics**:
        - Total chunks processed: {len(chunks)}
        - Total characters: {total_chars:,}
        - Estimated words: {total_words:,}

        ⚠️ **AI Summary Unavailable**:
        Gemini API daily quota exceeded. The content was successfully scraped and processed, but AI summarization is temporarily unavailable.

        💡 **Solutions**:
        1. Try again tomorrow (quota resets every 24 hours)
        2. Upgrade to paid Google AI plan for higher limits
        3. The raw content has been saved to files for manual review

        📝 **First 500 characters of content**:
        {chunks[0][:500] if chunks else "No content available"}...

        ---
        Generated at: {time.strftime('%Y-%m-%d %H:%M:%S')}
        """



_chunk_prompt = """
    You are a highly accurate and structured web content extractor.

    You will be given clean **visible text** extracted from a web page. Your job is to extract meaningful **sectional content and itemized data** into a consistent, developer-friendly JSON structure.

    ---

    🧠 TASK:

    1. Detect the type of webpage (`documentation`, `article`, `news`, `product_list`, `video_list`, `food_menu`, `knowledge_base`, or `other`)
    2. Extract:
    - **Sections** of text (with heading, type, and content)
    - **Items** if the page contains products, articles, videos, food, etc.
    - Links, images, and videos only if meaningful
    3. Use a **flat and clean JSON** format.
    4. Don't include UI components, cookie banners, or ads.
    5. Use `null` or empty arrays when no data exists. Don't guess or create fake values.
    6. If unsure of the item structure, use `type: other` and add basic fields.

    ---

    🧾 RETURN FORMAT:

    ```json
    {
    "page_type": "article | documentation | news | product_list | video_list | food_menu | knowledge_base | other",
    "title": "Main page title",
    "description": "Brief summary or intro, if any",
    "sections": [
        {
        "heading": "Section Heading",
        "type": "text | faq | code | info | steps | custom",
        "content": "Full text of this section"
        }
    ],
    "items": [
        {
        "type": "product | news | video | food | other",
        "title": "Item or entry title",
        "description": "Detailed content",
        "price": "₹... (if applicable)",
        "rating": 4.3,
        "date": "2025-07-25",
        "image": "https://...",
        "link": "https://...",
        "metadata": {
            "brand": "...",
            "features": ["..."],
            "location": "...",
            "creator": "...",
            "category": "...",
            "duration": "..."
        }
        }
    ],
    "links": [
        { "text": "Link text", "url": "https://..." }
    ],
    "images": ["https://..."],
    "videos": ["https://..."],
    "scraped_at": "2025-07-25T12:00:00Z",
    "source_url": "https://original-page-url.com"
    }
    """


_final_merge_prompt = f"""
    You are a smart AI assistant that merges multiple chunked outputs of a webpage into one final clean JSON.

    Each chunk may contain overlapping sections or items. Your job is to:

    - Merge all content
    - Deduplicate sections or items
    - Preserve structure and meaningful groupings
    - Output clean, final JSON that follows the standard structure below

    ---

    🧾 FINAL JSON FORMAT:

    ```json
    {{
    "page_type": "...",
    "title": "...",
    "description": "...",
    "sections": [
        {{
        "heading": "...",
        "type": "...",
        "content": "..."
        }}
    ],
    "items": [
        {{
        "type": "...",
        "title": "...",
        "description": "...",
        "price": "...",
        "rating": 4.5,
        "date": "...",
        "image": "...",
        "link": "...",
        "metadata": {{
            "brand": "...",
            "features": [...],
            "creator": "...",
            "duration": "...",
            "category": "..."
        }}
        }}
    ],
    "links": [...],
    "images": [...],
    "videos": [...],
    "scraped_at": "...",
    "source_url": "..."
    }}
    """




chunk_prompt = """
    You are a highly accurate and structured web content extractor.
    You will be given clean **visible text** extracted from a web page. Your job is to extract meaningful **sectional content and itemized data** into a consistent.

    🧠 TASK:

    1. Detect the type of webpage (`documentation`, `article`, `news`, `product_list`, `video_list`, `food_menu`, `knowledge_base`, or `other`)
    2. Don't include UI components, cookie banners, or ads.
    """


final_merge_prompt = f"""
    You are a smart AI assistant that merges multiple chunked outputs of a webpage into one final clean samarrize detailed text.

    Each chunk may contain overlapping sections or items. Your job is to:

    - Merge all content
    - Deduplicate sections or items
    - Preserve structure and meaningful groupings
    - Output clean, final

    """

from fastapi import HTTPException
import re,json

def serch_questions(query):
    gmini()

async def root_run(q):
    # url = item.url
    if not q:
        return {"error": True, "msg": "No query provided"}
    print("URL from Root Run "+q)
    
    q = q.strip()
    
    # Basic URL validation
    if not q.startswith(('http://', 'https://')):
        ans = gmini(q)
        return {
            "question": q,
            "output": ans
        }
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
    url = q
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
            parsed_output =  final_summary

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


