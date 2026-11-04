"""PhishTrace web application."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import urlencode

from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app import agents, store
from app.corpus import DOCS, EXAMPLES, brand_rows, tld_rows
from app.detector import catalog
from app.eda_data import public_sets, summarize
from app.retrieval import VERSION

ROOT = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(ROOT / "templates"))
templates.env.globals["nav"] = [
    {"path": "/", "label": "Overview", "key": "home"},
    {"path": "/investigate", "label": "Investigate", "key": "investigate"},
    {"path": "/pipeline", "label": "Pipeline", "key": "pipeline"},
    {"path": "/methodology", "label": "Method", "key": "method"},
    {"path": "/knowledge", "label": "Knowledge", "key": "knowledge"},
    {"path": "/data", "label": "Data", "key": "data"},
    {"path": "/reports", "label": "Dockets", "key": "reports"},
]

app = FastAPI(
    title="PhishTrace",
    version="1.0.0",
    description="Local phishing-investigation workbench. Rules, retrieval, and a separate verifier. No trained model and no outbound fetch.",
)
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")


class InvestigateIn(BaseModel):
    url: str = Field(min_length=1, max_length=2048)
    mode: str = "agentic"


def _examples() -> list[dict[str, str]]:
    rows = []
    for example in EXAMPLES:
        query = urlencode({"mode": example["mode"], "url": example["url"]})
        rows.append({**example, "href": f"/run?{query}", "form_href": f"/investigate?{query}"})
    return rows


def _render(request: Request, name: str, context: dict[str, object], status: int = 200):
    return templates.TemplateResponse(request=request, name=name, context=context, status_code=status)


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


@app.get("/")
def home(request: Request):
    return _render(
        request,
        "home.html",
        {"active": "home", "examples": _examples(), "recent": store.recent(3)},
    )


@app.get("/investigate")
def investigate_form(request: Request, url: str = "", mode: str = "agentic", error: str = ""):
    if mode not in {"rules", "retrieval", "agentic", "compare"}:
        mode = "agentic"
    return _render(
        request,
        "investigate.html",
        {
            "active": "investigate",
            "examples": _examples(),
            "prefill_url": url,
            "prefill_mode": mode,
            "error": error[:300],
            "public_sets": public_sets(),
        },
    )


@app.post("/investigate")
def investigate_post(url: str = Form(""), mode: str = Form("agentic")):
    try:
        body = agents.investigate(url, mode)
    except ValueError as exc:
        query = urlencode({"url": url, "mode": mode, "error": str(exc)})
        return RedirectResponse(f"/investigate?{query}", status_code=303)
    record = store.save(body)
    return RedirectResponse(f"/reports/{record['id']}", status_code=303)


@app.get("/run")
def run_example(url: str, mode: str = "agentic"):
    try:
        body = agents.investigate(url, mode)
    except ValueError as exc:
        query = urlencode({"url": url, "mode": mode, "error": str(exc)})
        return RedirectResponse(f"/investigate?{query}", status_code=303)
    record = store.save(body)
    return RedirectResponse(f"/reports/{record['id']}", status_code=303)


@app.get("/pipeline")
def pipeline(request: Request):
    return _render(request, "pipeline.html", {"active": "pipeline"})


@app.get("/methodology")
def methodology(request: Request):
    return _render(request, "methodology.html", {"active": "method", "rules": catalog()})


@app.get("/knowledge")
def knowledge(request: Request):
    docs = sorted(DOCS, key=lambda doc: str(doc["title"]))
    return _render(
        request,
        "knowledge.html",
        {
            "active": "knowledge",
            "docs": docs,
            "brands": brand_rows(),
            "tlds": tld_rows(),
            "kb_version": VERSION,
        },
    )


@app.get("/data")
def data_page(request: Request):
    return _render(
        request,
        "data.html",
        {"active": "data", "summary": summarize(), "public_sets": public_sets()},
    )


@app.get("/reports")
def reports(request: Request):
    return _render(request, "reports.html", {"active": "reports", "records": store.recent()})


@app.get("/reports/{report_id}")
def report(request: Request, report_id: str):
    record = store.get(report_id)
    if record is None:
        return _missing(request, "That docket is not on this server. Dockets stay in memory and clear when the app stops.")
    return _render(request, "report.html", {"active": "reports", "record": record})


@app.get("/api/health")
def health():
    return {"status": "ok", "model": "none", "fetcher": "disabled", "knowledge_base": VERSION}


@app.get("/api/knowledge")
def api_knowledge():
    return {"version": VERSION, "documents": DOCS, "brands": brand_rows(), "suffixes": tld_rows()}


@app.get("/api/eda")
def api_eda():
    return summarize()


@app.get("/api/rules")
def api_rules():
    return {"rules": catalog(), "note": "Weighted rules are the risk signal. No classifier is trained."}


@app.get("/api/reports")
def api_reports():
    return {"reports": store.recent()}


@app.get("/api/reports/{report_id}")
def api_report(report_id: str):
    record = store.get(report_id)
    if record is None:
        raise HTTPException(status_code=404, detail="Docket not found")
    return record


@app.post("/api/investigate")
def api_investigate(payload: InvestigateIn):
    try:
        body = agents.investigate(payload.url, payload.mode)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return store.save(body)


@app.exception_handler(404)
async def not_found(request: Request, _exc: Exception):
    if request.url.path.startswith("/api/"):
        return JSONResponse({"detail": "Not found"}, status_code=404)
    if request.url.path.startswith("/reports/"):
        return _missing(request, "That docket is not on this server. Dockets stay in memory and clear when the app stops.")
    return _missing(request, "That page is not part of this workbench.")


def _missing(request: Request, message: str):
    return _render(request, "404.html", {"active": "", "message": message}, status=404)
