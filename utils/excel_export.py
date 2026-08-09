from openpyxl import Workbook


def export_results(results):

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

    wb.save("output/results.xlsx")