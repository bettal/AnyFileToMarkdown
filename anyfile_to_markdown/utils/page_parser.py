def parse_pages(raw: str, total: int):
    if not raw.strip():
        return None
    result = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            a = a.strip()
            b = b.strip()
            start = int(a) - 1 if a else 0
            end = total - 1 if b.upper() == "N" else int(b) - 1
            result.extend(range(start, end + 1))
        else:
            result.append(int(part) - 1)
    return sorted(set(r for r in result if 0 <= r < total))
