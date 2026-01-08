from fastmcp import FastMCP
import requests
import xml.etree.ElementTree as ET
import os

os.environ.get("DOTENV_PATH", os.path.join(os.path.dirname(__file__), ".env"))

mcp = FastMCP("LegalAssistant")

BASE_URL = "http://www.law.go.kr/DRF/lawSearch.do?target=prec"


@mcp.tool()
def search_precedents(
    query: str,
    search_type: int = 1,
    display_count: int = 5,
    sort_option: str = "ddes",
    court_type: str = None,
) -> str:
    params = {
        "OC": OC_ID,
        "target": "prec",
        "type": "JSON",  # 처리가 쉬운 JSON 선택
        "search": search_type,
        "query": query,
        "display": display_count,
        "sort": sort_option,
    }

    try:
        response = requests.get(BASE_URL, params=params)
        # XML 파싱 (실제 구현 시에는 더 정교한 예외처리가 필요합니다)
        root = ET.fromstring(response.content)

        results = []
        for prec in root.findall(".//prec"):
            title = prec.findtext("사건명")
            case_no = prec.findtext("사건번호")
            date = prec.findtext("선고일자")
            results.append(f"[{case_no}] {title} ({date})")

        if not results:
            return f"'{keyword}'와 관련된 판례를 찾지 못했습니다."

        return "\n".join(results[:5])  # 상위 5개 결과 반환

    except Exception as e:
        return f"데이터를 가져오는 중 오류 발생: {str(e)}"


@mcp.tool()
def analyze_case_impact(case_text: str) -> str:
    """
    판례의 전문을 입력받아 핵심 쟁점과 판결 결과를 분석합니다.
    (이 도구는 LLM이 판례를 요약할 때 가이드라인 역할을 합니다)
    """
    # 실제로는 LLM이 이 텍스트를 보고 요약하도록 유도하는 컨텍스트 역할을 함
    return f"다음 판례 전문을 분석하여 '사실관계, 법적 쟁점, 최종 판결' 순으로 요약해주세요: {case_text}"


# 3. 서버 실행
if __name__ == "__main__":
    mcp.run()
