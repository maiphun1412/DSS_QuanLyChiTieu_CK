from typing import List, Dict, Any


CRITERIA_NAMES = [
    "Mức độ cần thiết",
    "Tác động ngân sách",
    "Khả năng cắt giảm",
    "Tần suất phát sinh",
    "Mức độ linh hoạt",
]


CATEGORY_PROFILES = {
    "Nhà ở": {
        "Mức độ cần thiết": 0.95,
        "Tác động ngân sách": 0.95,
        "Khả năng cắt giảm": 0.15,
        "Tần suất phát sinh": 0.90,
        "Mức độ linh hoạt": 0.10,
    },
    "Ăn uống": {
        "Mức độ cần thiết": 0.85,
        "Tác động ngân sách": 0.70,
        "Khả năng cắt giảm": 0.45,
        "Tần suất phát sinh": 0.95,
        "Mức độ linh hoạt": 0.35,
    },
    "Đi lại": {
        "Mức độ cần thiết": 0.65,
        "Tác động ngân sách": 0.60,
        "Khả năng cắt giảm": 0.50,
        "Tần suất phát sinh": 0.80,
        "Mức độ linh hoạt": 0.45,
    },
    "Học tập": {
        "Mức độ cần thiết": 0.75,
        "Tác động ngân sách": 0.55,
        "Khả năng cắt giảm": 0.35,
        "Tần suất phát sinh": 0.60,
        "Mức độ linh hoạt": 0.35,
    },
    "Giải trí": {
        "Mức độ cần thiết": 0.20,
        "Tác động ngân sách": 0.50,
        "Khả năng cắt giảm": 0.95,
        "Tần suất phát sinh": 0.50,
        "Mức độ linh hoạt": 0.95,
    },
    "Sức khỏe": {
        "Mức độ cần thiết": 0.90,
        "Tác động ngân sách": 0.75,
        "Khả năng cắt giảm": 0.20,
        "Tần suất phát sinh": 0.45,
        "Mức độ linh hoạt": 0.20,
    },
    "Khác": {
        "Mức độ cần thiết": 0.30,
        "Tác động ngân sách": 0.45,
        "Khả năng cắt giảm": 0.85,
        "Tần suất phát sinh": 0.45,
        "Mức độ linh hoạt": 0.85,
    },
}


def _normalize_category_name(name: str) -> str:
    if not name:
        return "Khác"

    value = str(name).strip().lower()

    mapping = {
        "nha o": "Nhà ở",
        "nhà ở": "Nhà ở",
        "housing": "Nhà ở",
        "house": "Nhà ở",
        "rent": "Nhà ở",
        "motel": "Nhà ở",
        "communal": "Nhà ở",
        "phone": "Nhà ở",

        "an uong": "Ăn uống",
        "ăn uống": "Ăn uống",
        "food": "Ăn uống",
        "restaurant": "Ăn uống",
        "restuarant": "Ăn uống",
        "market": "Ăn uống",
        "coffee": "Ăn uống",
        "coffe": "Ăn uống",

        "di lai": "Đi lại",
        "đi lại": "Đi lại",
        "di chuyen": "Đi lại",
        "di chuyển": "Đi lại",
        "transport": "Đi lại",
        "taxi": "Đi lại",
        "fuel": "Đi lại",

        "hoc tap": "Học tập",
        "học tập": "Học tập",
        "study": "Học tập",
        "learning": "Học tập",
        "business": "Học tập",
        "business lunch": "Học tập",
        "business_expenses": "Học tập",

        "giai tri": "Giải trí",
        "giải trí": "Giải trí",
        "entertainment": "Giải trí",
        "film/enjoyment": "Giải trí",
        "events": "Giải trí",
        "joy": "Giải trí",
        "sport": "Giải trí",
        "clothing": "Giải trí",
        "travel": "Giải trí",

        "suc khoe": "Sức khỏe",
        "sức khỏe": "Sức khỏe",
        "health": "Sức khỏe",

        "khac": "Khác",
        "khác": "Khác",
        "other": "Khác",
        "tech": "Khác",
        "shopping": "Khác",
        "mua sam": "Khác",
        "mua sắm": "Khác",
    }

    return mapping.get(value, "Khác")


def _priority_label(score: float) -> str:
    if score >= 0.75:
        return "Rất cao"
    if score >= 0.58:
        return "Cao"
    if score >= 0.42:
        return "Trung bình"
    if score >= 0.28:
        return "Thấp"
    return "Rất thấp"


def _build_reason(category: str, profile: Dict[str, float]) -> str:
    need = profile.get("Mức độ cần thiết", 0.5)
    reducible = profile.get("Khả năng cắt giảm", 0.5)
    flexibility = profile.get("Mức độ linh hoạt", 0.5)

    if reducible >= 0.75 and flexibility >= 0.75 and need <= 0.4:
        return "Dễ cắt giảm vì mức cần thiết thấp và độ linh hoạt cao."
    if need >= 0.8 and reducible <= 0.3:
        return "Thiết yếu, nên hạn chế cắt giảm mạnh."
    if flexibility >= 0.7:
        return "Có thể điều chỉnh linh hoạt theo ngân sách."
    return "Cần cân nhắc tối ưu dựa trên tình hình chi tiêu."


def _convert_ratio_to_saaty(row_value: float, col_value: float) -> str:
    """
    Tạo giá trị so sánh cặp theo thang Saaty từ hồ sơ danh mục.
    Giá trị hàng / cột càng lớn thì danh mục hàng càng được ưu tiên hơn danh mục cột.
    """
    if row_value <= 0 or col_value <= 0:
        return "1"

    ratio = row_value / col_value

    def map_strength(value: float) -> int:
        if value >= 1.85:
            return 9
        if value >= 1.65:
            return 7
        if value >= 1.35:
            return 5
        if value >= 1.15:
            return 3
        return 1

    if ratio >= 1:
        return str(map_strength(ratio))

    inverse = map_strength(1 / ratio)
    if inverse == 1:
        return "1"

    return f"1/{inverse}"


def _build_comparison_matrices(categories: List[str]) -> List[Dict[str, Any]]:
    """
    Tạo 5 bảng so sánh danh mục theo 5 tiêu chí.
    Các danh mục được lấy từ dữ liệu người dùng đã upload/nhập tay.
    """
    matrices = []

    for criterion in CRITERIA_NAMES:
        matrix = []

        for row_category in categories:
            row_profile = CATEGORY_PROFILES.get(row_category, CATEGORY_PROFILES["Khác"])
            row_value = float(row_profile.get(criterion, 0.5))

            row = []

            for col_category in categories:
                col_profile = CATEGORY_PROFILES.get(col_category, CATEGORY_PROFILES["Khác"])
                col_value = float(col_profile.get(criterion, 0.5))

                # Với bài toán cắt giảm chi tiêu:
                # danh mục ít cần thiết hơn sẽ được ưu tiên cắt giảm cao hơn.
                if criterion == "Mức độ cần thiết":
                    row_value_for_compare = 1 - row_value
                    col_value_for_compare = 1 - col_value
                else:
                    row_value_for_compare = row_value
                    col_value_for_compare = col_value

                if row_category == col_category:
                    row.append("1")
                else:
                    row.append(
                        _convert_ratio_to_saaty(
                            row_value_for_compare,
                            col_value_for_compare
                        )
                    )

            matrix.append(row)

        matrices.append({
            "criterion": criterion,
            "categories": categories,
            "matrix": matrix,
        })

    return matrices

def _build_category_criteria_scores(
    categories: List[str],
    category_totals: Dict[str, float],
    category_counts: Dict[str, int],
) -> List[Dict[str, Any]]:
    """
    Trả điểm chi tiết từng danh mục theo từng tiêu chí để Step 4 hiển thị rõ cách tính.
    """
    max_amount = max(category_totals.values()) if category_totals else 1.0
    max_count = max(category_counts.values()) if category_counts else 1

    result = []

    for category in categories:
        profile = CATEGORY_PROFILES.get(category, CATEGORY_PROFILES["Khác"])
        amount = category_totals.get(category, 0.0)
        count = category_counts.get(category, 0)

        frequency_ratio = count / max_count if max_count > 0 else 0
        amount_ratio = amount / max_amount if max_amount > 0 else 0

        criteria_scores = {
            "Mức độ cần thiết": round(1 - profile.get("Mức độ cần thiết", 0.5), 4),
            "Tác động ngân sách": round(
                (profile.get("Tác động ngân sách", 0.5) * 0.5) + (amount_ratio * 0.5),
                4
            ),
            "Khả năng cắt giảm": round(profile.get("Khả năng cắt giảm", 0.5), 4),
            "Tần suất phát sinh": round(
                max(profile.get("Tần suất phát sinh", 0.5), frequency_ratio),
                4
            ),
            "Mức độ linh hoạt": round(profile.get("Mức độ linh hoạt", 0.5), 4),
        }

        result.append({
            "category": category,
            "amount": round(amount, 2),
            "count": count,
            "criteria_scores": criteria_scores,
        })

    return result


def build_dss_recommendation(
    expenses: List[Dict[str, Any]],
    ahp_weights: List[Dict[str, Any]]
) -> Dict[str, Any]:
    if not isinstance(expenses, list) or len(expenses) == 0:
        raise ValueError("Chưa có dữ liệu chi tiêu để phân tích DSS.")

    if not isinstance(ahp_weights, list) or len(ahp_weights) == 0:
        raise ValueError("Chưa có trọng số AHP để phân tích DSS.")

    weights_map: Dict[str, float] = {}
    for item in ahp_weights:
        name = str(item.get("name", "")).strip()
        value = float(item.get("value", 0) or 0)
        if name:
            weights_map[name] = value

    if not weights_map:
        raise ValueError("Trọng số AHP không hợp lệ.")

    category_totals: Dict[str, float] = {}
    category_counts: Dict[str, int] = {}

    for item in expenses:
        category = _normalize_category_name(item.get("category"))
        amount = float(item.get("amount", 0) or 0)

        if amount <= 0:
            continue

        category_totals[category] = category_totals.get(category, 0.0) + amount
        category_counts[category] = category_counts.get(category, 0) + 1

    if not category_totals:
        raise ValueError("Không có khoản chi hợp lệ để phân tích DSS.")

    categories = list(category_totals.keys())
    total_expense = sum(category_totals.values())
    max_amount = max(category_totals.values()) if category_totals else 1.0
    max_count = max(category_counts.values()) if category_counts else 1

    items = []

    for category, amount in category_totals.items():
        profile = CATEGORY_PROFILES.get(category, CATEGORY_PROFILES["Khác"])
        frequency_ratio = category_counts[category] / max_count if max_count > 0 else 0

        need = profile.get("Mức độ cần thiết", 0.5)
        budget_impact = profile.get("Tác động ngân sách", 0.5)
        reducible = profile.get("Khả năng cắt giảm", 0.5)
        profile_frequency = profile.get("Tần suất phát sinh", 0.5)
        flexibility = profile.get("Mức độ linh hoạt", 0.5)

        criteria_scores = {
            "Mức độ cần thiết": 1 - need,
            "Tác động ngân sách": budget_impact,
            "Khả năng cắt giảm": reducible,
            "Tần suất phát sinh": max(profile_frequency, frequency_ratio),
            "Mức độ linh hoạt": flexibility,
        }

        weighted_profile_score = sum(
            weights_map.get(criterion, 0) * criteria_scores.get(criterion, 0)
            for criterion in CRITERIA_NAMES
        )

        amount_factor = 0.65 + 0.35 * (amount / max_amount if max_amount > 0 else 0)
        final_score = weighted_profile_score * amount_factor

        items.append({
            "category": category,
            "amount": round(amount, 2),
            "count": category_counts[category],
            "score_raw": final_score,
            "criteria_scores": {
                key: round(value, 4)
                for key, value in criteria_scores.items()
            },
            "profile": profile,
        })

    max_score = max(item["score_raw"] for item in items) if items else 1.0

    for item in items:
        normalized_score = item["score_raw"] / max_score if max_score > 0 else 0
        item["score"] = round(normalized_score, 4)
        item["priority"] = _priority_label(normalized_score)
        item["reason"] = _build_reason(item["category"], item["profile"])

    items.sort(key=lambda x: x["score"], reverse=True)

    return {
        "total_expense": round(total_expense, 2),
        "criteria": CRITERIA_NAMES,
        "categories": categories,
        "comparison_matrices": _build_comparison_matrices(categories),
        "category_criteria_scores": _build_category_criteria_scores(
            categories=categories,
            category_totals=category_totals,
            category_counts=category_counts,
        ),
        "recommendations": [
            {
                "category": item["category"],
                "amount": item["amount"],
                "count": item["count"],
                "score": item["score"],
                "priority": item["priority"],
                "reason": item["reason"],
                "criteria_scores": item["criteria_scores"],
            }
            for item in items
        ],
    }