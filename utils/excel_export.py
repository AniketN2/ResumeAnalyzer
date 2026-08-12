from io import BytesIO
from openpyxl import Workbook


def export_results(results) -> bytes:

    wb = Workbook()

    ws = wb.active

    ws.append([
        "Candidate",
        "Score",
        "Recommendation"
    ])

    for result in results:

        ws.append([

            result["candidate"].name,

            result["score"].total_score,

            result["score"].recommendation

        ])

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    return buffer.getvalue()