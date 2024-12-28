from datetime import datetime


def investing(target, sources):
    remaining_amount = target.full_amount - target.invested_amount
    invested_amount = target.invested_amount

    for source in sources:
        if remaining_amount <= 0:
            break

        available_amount = source.full_amount - source.invested_amount

        if remaining_amount >= available_amount:
            source.invested_amount = source.full_amount
            source.fully_invested = True
            source.close_date = datetime.now()
            remaining_amount -= available_amount
            invested_amount += available_amount
        else:
            source.invested_amount += remaining_amount
            invested_amount += remaining_amount
            remaining_amount = 0

    target.invested_amount = invested_amount
    if remaining_amount == 0:
        target.fully_invested = True
        target.close_date = datetime.now()

    return target, sources