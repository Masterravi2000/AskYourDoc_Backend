from pydantic import BaseModel

class DashboardStatsResponse(BaseModel):
    total_files: int
    today_files: int

    total_searches: int
    total_downloads: int

    pdf_count: int
    pdf_today: int

    xls_count: int
    xls_today: int

    pptx_count: int
    pptx_today: int

    txt_count: int
    txt_today: int

    png_count: int
    png_today: int

    jpg_count: int
    jpg_today: int

    jpeg_count: int
    jpeg_today: int