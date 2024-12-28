from datetime import datetime

from app.models import FinanceBase


def process_investment(
        target: FinanceBase,
        sources: list[FinanceBase]
) -> list[FinanceBase]:

    use_sources = []
    current_time = datetime.utcnow()

    for source in sources:
        invest_amount = min(
            target.full_amount - target.invested_amount,
            source.full_amount - source.invested_amount
        )
        for obj in (target, source):
            obj.invested_amount += invest_amount
            if obj.invested_amount == obj.full_amount:
                obj.fully_invested = True
                obj.close_date = current_time
        use_sources.append(source)
        if target.fully_invested:
            break
    return use_sources
