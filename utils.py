from collections import defaultdict

def calculate_balances(expenses):
    balances = defaultdict(float)
    for exp in expenses:
        amount = exp["amount"]
        paid_by = exp["paid_by"]
        shared_by = exp.get("shared_by") or list({e["paid_by"] for e in expenses})  # default: all people
        split = amount / len(shared_by)
        for person in shared_by:
            balances[person] -= split
        balances[paid_by] += amount
    return balances

def simplify_settlements(balances):
    from heapq import heappush, heappop
    import math

    pos_heap, neg_heap = [], []
    for person, balance in balances.items():
        if abs(balance) < 1e-2:
            continue
        if balance > 0:
            heappush(pos_heap, (-balance, person))  # max-heap
        else:
            heappush(neg_heap, (balance, person))   # min-heap

    settlements = []
    while pos_heap and neg_heap:
        credit, cr_person = heappop(pos_heap)
        debit, db_person = heappop(neg_heap)

        settle_amount = min(-credit, -debit)
        settlements.append({
            "from": db_person,
            "to": cr_person,
            "amount": round(settle_amount, 2)
        })

        if -credit > settle_amount:
            heappush(pos_heap, (credit + settle_amount, cr_person))
        if -debit > settle_amount:
            heappush(neg_heap, (debit + settle_amount, db_person))

    return settlements
