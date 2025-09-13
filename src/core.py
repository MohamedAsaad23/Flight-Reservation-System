import heapq

def find_shortest_path(db, start, end):
    
    flights_dict = {}
    db.c.execute("SELECT src, dest, cost FROM flights")
    for src, dest, cost in db.c.fetchall():
        flights_dict.setdefault(src, []).append((dest, cost))

    pq = [(0, start, [])]
    visited = set()

    while pq:
        cost, airport, path = heapq.heappop(pq)
        if airport in visited:
            continue
        path = path + [airport]
        if airport == end:
            return cost, path
        visited.add(airport)
        for neighbor, price in flights_dict.get(airport, []):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + price, neighbor, path))
    return float("inf"), []
