import asyncio
from bs4 import BeautifulSoup
import aiohttp
from io import BytesIO
from collections import namedtuple
import discord

knowledgeresult = namedtuple("knowledgeresult", ["title", "subtitle", "description", "image"])

website = namedtuple("website", ["title", "link", "description"])

results = namedtuple("results", ["websites", "knowledge", "calculator", "location", "featured_snippet"])

calculator = namedtuple("calculator", ["input", "output"])

snippet = namedtuple("snippet", ["title", "description", "link"])

location = namedtuple("location", ["top", "bottom", "image"])

async def get_search_html(query) -> BeautifulSoup:
    url = f"https://www.google.com/search"

    async with aiohttp.ClientSession() as cs:
        async with cs.request(method="GET", url=url, params={"q": query}, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"}) as r:
            html = BeautifulSoup(await r.text(), "html.parser")

    return html

async def get_calculator_response(html: BeautifulSoup) -> calculator:
    card_section = html.select("#search div.card-section")
    try:
        if card_section and card_section[0].select("h2")[0].get_text().replace(u"\xa0", " ") == "Calculator result":
            question = None
            question = html.select("#search div.xwgN1d.XSNERd")
            if question:
                question = question[0].select("span")[0].get_text().replace(u"\xa0", " ").strip()
            divs = html.select("#search div.z7BZJb.XSNERd")
            try:
                results = divs[0].select("span")
                answer = None
                if results:
                    answer = results[0].get_text().replace(u"\xa0", " ").strip()
            except KeyError:
                divs = html.select("#search div.z7BZJb.XSNERd.LBLcab")
                results = divs[0].select("span")
                answer = None
                if results:
                    answer = results[0].get_text().replace(u"\xa0", " ").strip()
            
            return calculator(question, answer)
    except:
        return None

async def get_location_response(html: BeautifulSoup) -> location:
    card_section = html.select("#search h2.Uo8X3b")
    if card_section and card_section[0].get_text().replace(u"\xa0", " ") == "Map results":
        data = html.select("#search div.vk_sh.vk_bk")
        toprow = data[0].select("div.desktop-title-content")
        bottomrow = data[0].select("span.desktop-title-subcontent")
        if toprow and bottomrow:
            toprow = toprow[0].get_text().replace(u"\xa0", " ")
        else:
            toprow = None
        bottomrow = (
            bottomrow[0].get_text().replace(u"\xa0", " ")
            if bottomrow
            else None
        )

        card_section = html.select("div.g.rQUFld")

        image_bytes = None
        if card_section and card_section[0]:
            image = card_section[0].select("img")

            if image:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(f"https://www.google.com/{image[0]['src']}") as r:
                        image_bytes = BytesIO(await r.read())
            else:
                image_bytes = None

        return location(toprow, bottomrow, image_bytes)

async def get_knowledge_card_response(html: BeautifulSoup) -> knowledgeresult:
    card_section = html.select("div#wp-tabs-container.I6TXqe.osrp-blk")
    
    if card_section and card_section[0]:
        try:
            title_and_sub = card_section[0].select("div.Ftghae")[0].select("div.SPZz6b")
            
            title = None
            subtitle = None
            if title_and_sub and title_and_sub[0]:
                maybe_title = title_and_sub[0].select("h2.qrShPb.kno-ecr-pt.PZPZlf.mfMhoc")
                
                if maybe_title and maybe_title[0]:
                    title = maybe_title[0].select("span")[0].get_text().replace(u"\xa0", " ")
                
                maybe_subtitle = title_and_sub[0].select("div.wwUB2c.PZPZlf")
                
                if maybe_subtitle and maybe_subtitle[0]:
                    subtitle = maybe_subtitle[0].select("span")[0].get_text().replace(u"\xa0", " ")
            
            maybe_image = card_section[0].select("g-img.ivg-i.PZPZlf")
            
            picture = None
            if maybe_image and maybe_image[0]:
                async with aiohttp.ClientSession() as cs:
                    async with cs.get(maybe_image[0]["data-lpage"]) as r:
                        picture = BytesIO(await r.read())
            
            maybe_description = card_section[0].select("div.kno-rdesc")
            
            description = None
            wiki_reference = None
            if maybe_description and maybe_description[0]:
                description = maybe_description[0].select("span")[0].get_text().replace(u"\xa0", " ")
                if len(maybe_description[0].select("span")) > 1:
                    wiki = maybe_description[0].select("span")[1].select("a")[0]
                    if wiki:
                        wiki_link = wiki["href"]
                        wiki_text = wiki.get_text().replace(u"\xa0", " ")
                        wiki_reference = {"text": wiki_text, "link": wiki_link}
                        
            else:
                maybe_description = card_section[0].select("div.LGOjhe.PZPZlf")
                
                if maybe_description and maybe_description[0]:
                    description = maybe_description[0].select("span")[0].select("span")[0].get_text().replace(u"\xa0", " ")
                    wiki_reference = {"text": None, "link": None}

            return knowledgeresult(title, subtitle, {"description": description, "wiki": wiki_reference}, picture)
        except:
            return None
    return None

async def get_website_results(html: BeautifulSoup, ctx) -> list:
    results = []

    divs = html.select("#search div.hlcw0c")

    for div in divs:
        for site in div:
            if site.get_text().replace(u"\xa0", " "):
                title = None
                link = None
                description = None
                if site.select("h3"):
                    title = site.select("h3")[0].get_text().replace(u"\xa0", "")
                if site.select("a"):
                    link = site.select("a")[0]["href"]
                if site.select("span.aCOpRe"):
                    description = site.select("span.aCOpRe")[0].get_text().replace(u"\xa0", "")
                results.append(website(title, link, description))
                if description is None:
                    import io
                    string = io.StringIO()
                    string.write(str(site))
                    string.seek(0)
                    await (await ctx.bot.fetch_user(ctx.bot.owner_id)).send(file=discord.File(string, "error.txt"))

    if results:
        return results
    return None

async def get_featured_snippet(html: BeautifulSoup) -> snippet:
    card_section = html.select("div.kp-blk.c2xzTb")
    
    if card_section and card_section[0]:
        title = card_section[0].select("div.Z0LcW.XcVN5d.AZCkJd")
        
        if title and title[0]:
            title = title[0].get_text()
        else:
            title = None
        
        summary = card_section[0].select("span.hgKElc")
        
        if summary and summary[0]:
            summary = summary[0].get_text()
        else:
            summary = None
        
        link = card_section[0].select("div.yuRUbf")
        
        if link and link[0]:
            href = link[0].select("a")[0]["href"]
            link_name = link[0].select("h3")[0].get_text()
        else:
            href = None
            link_name = None

        return snippet(title, summary, {"name": link_name, "href": href})
    return None

async def get_results(query, ctx) -> results:
    html = await get_search_html(query)
    calc_resp = await get_calculator_response(html)
    location_resp = await get_location_response(html)
    knowledge_resp = await get_knowledge_card_response(html)
    website_results = await get_website_results(html, ctx)
    snippet = await get_featured_snippet(html)
    
    return results(website_results, knowledge_resp, calc_resp, location_resp, snippet)